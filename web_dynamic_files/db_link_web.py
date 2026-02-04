"""
数据库连接模块 | Database Connection Module
提供数据库连接池管理和基础连接功能
"""
import mysql.connector
from mysql.connector import Error, pooling
import streamlit as st
from typing import Optional
from contextlib import contextmanager

# 连接池配置
_connection_pool: Optional[pooling.MySQLConnectionPool] = None


def get_connection_pool(host: str, user: str, password: str, 
                        database: str, port: str, pool_size: int = 5) -> Optional[pooling.MySQLConnectionPool]:
    """
    获取或创建数据库连接池
    
    Args:
        host: 数据库主机
        user: 用户名
        password: 密码
        database: 数据库名
        port: 端口
        pool_size: 连接池大小
    
    Returns:
        MySQLConnectionPool 或 None
    """
    global _connection_pool
    
    try:
        if _connection_pool is None:
            _connection_pool = pooling.MySQLConnectionPool(
                pool_name="crawler_pool",
                pool_size=pool_size,
                pool_reset_session=True,
                host=host,
                user=user,
                password=password,
                database=database,
                port=int(port),
                autocommit=False
            )
        return _connection_pool
    except Error as e:
        st.error(f"创建连接池失败: {e}")
        return None


def link_db(host: str, user: str, password: str, 
            database: str, port: str) -> Optional[mysql.connector.MySQLConnection]:
    """
    获取数据库连接（支持连接池）
    
    Args:
        host: 数据库主机
        user: 用户名
        password: 密码
        database: 数据库名
        port: 端口
    
    Returns:
        数据库连接对象或 None
    """
    try:
        # 尝试从连接池获取
        pool = get_connection_pool(host, user, password, database, port)
        if pool:
            connection = pool.get_connection()
            if connection.is_connected():
                st.success("数据库连接成功（连接池）")
                return connection
        
        # 回退到直接连接
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port),
        )
        
        if connection.is_connected():
            st.success("数据库连接成功")
            return connection
            
    except Error as e:
        st.error(f"连接数据库出错: {e}")
        return None


def close_db(connection, cursor=None) -> None:
    """
    安全关闭数据库连接和游标
    
    Args:
        connection: 数据库连接
        cursor: 游标（可选）
    """
    try:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            st.success("数据库已关闭")
    except Error as e:
        st.warning(f"关闭数据库连接时出错: {e}")


@contextmanager
def get_db_connection(host: str, user: str, password: str, 
                      database: str, port: str):
    """
    数据库连接上下文管理器，自动管理连接生命周期
    
    用法:
        with get_db_connection(...) as conn:
            cursor = conn.cursor()
            cursor.execute(...)
    """
    connection = None
    try:
        connection = link_db(host, user, password, database, port)
        yield connection
    finally:
        if connection:
            close_db(connection)


def reset_connection_pool() -> None:
    """重置连接池（用于配置变更时）"""
    global _connection_pool
    _connection_pool = None
