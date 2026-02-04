"""
数据库写入模块 | Database Write Module
提供表创建和数据批量插入功能
"""
from urllib.parse import urlparse
from typing import Dict, List, Any, Optional
import streamlit as st
from db_link_web import link_db, close_db
from mysql.connector import Error
import sys
import os

# 添加父目录到路径以导入 config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import validate_table_name


def get_url_name(url: str) -> str:
    """
    从 URL 中提取域名作为文件名
    
    Args:
        url: 网页 URL
    
    Returns:
        域名字符串
    """
    if not url:
        return "unknown"
    netloc = urlparse(url).netloc
    domain = netloc.split('.')[0] if netloc else "unknown"
    return domain


def create_table(table_name: str, schema: Dict[str, str], 
                 host: str, user: str, password: str, 
                 database: str, port: str) -> bool:
    """
    自动创建数据表
    
    Args:
        table_name: 表名
        schema: 字段和类型映射
        host, user, password, database, port: 数据库配置
    
    Returns:
        是否创建成功
    """
    # 验证表名
    if not validate_table_name(table_name):
        st.error("表名格式不正确，只能包含字母、数字、下划线")
        return False
    
    connection = link_db(host, user, password, database, port)
    if not connection:
        st.error("连接失败，表格无法创建")
        return False
    
    cursor = None
    try:
        # 默认字段
        columns = ["id INT NOT NULL AUTO_INCREMENT PRIMARY KEY"]
        default_fields = {
            "title": "VARCHAR(255)",
            "url": "LONGTEXT NOT NULL",
            "content": "LONGTEXT",
            "image": "TEXT",
            "HTML": "LONGTEXT",
        }
        
        # 添加默认字段
        for field, data_type in default_fields.items():
            if field not in schema:
                columns.append(f'`{field}` {data_type}')
        
        # 添加自定义字段（转义防止注入）
        for field, data_type in schema.items():
            safe_field = field.replace('`', '``')
            columns.append(f'`{safe_field}` {data_type}')
        
        columns_sql = ",\n    ".join(columns)
        create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS `{table_name}` (
                {columns_sql}
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        '''
        
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
        connection.commit()
        st.success(f"表 `{table_name}` 创建成功")
        return True
        
    except Error as e:
        st.error(f"创建表格失败: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        close_db(connection, cursor)


def insert_news(finial_content: List[Dict[str, Any]], table_name: str,
                host: str, user: str, password: str, 
                database: str, port: str, batch_size: int = 50) -> tuple:
    """
    批量插入新闻数据
    
    Args:
        finial_content: 要插入的数据列表
        table_name: 目标表名
        host, user, password, database, port: 数据库配置
        batch_size: 批量插入大小
    
    Returns:
        (成功数, 失败数) 元组
    """
    # 验证表名
    if not validate_table_name(table_name):
        st.error("表名格式不正确")
        return (0, 0)
    
    if not finial_content:
        st.warning("没有数据需要插入")
        return (0, 0)
    
    connection = link_db(host, user, password, database, port)
    if not connection:
        st.error("数据库连接失败")
        return (0, len(finial_content))
    
    cursor = None
    success = 0
    failed = 0
    
    try:
        cursor = connection.cursor()
        
        # 标准字段顺序
        standard_fields = ["title", "url", "content", "image", "HTML"]
        
        # 批量处理数据
        batch = []
        for i, news in enumerate(finial_content):
            fields = []
            values = []
            
            # 处理标准字段
            for field in standard_fields:
                if field in news:
                    fields.append(field)
                    values.append(news[field])
            
            # 处理自定义字段
            for field, value in news.items():
                if field not in standard_fields:
                    fields.append(field)
                    values.append(value)
            
            batch.append((fields, values))
            
            # 达到批量大小或最后一条数据时执行插入
            if len(batch) >= batch_size or i == len(finial_content) - 1:
                batch_success, batch_failed = _execute_batch_insert(
                    cursor, connection, table_name, batch
                )
                success += batch_success
                failed += batch_failed
                batch = []
        
        st.success(f"成功插入 {success} 条数据，失败 {failed} 条")
        return (success, failed)
        
    except Exception as e:
        st.error(f"插入数据时发生错误: {e}")
        if connection:
            connection.rollback()
        return (success, failed + len(finial_content) - success)
    finally:
        close_db(connection, cursor)


def _execute_batch_insert(cursor, connection, table_name: str, 
                          batch: List[tuple]) -> tuple:
    """
    执行批量插入
    
    Args:
        cursor: 数据库游标
        connection: 数据库连接
        table_name: 表名
        batch: 批量数据 [(fields, values), ...]
    
    Returns:
        (成功数, 失败数)
    """
    success = 0
    failed = 0
    
    for fields, values in batch:
        try:
            fields_str = ", ".join([f"`{f}`" for f in fields])
            placeholders = ", ".join(["%s"] * len(values))
            insert_sql = f"INSERT INTO `{table_name}` ({fields_str}) VALUES ({placeholders})"
            
            cursor.execute(insert_sql, values)
            success += 1
        except Exception as e:
            failed += 1
            # 只在调试时显示详细错误
            # st.warning(f"插入失败: {e}")
    
    # 批量提交
    try:
        connection.commit()
    except Exception as e:
        connection.rollback()
        st.warning(f"批量提交失败: {e}")
    
    return (success, failed)


def insert_single(data: Dict[str, Any], table_name: str,
                  host: str, user: str, password: str,
                  database: str, port: str) -> bool:
    """
    插入单条数据
    
    Args:
        data: 要插入的数据字典
        table_name: 目标表名
        host, user, password, database, port: 数据库配置
    
    Returns:
        是否插入成功
    """
    success, failed = insert_news([data], table_name, host, user, password, database, port)
    return success > 0
