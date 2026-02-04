"""
国际化模块 | Internationalization Module
支持中英双语切换
"""

# 翻译字典
TRANSLATIONS = {
    # ==================== 通用 | Common ====================
    "app_title": {
        "zh": "🕷️ 动态网页爬虫工具",
        "en": "🕷️ Dynamic Web Crawler"
    },
    "welcome": {
        "zh": "🏠 欢迎使用动态网页爬虫",
        "en": "🏠 Welcome to Dynamic Web Crawler"
    },
    "back_home": {
        "zh": "← 返回主页",
        "en": "← Back to Home"
    },
    "language": {
        "zh": "🌐 语言",
        "en": "🌐 Language"
    },
    
    # ==================== 主页 | Home ====================
    "web_crawler": {
        "zh": "🔍 网页爬虫",
        "en": "🔍 Web Crawler"
    },
    "crawler_desc": {
        "zh": "支持动态加载页面的数据抓取",
        "en": "Scrape data from dynamically loaded pages"
    },
    "enter_dynamic": {
        "zh": "进入动态页爬取",
        "en": "Enter Dynamic Crawler"
    },
    "db_search": {
        "zh": "📊 数据库搜索",
        "en": "📊 Database Search"
    },
    "db_search_desc": {
        "zh": "搜索已爬取的数据",
        "en": "Search crawled data"
    },
    "enter_search": {
        "zh": "进入数据库搜索",
        "en": "Enter Database Search"
    },
    
    # ==================== 爬虫页面 | Crawler Page ====================
    "crawler_title": {
        "zh": "**🔍动态网站爬虫工具**",
        "en": "**🔍 Dynamic Website Crawler**"
    },
    "intro": {
        "zh": ">*介绍：*",
        "en": ">*Introduction:*"
    },
    "intro_desc1": {
        "zh": ">*当前工具默认爬取无刷加载网页，即不分页下拉自动加载。如："今日头条"、"稀土掘金"等*",
        "en": ">*This tool crawls infinite scroll pages (auto-load on scroll). e.g., Toutiao, Juejin*"
    },
    "intro_desc2": {
        "zh": ">*如果当前网址已经进入新闻，请勾选"当前为新闻详情页"*",
        "en": ">*If you're on a news detail page, check \"Current page is detail page\"*"
    },
    "crawler_config": {
        "zh": "爬虫配置",
        "en": "Crawler Configuration"
    },
    "basic_settings": {
        "zh": "基本设置",
        "en": "Basic Settings"
    },
    "target_url": {
        "zh": "目标URL",
        "en": "Target URL"
    },
    "target_url_help": {
        "zh": "爬取目标网址",
        "en": "URL to crawl"
    },
    "is_detail_page": {
        "zh": "当前为新闻详情页",
        "en": "Current page is detail page"
    },
    "is_detail_page_help": {
        "zh": "勾选代表没有新闻列表，当前就是新闻详情页",
        "en": "Check if this is a detail page, not a list page"
    },
    "fetch_count": {
        "zh": "爬取新闻数量 >= 1",
        "en": "Number of items to fetch >= 1"
    },
    "request_header": {
        "zh": "URL请求头(可选）",
        "en": "Request Header (optional)"
    },
    "request_header_help": {
        "zh": "请求头模拟真实用户进入网页时的请求，可以越过一定的反爬机制",
        "en": "Request header simulates real user requests, can bypass some anti-crawler"
    },
    "driver_path": {
        "zh": "Edge驱动路径",
        "en": "Edge Driver Path"
    },
    "wait_time": {
        "zh": "等待页面元素时间 >= 20",
        "en": "Wait time for elements >= 20"
    },
    "wait_time_help": {
        "zh": "页面动态少的（如今日头条）建议设置20秒以上，页面动态多的（如淘宝）建议设置50秒以上",
        "en": "For less dynamic pages: 20s+, for more dynamic pages (Taobao): 50s+"
    },
    "interval_time": {
        "zh": "间隔时间 >= 0.5",
        "en": "Interval time >= 0.5"
    },
    "interval_help": {
        "zh": "⏱️ 建议设置0.5秒以上，避免请求过于频繁",
        "en": "⏱️ Set 0.5s+ to avoid too frequent requests"
    },
    "headless_mode": {
        "zh": "无窗口模式",
        "en": "Headless Mode"
    },
    "headless_help": {
        "zh": "勾选后将在后台运行浏览器",
        "en": "Run browser in background when checked"
    },
    "save_config": {
        "zh": "保存基本配置",
        "en": "Save Configuration"
    },
    "save_config_help": {
        "zh": "防止网页刷新后自定义丢失",
        "en": "Prevent losing settings on page refresh"
    },
    "clear_cache": {
        "zh": "清理缓存",
        "en": "Clear Cache"
    },
    "save_success": {
        "zh": "保存成功",
        "en": "Saved successfully"
    },
    
    # ==================== 高级筛选 | Advanced Filter ====================
    "advanced_filter": {
        "zh": "高级筛选",
        "en": "Advanced Filter"
    },
    "element_locator": {
        "zh": "元素定位",
        "en": "Element Locators"
    },
    "news_url_tag": {
        "zh": "**新闻url标签设置(新闻列表)**",
        "en": "**News URL Tag Settings (List Page)**"
    },
    "locator_method": {
        "zh": "定位方式",
        "en": "Locator Method"
    },
    "tag": {
        "zh": "标签",
        "en": "Tag"
    },
    "selector": {
        "zh": "选择器",
        "en": "Selector"
    },
    "title_tag": {
        "zh": "**标题元素标签设置**",
        "en": "**Title Element Settings**"
    },
    "content_tag": {
        "zh": "**内容元素标签设置**",
        "en": "**Content Element Settings**"
    },
    "image_tag": {
        "zh": "**图片元素标签设置**",
        "en": "**Image Element Settings**"
    },
    
    # ==================== 自定义字段 | Custom Fields ====================
    "add_custom_field": {
        "zh": "➕ 添加自定义字段",
        "en": "➕ Add Custom Field"
    },
    "field_name": {
        "zh": "名称",
        "en": "Name"
    },
    "field_name_help": {
        "zh": "比如：姓名/年龄 等",
        "en": "e.g., Name/Age etc."
    },
    "field_type": {
        "zh": "类型",
        "en": "Type"
    },
    "field_type_help": {
        "zh": "当前需要爬取的类型",
        "en": "Type of data to extract"
    },
    "confirm": {
        "zh": "确认",
        "en": "Confirm"
    },
    "name_empty": {
        "zh": "名称不能为空",
        "en": "Name cannot be empty"
    },
    "name_exists": {
        "zh": "该名称已存在",
        "en": "This name already exists"
    },
    "add_success": {
        "zh": "成功添加：",
        "en": "Successfully added: "
    },
    "current_fields": {
        "zh": "### 📝 当前自定义字段",
        "en": "### 📝 Current Custom Fields"
    },
    "clear_all_custom": {
        "zh": "清除所有自定义",
        "en": "Clear All Custom Fields"
    },
    "custom_cleared": {
        "zh": "自定义清理成功",
        "en": "Custom fields cleared"
    },
    "no_config_to_delete": {
        "zh": "没有配置文件需要删除",
        "en": "No config file to delete"
    },
    
    # ==================== 关键词模式 | Keyword Mode ====================
    "html_tag_input": {
        "zh": "请输入单条新闻通用HTML标签",
        "en": "Enter common HTML tag for news items"
    },
    "html_tag_help": {
        "zh": "使用关键词对多条新闻筛选需要先填写新闻url标签定位,在HTML中以'<xx '开头",
        "en": "For keyword filtering, first set news URL tag locator (starts with '<xx ' in HTML)"
    },
    "key_element": {
        "zh": "请输入单条新闻通用HTML标签关键元素",
        "en": "Enter key element attribute for news items"
    },
    "key_element_help": {
        "zh": "用来分开异类，在HTML中以class= 、id= 等显示",
        "en": "Used to distinguish items, shown as class=, id= etc. in HTML"
    },
    "keyword": {
        "zh": "关键词",
        "en": "Keyword"
    },
    "keyword_help": {
        "zh": "通过关键词搜索该页信息",
        "en": "Search page info by keyword"
    },
    
    # ==================== 数据类型 | Data Types ====================
    "text": {
        "zh": "文本",
        "en": "Text"
    },
    "image": {
        "zh": "图片",
        "en": "Image"
    },
    "url": {
        "zh": "网址",
        "en": "URL"
    },
    "link": {
        "zh": "链接",
        "en": "Link"
    },
    "phone": {
        "zh": "电话",
        "en": "Phone"
    },
    "email": {
        "zh": "邮箱",
        "en": "Email"
    },
    "age": {
        "zh": "年龄",
        "en": "Age"
    },
    
    # ==================== 爬取控制 | Crawling Control ====================
    "start_crawl": {
        "zh": "开始爬取",
        "en": "Start Crawling"
    },
    "crawling_info": {
        "zh": "配置爬虫参数并点击'开始爬取'按钮",
        "en": "Configure parameters and click 'Start Crawling'"
    },
    "crawling_progress": {
        "zh": "爬取进行中，请稍候...",
        "en": "Crawling in progress, please wait..."
    },
    "crawl_complete": {
        "zh": "爬取完成",
        "en": "Crawling complete"
    },
    "url_empty": {
        "zh": "URL不得为空",
        "en": "URL cannot be empty"
    },
    "tag_format_error": {
        "zh": "请输入正确标签形式",
        "en": "Please enter correct tag format"
    },
    "url_tag_error": {
        "zh": "url标签格式错误",
        "en": "URL tag format error"
    },
    "url_not_filled": {
        "zh": "url未填写",
        "en": "URL not filled"
    },
    
    # ==================== 结果显示 | Results ====================
    "results": {
        "zh": "爬取结果",
        "en": "Crawling Results"
    },
    "download_excel": {
        "zh": "下载Excel",
        "en": "Download Excel"
    },
    "download_csv": {
        "zh": "下载CSV",
        "en": "Download CSV"
    },
    "save_to_db": {
        "zh": "储存数据库",
        "en": "Save to Database"
    },
    "table_name": {
        "zh": "输入表格名称(新名创建，同名添加）",
        "en": "Enter table name (new name creates, same name appends)"
    },
    "table_name_help": {
        "zh": "只能包含英文或数字",
        "en": "Only letters and numbers allowed"
    },
    "reset": {
        "zh": "重置",
        "en": "Reset"
    },
    "reset_help": {
        "zh": "输入参数归为默认",
        "en": "Reset parameters to default"
    },
    "continue_crawl": {
        "zh": "继续爬取",
        "en": "Continue Crawling"
    },
    "continue_help": {
        "zh": "输入参数不变",
        "en": "Keep current parameters"
    },
    "confirm_reset": {
        "zh": "确定要清空所有参数吗？操作不可撤销",
        "en": "Are you sure to clear all parameters? This cannot be undone"
    },
    "confirm_clear": {
        "zh": "确认清空",
        "en": "Confirm Clear"
    },
    "cancel": {
        "zh": "取消",
        "en": "Cancel"
    },
    
    # ==================== 数据库 | Database ====================
    "db_title": {
        "zh": "📊 MySQL 表格数据搜索",
        "en": "📊 MySQL Table Data Search"
    },
    "db_params": {
        "zh": "数据库参数(以下为默认参数，按需修改)",
        "en": "Database Parameters (default values, modify as needed)"
    },
    "enter_table_name": {
        "zh": "输入表名：",
        "en": "Enter table name:"
    },
    "table_name_rule": {
        "zh": "输入table名称（只能包含字母、数字、下划线）",
        "en": "Enter table name (only letters, numbers, underscores)"
    },
    "load_data": {
        "zh": "加载数据",
        "en": "Load Data"
    },
    "table_name_error": {
        "zh": "表名格式不正确，只能包含字母、数字、下划线，且不能以数字开头",
        "en": "Invalid table name. Only letters, numbers, underscores allowed. Cannot start with number"
    },
    "db_connect_success": {
        "zh": "数据库连接成功",
        "en": "Database connected successfully"
    },
    "db_connect_fail": {
        "zh": "数据库连接失败",
        "en": "Database connection failed"
    },
    "searching": {
        "zh": "正在搜索...",
        "en": "Searching..."
    },
    "db_query_error": {
        "zh": "查询数据库时出错",
        "en": "Error querying database"
    },
    "db_closed": {
        "zh": "数据库已关闭",
        "en": "Database closed"
    },
    
    # ==================== 错误信息 | Error Messages ====================
    "webdriver_fail": {
        "zh": "WebDriver启动失败",
        "en": "WebDriver startup failed"
    },
    "check_browser": {
        "zh": "请检查Edge浏览器和EdgeDriver是否正确安装",
        "en": "Please check if Edge browser and EdgeDriver are installed correctly"
    },
    "crawl_error": {
        "zh": "爬取过程中出现错误",
        "en": "Error during crawling"
    },
    "check_network": {
        "zh": "请检查网络连接和网页元素选择器是否正确",
        "en": "Please check network connection and element selectors"
    },
    "insert_success": {
        "zh": "成功插入",
        "en": "Successfully inserted"
    },
    "insert_fail": {
        "zh": "失败",
        "en": "failed"
    },
    "records": {
        "zh": "条数据",
        "en": "records"
    },
    "table_created": {
        "zh": "表创建成功",
        "en": "Table created successfully"
    },
    "data_saved": {
        "zh": "数据已保存到MySQL数据库表",
        "en": "Data saved to MySQL table"
    },
}


def get_text(key: str, lang: str = "zh") -> str:
    """
    获取翻译文本
    
    Args:
        key: 翻译键
        lang: 语言代码 ("zh" 或 "en")
    
    Returns:
        翻译后的文本
    """
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get("zh", key))
    return key


def t(key: str, lang: str = "zh") -> str:
    """get_text 的简写"""
    return get_text(key, lang)
