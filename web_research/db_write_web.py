"""
数据库写入模块（web_research）
从 web_dynamic_files 导入以保持一致性
"""
import sys
import os

# 添加 web_dynamic_files 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'web_dynamic_files'))

from db_write_web import (
    get_url_name, create_table, insert_news, insert_single
)

__all__ = ['get_url_name', 'create_table', 'insert_news', 'insert_single']
