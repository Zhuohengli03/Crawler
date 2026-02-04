"""
数据库搜索模块 | Database Search Module
"""
import re
import os
import sys

import streamlit as st
import pandas as pd

# 添加路径以导入模块
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
sys.path.insert(0, _current_dir)
sys.path.insert(0, _parent_dir)

from db_link_web import link_db
from i18n import t


def get_lang():
    """获取当前语言设置"""
    return st.session_state.get('lang', 'zh')


def validate_table_name(table_name: str) -> bool:
    """验证表名是否安全（只允许字母、数字、下划线）"""
    if not table_name:
        return False
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name))


def web_research():
    """数据库搜索主函数"""
    lang = get_lang()
    
    st.title(t("db_title", lang))
    
    # 数据库配置
    with st.expander(t("db_params", lang)):
        host = st.text_input("HOST", "127.0.0.1", key="research_host")
        user = st.text_input("USER", "root", key="research_user")
        password = st.text_input("PASSWORD", type="password", key="research_password")
        database = st.text_input("DATABASE", "pages", key="research_database")
        port = st.text_input("PORT", "3306", key="research_port")
    
    # 表名输入
    table = st.text_input(t("enter_table_name", lang), help=t("table_name_rule", lang), key="research_table")
    
    # 关键词选择 - 双语
    if lang == "en":
        key_words_options = ["URL", "Phone(+86)", "Name", "Email", "International Phone", "Image"]
        key_map = {
            "URL": r'https?://[^\s<>"]+',
            "Phone(+86)": r'(?:\+86)?[\s-]?1[3-9]\d{9}',
            "Name": r'^[\u4e00-\u9fa5]{2,4}$',
            "Email": r'[\w\.]+@[\w]+\.[\w]{0,4}',
            "International Phone": r'\(?\+?[0-9]{1,3}\)?[\s-]?[0-9]{8}',
            "Image": r'https?://.*\.(jpg|png|jpeg|gif)'
        }
    else:
        key_words_options = ["网址", "电话(+86)", "姓名", "邮箱", "国际电话", "图片"]
        key_map = {
            "网址": r'https?://[^\s<>"]+',
            "电话(+86)": r'(?:\+86)?[\s-]?1[3-9]\d{9}',
            "姓名": r'^[\u4e00-\u9fa5]{2,4}$',
            "邮箱": r'[\w\.]+@[\w]+\.[\w]{0,4}',
            "国际电话": r'\(?\+?[0-9]{1,3}\)?[\s-]?[0-9]{8}',
            "图片": r'https?://.*\.(jpg|png|jpeg|gif)'
        }
    
    research_content = st.selectbox(t("keyword", lang), key_words_options,
                                    help=t("keyword_help", lang), key="research_key_select")
    
    if st.button(t("load_data", lang), key="research_load"):
        if not validate_table_name(table):
            st.error(t("table_name_error", lang))
            return
        
        conn = None
        try:
            conn = link_db(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            
            if not conn:
                st.error(t("db_connect_fail", lang))
                return
            
            st.success(t("searching", lang))
            
            # 使用反引号包裹表名，防止SQL注入（表名已验证）
            safe_table = f"`{table}`"
            df = pd.read_sql(f"SELECT * FROM {safe_table}", conn)
            
            # 关键词所输出的正则模式
            pattern = key_map[research_content]
            
            # 输出结果
            final_results = []
            
            # 从HTML列来筛选出信息
            if 'HTML' in df.columns:
                for html_content in df['HTML']:
                    html_str = str(html_content)
                    content_match = re.findall(pattern, html_str)
                    # 去重
                    content = set(content_match)
                    final_results.append(content)
                
                # 将输出呈现为表格
                df[research_content] = final_results
            
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"{t('db_query_error', lang)}: {e}")
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass


# 仅在直接运行时执行
if __name__ == "__main__":
    web_research()
