"""
公共配置模块 | Common Configuration Module
存放项目通用常量、配置和工具函数
"""
from typing import Dict, Any, Optional
from selenium.webdriver.common.by import By


# ==================== 元素定位方式映射 ====================
BY_MAPPING: Dict[str, str] = {
    "XPATH": By.XPATH,
    "CSS选择器": By.CSS_SELECTOR,
    "ID": By.ID,
    "CLASS": By.CLASS_NAME,
    "TAG": By.TAG_NAME
}


# ==================== 数据库默认配置 ====================
DEFAULT_DB_CONFIG: Dict[str, Any] = {
    "host": "127.0.0.1",
    "port": "3306",
    "user": "root",
    "password": "",
    "database": "pages"
}


# ==================== 爬虫默认配置 ====================
DEFAULT_CRAWLER_CONFIG: Dict[str, Any] = {
    "wait_time": 30,           # 等待页面元素时间（秒）
    "time_sleep": 1.0,         # 请求间隔时间（秒）
    "total_to_fetch": 5,       # 默认爬取数量
    "max_scroll_attempts": 20, # 最大滚动次数
    "page_load_timeout": 30,   # 页面加载超时（秒）
    "script_timeout": 30,      # 脚本执行超时（秒）
    "implicit_wait": 10,       # 隐式等待时间（秒）
}


# ==================== 数据类型检测阈值 ====================
VARCHAR_MAX_LENGTH = 500      # VARCHAR 最大长度
TEXT_THRESHOLD = 500          # 超过此长度使用 LONGTEXT


# ==================== 正则表达式模式 ====================
REGEX_PATTERNS: Dict[str, str] = {
    "网址": r'https?://[^\s<>"]+',
    "电话": r'\b(?:\+[()\d]{2,3})?1\d{10}\b|\b(?:\d{3}[-\s]){3}\b',
    "电话(+86)": r'(?:\+86)?[\s-]?1[3-9]\d{9}',
    "邮箱": r'[\w\.]+@[\w]+\.[\w]{0,4}',
    "年龄": r'^(?:120|1[01][0-9]|[1-9][0-9]?|[1-9])$',
    "图片": r'<img.*?src="([^"]+)[.jpg|.png|.gif|.image]*"',
    "姓名": r'^[\u4e00-\u9fa5]{2,4}$',
    "国际电话": r'\(?\+?[0-9]{1,3}\)?[\s-]?[0-9]{8}',
}


# ==================== WebDriver 配置选项 ====================
WEBDRIVER_OPTIONS = [
    "--disable-features=EdgeChinaBrowsersImport",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-plugins",
    "--disable-images",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--disable-features=TranslateUI",
    "--disable-ipc-flooding-protection",
    "--memory-pressure-off",
    "--max_old_space_size=4096",
    "--window-size=1920,1080",
    "--start-maximized",
]


# ==================== 工具函数 ====================
def get_webdriver_options(headless: bool = False) -> list:
    """获取 WebDriver 配置选项列表"""
    options = WEBDRIVER_OPTIONS.copy()
    if headless:
        options.append("--headless")
    return options


def validate_table_name(table_name: str) -> bool:
    """
    验证表名是否安全（防止 SQL 注入）
    只允许字母、数字、下划线，且不能以数字开头
    """
    import re
    if not table_name:
        return False
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name))


def detect_data_type(value) -> str:
    """根据值自动检测 MySQL 数据类型"""
    import re
    import pandas as pd
    
    if pd.isna(value):
        return "TEXT"
    if isinstance(value, bool):
        return "BOOLEAN"
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "FLOAT"
    
    str_value = str(value)
    
    # 检测日期时间格式
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str_value):
        return "DATETIME"
    if re.match(r'^\d{4}-\d{2}-\d{2}', str_value):
        return "DATE"
    
    # 根据长度决定类型
    if len(str_value) < VARCHAR_MAX_LENGTH:
        return "VARCHAR(500)"
    return "LONGTEXT"


def generate_table_schema(data: list) -> Dict[str, str]:
    """根据爬取的数据生成表结构"""
    if not data:
        return {}
    
    # 合并所有数据点的键
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())
    
    # 为每个键确定数据类型
    schema = {}
    for key in all_keys:
        values = [item.get(key) for item in data if key in item]
        if not values:
            schema[key] = "TEXT"
            continue
        
        detected_types = {detect_data_type(v) for v in values}
        # 如果有多种类型，默认使用 LONGTEXT
        schema[key] = "LONGTEXT" if len(detected_types) > 1 else detected_types.pop()
    
    return schema
