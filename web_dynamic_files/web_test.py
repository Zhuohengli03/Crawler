# 读取、写入、解析 JSON 数据（JSON 是一种轻量级的数据交换格式）
import json
# 处理路径、文件、目录、系统环境变量等
import os
# 文本中查找、提取、替换复杂模式（如手机号、网址、日期），正则算法
import re
# 导入streamlit库
import streamlit as st
# 导入 元素定位方式
from selenium.webdriver.common.by import By
# 创建浏览器入口
from selenium import webdriver
# 定制 EdgeDriver 的启动方式通过edge，".<edge>."可更换
from selenium.webdriver.edge.service import Service as EdgeService
# 配置相应驱动器参数，如：是否无头运行（headless）、禁用扩展、窗口大小、是否启用日志、代理等
from selenium.webdriver.edge.options import Options
from db_write_web import create_table, insert_news, get_url_name
import pandas as pd
from result_web import WebCrawler
import io


def detect_data_type(value):
    if pd.isna(value):
        return "TEXT"
    if isinstance(value, int):
        return "INT"
    if isinstance(value, float):
        return "FLOAT"
    if isinstance(value, bool):
        return "BOOLEAN"
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(value)):
        return "DATETIME"
    if re.match(r'^\d{4}-\d{2}-\d{2}', str(value)):
        return "DATE"
    if len(str(value)) < 255:
        return "VARCHAR(255)"
    if re.match(r'^https?://', str(value)):
        return "VARCHAR(500)"
    return "LONGTEXT"


def generate_table_schema(data):
    """根据爬取的数据生成表结构"""
    if not data:
        return {}

    # 合并所有数据点的键
    # """set()成员检测、消除重复元素"""
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())

    # 为每个键确定数据类型
    schema = {}
    for key in all_keys:
        # 收集该键的所有值
        values = [item.get(key) for item in data if key in item]
        if not values:
            schema[key] = "TEXT"
            continue

        # 检测数据类型
        detected_types = {detect_data_type(v) for v in values}

        # 如果有多种类型，默认使用TEXT
        if len(detected_types) > 1:
            schema[key] = "LONGTEXT"
        else:
            schema[key] = detected_types.pop()

    return schema


def save_json(filename="pages_rubbish.json"):
    config = {
        "url": st.session_state.url,
        "driver_path": st.session_state.driver_path,
        "header_request": st.session_state.header_request,
        "new_content": st.session_state.new_content,
        "total_to_fetch": st.session_state.total_to_fetch,
        "wait_time": st.session_state.wait_time,
        "time_sleep": st.session_state.time_sleep,
        "headless": st.session_state.headless,
        "higher_requests": st.session_state.higher_requests,
        "final_content": st.session_state.final_content,
        "main_tag": st.session_state.main_tag,
        "main_element": st.session_state.main_element,
        "custom_fields": st.session_state.custom_fields,
        "main_key_words": st.session_state.main_key_words,
        "show_results": st.session_state.show_results,
        "table_name": st.session_state.table_name,
        "host": st.session_state.host,
        "port": st.session_state.port,
        "user": st.session_state.user,
        "password": st.session_state.password,
        "database": st.session_state.database,

    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


def open_json(filename="pages_rubbish.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
            for key, value in config.items():
                st.session_state[key] = value


def delete_json(filename="pages_rubbish.json"):
    if os.path.exists(filename):
        os.remove(filename)
        st.success(f"{filename} 已删除")
    else:
        st.warning(f"{filename} 文件不存在")


def initial():
    default_states = {
        "crawling": False,
        "final_content": [],
        "custom_fields": [],
        "table_name": "",
        "higher_requests": False,
        "show_results": False,
        "headless": False,
        "url": "",
        "driver_path": "",
        "new_content": False,
        "total_to_fetch": 5,
        "wait_time": 20,
        "time_sleep": 1.0,
        "main_tag": "",
        "main_element": "",
        "main_key_words": "",
        "header_request": "",
        "host":"",
        "user":"",
        "password":"",
        "database":"",
        "port":""

    }
    for key, value in default_states.items():
        st.session_state.setdefault(key, value)

    if "config_loaded" not in st.session_state:
        open_json()
        st.session_state.config_loaded = True

    # -----------------------基本设置与初始参数----------------------------
    UI(key_prefix="main")

# ----------------------------用户交互-----------------------------------------------
def UI(key_prefix="main"):
    if not st.session_state.crawling:
        # 页面布局
        st.title("**🔍动态网站爬虫工具**")
        st.markdown(">*介绍：*")
        st.markdown(">*前工具默认爬取无刷加载网页，即不分页下拉自动加载。如：“今日头条”、“稀土掘金”等*")
        st.markdown(">*如果当前网址已经进入新闻，请勾选“当前为新闻详情页”*")
        st.markdown(">*运行过程中多次点击按钮*")
        st.markdown(">*开始日期：2025.6.11*")
        st.markdown(">*完成日期：*")

        # 配置区域
        st.header("爬虫配置")

        # 基本设置
        st.subheader("基本设置")
        url = st.text_input("目标URL",
                            "https://zh.wikipedia.org/wiki/%E7%A7%91%E6%AF%94%C2%B7%E5%B8%83%E8%8E%B1%E6%81%A9%E7%89%B9",
                            help="爬取目标网址", key=f"{key_prefix}_text_input")



        st.session_state.new_content = st.checkbox("当前为新闻详情页",
                                                   help="勾选代表没有新闻列表，当前就是新闻详情页", value=False)
        if not st.session_state.new_content:
            # 当前是新闻列表
            st.session_state.total_to_fetch = st.number_input("爬取新闻数量 >= 1", min_value=0, value=5,
                                                              key=f"{key_prefix}_total_to_fetch")
            if int(st.session_state.total_to_fetch) < 0:
                st.error("请输入正整数")


        header_request = st.text_input("URL请求头(可选）",
                                       help="请求头模拟真实用户进入网页时的请求，可以越过一定的反爬机制")
        driver_path = st.text_input("Edge驱动路径",
                                    r"D:\pycharm\PyCharm 2024.3.1.1\Projects\pages\edgedriver_win64\msedgedriver.exe")
        wait_time = st.number_input("等待页面元素时间 >= 10", help=" 建议设置10秒以上，确保页面元素加载完成",
                                    min_value=1, value=20, key=f"{key_prefix}_wait_time")
        time_sleep = st.number_input("间隔时间 >= 0.5", help="⏱️ 建议设置0.5秒以上，避免请求过于频繁", min_value=0.5,
                                     value=1.0, key=f"{key_prefix}_time_sleep")
        headless = st.checkbox("无窗口模式", help="勾选后将在后台运行浏览器", value=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("保存基本配置", help="防止网页刷新后自定义丢失"):
                st.session_state.url = url
                st.session_state.driver_path = driver_path
                st.session_state.wait_time = wait_time
                st.session_state.time_sleep = time_sleep
                st.session_state.headless = headless
                st.session_state.crawling = False
                save_json()
                st.success("保存成功")
        with col2:
            if st.button("清理缓存"):
                delete_json()


        higher_or_tag(url, driver_path, wait_time, time_sleep, headless)



    if st.session_state.show_results:
        show_result()


# --------------------------------筛选方式（关键词/高级/标签）----------------------------------
def higher_or_tag(url, driver_path, wait_time, time_sleep, headless):
    # 是否使用高级筛选或标签搜索
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.higher_requests = st.checkbox("高级筛选", value=False)
        st.session_state.key_words = ''
    with col2:
        if not st.session_state.higher_requests:
            st.session_state.tag_check = st.checkbox("使用标签搜索", value=False)

    # 用高级筛选\搜索栏\标签

    if st.session_state.higher_requests:
        st.session_state.main_key_words = []
        # 使用高级筛选
        # 元素定位设置
        st.subheader("元素定位")
        st.session_state.by_mapping = {
            "XPATH": By.XPATH,
            "CSS选择器": By.CSS_SELECTOR,
            "ID": By.ID,
            "类名": By.CLASS_NAME,
            "标签名": By.TAG_NAME
        }

        # 如果未勾选新闻详情页（新闻详情页不需要主标签）
        if not st.session_state.new_content:
            # 主元素（列表）
            st.write("**新闻url标签设置(新闻列表)**")
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("定位方式", list(st.session_state.by_mapping.keys()), key="main_key")
            with col2:
                st.text_input("标签", '//div[contains(@class, "title-row")]//a',
                              key="main_column")

        # 标题元素
        st.write("**标题元素标签设置**")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("定位方式", list(st.session_state.by_mapping.keys()), key="title_key")
        with col2:
            st.text_input("选择器", '//h1[contains(@class, "article-title")]',
                          key="title_column")

        # 内容元素
        st.write("**内容元素标签设置**")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("定位方式", list(st.session_state.by_mapping.keys()),
                         key="content_key")
        with col2:
            st.text_input("选择器", '//div[contains(@class, "article-viewer markdown-body")]',
                          key="content_column")

        # 图片元素
        st.write("**图片元素标签设置**")
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("定位方式", list(st.session_state.by_mapping.keys()), key="image_key")
        with col2:
            st.text_input("选择器", '//div[contains(@id, "article-root")]//img', key="image_column")


        st.session_state.key_words = False
        user_definition(url, driver_path, wait_time, time_sleep, headless, st.session_state.higher_requests)


    # 未勾选新闻页 - 未勾选高级筛选 - 勾选标签搜索
    elif st.session_state.tag_check:
        st.error("当前功能未开发")

        # col1, col2 = st.columns(2)
        # with col1:
        #     tag = st.text_input("标签")
        #     if tag.strip():
        #         st.session_state.main_tag = tag
        #         st.session_state.main_key_words = False
        # with col2:
        # st.session_state.main_element = st.text_input("元素(可选）")

    # 未勾选新闻页 - 未勾选高级筛选 - 未勾选标签搜索
    else:
        key_words(url, driver_path, wait_time, time_sleep, headless, st.session_state.higher_requests)


# -------------------------------用户自定义------------------------------------
def user_definition(url, driver_path, wait_time, time_sleep, headless, higher_requests):
    with st.expander("➕ 添加自定义字段", expanded=False):
        name = st.text_input("名称", help="比如：姓名/年龄 等").strip()
        field_type = st.selectbox("类型", ["文本", "数字", "图片", "网址", "链接"],
                                  help="当前需要爬取的类型")
        # st.write(f"你选择的字段类型是：{field_type}，类型是：{type(field_type)}")

        by = st.selectbox("定位方式", list(st.session_state.by_mapping.keys()), key=f"{name}_{field_type}")
        selector = st.text_input("选择器", '//td[contains(@class, "infobox-full-data")]')

        if st.button("确认"):

            if not name:
                st.warning("名称不能为空")
            elif any(f["name"] == name for f in st.session_state.custom_fields):
                st.warning("该名称已存在")
            else:
                st.session_state.custom_fields.append({
                    "name": name,
                    # 类型用在只有标签的情况下文本就text， 网址herf， 图片字符串
                    "type": field_type,
                    "by": by,
                    "selector": selector
                })

                st.success(f"成功添加：{name}")

        # 展示所有已添加的字段
    if st.session_state.custom_fields:
        for i, field in enumerate(st.session_state.custom_fields):
            st.markdown("### 📝 当前自定义字段")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                field["type"] = st.selectbox(f"{i + 1}.{name}", ["文本", "数字", "图片", "网址", "链接"],
                                             index=["文本", "数字", "图片", "网址", "链接"].index(
                                                 field["type"]), key=f"type_{i + 1}")

            with col2:
                field["by"] = st.selectbox(f"定位方式", list(st.session_state.by_mapping.keys()),
                                           key=f"{i + 1}_key")

            with col3:
                field["selector"] = st.text_input(f"选择器", value=field["selector"],
                                                  key=f"{i + 1}_column")

            with col4:
                if st.button("❌", key=f"delete_{i}"):
                    del st.session_state.custom_fields[i]
                    st.rerun()

    if st.button("清除所有自定义"):
        if st.session_state.custom_fields:
            st.session_state.custom_fields = []
            save_json()
            st.success("自定义清理成功")
            st.rerun()
        else:
            st.warning("没有配置文件需要删除")

    if not st.session_state.crawling:
        st.info("配置爬虫参数并点击'开始爬取'按钮")

    if st.button("开始爬取"):
        if url.strip():
            st.session_state.crawling = False
            # 开始按钮自动保存
            st.session_state.url = url
            st.session_state.driver_path = driver_path
            st.session_state.total_to_fetch = st.session_state.total_to_fetch
            st.session_state.wait_time = wait_time
            st.session_state.time_sleep = time_sleep
            st.session_state.headless = headless
            st.session_state.higher_requests = higher_requests
            save_json()
            do_crawling()


# ------------------------------关键词搜索-----------------------------------
def key_words(url, driver_path, wait_time, time_sleep, headless, higher_requests):
    st.session_state.main_key_words = st.selectbox("关键词", ["网址", "电话", "姓名", "年龄", "成就", "图片"],
                                                   help="通过关键词搜索该页信息", key="whole_research")

    if not st.session_state.crawling:
        st.info("配置爬虫参数并点击'开始爬取'按钮")

    if st.button("开始爬取"):
        if url.strip():
            if st.session_state.main_tag or st.session_state.main_key_words:
                st.session_state.crawling = False
                # 开始按钮自动保存
                st.session_state.url = url
                st.session_state.driver_path = driver_path
                st.session_state.total_to_fetch = st.session_state.total_to_fetch
                st.session_state.wait_time = wait_time
                st.session_state.time_sleep = time_sleep
                st.session_state.headless = headless
                st.session_state.higher_requests = False
                save_json()
                do_crawling()
            else:
                st.error("请输入正确标签形式")

        else:
            st.warning("url未填写")


# ------------------------------结果显示区域------------------------------------
def show_result():
    st.subheader("爬取结果")
    df = pd.DataFrame(st.session_state.final_content)

    st.dataframe(df)
    save_json()
    # get_url_name(st.session_state.url)

    # 下载按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        if st.download_button(
                label="下载Excel",
                data=output.getvalue(),
                file_name=get_url_name(st.session_state.url) + ".xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                help="如果新闻过大建议用csv文件保存",
        ):
            st.session_state.show_results = True
            st.session_state.crawling = True
            st.rerun()

    with col2:
        data_csv = pd.DataFrame(st.session_state.final_content).to_csv(index=False).encode('utf-8')
        if st.download_button(
                label="下载CSV",
                data=data_csv,
                file_name=get_url_name(st.session_state.url) + ".csv",
                mime='text/csv'
        ):
            st.session_state.show_results = True
            st.session_state.crawling = True
            st.rerun()

    with col3:
        with st.expander("储存数据库"):
            st.session_state.table_name = st.text_input("输入表格名称(新名创建，同名添加）", help="只能包含英文或数字")
            st.session_state.host = st.text_input("HOST","127.0.0.1")
            st.session_state.user = st.text_input("USER","root")
            st.session_state.password = st.text_input("PASSWORD", "20030716")
            st.session_state.database = st.text_input("DATABASE", "pages")
            st.session_state.port = st.text_input("PORT", "3306")

            if st.button("确定"):
                if st.session_state.table_name.strip():
                    data = st.session_state.final_content
                    schema = generate_table_schema(data)
                    # st.code(data)
                    # 数据库信息
                    create_table(table_name=st.session_state.table_name, schema=schema,
                                host=st.session_state.host,
                                user=st.session_state.user,
                                password=st.session_state.password,
                                database=st.session_state.database,
                                port=st.session_state.port)
                    insert_news(finial_content=st.session_state.final_content,
                                table_name=st.session_state.table_name,
                                host=st.session_state.host,
                                user=st.session_state.user,
                                password=st.session_state.password,
                                database=st.session_state.database,
                                port=st.session_state.port)

                    st.success(f"数据已保存到MySQL数据库表: {st.session_state.table_name}")
                    st.session_state.show_results = True
                    st.session_state.crawling = False
                else:
                    st.error("内容格式不正确")

    col1, col2 = st.columns(2)
    with col1:
        # 第一步：点击“重置”后，设置确认状态
        if st.button("重置", help="输入参数归为默认", key="reset"):
            st.session_state.confirm_reset = True

        # 第二步：如果正在确认重置，显示确认按钮
        if st.session_state.get("confirm_reset", False):
            st.warning("确定要清空所有参数吗？操作不可撤销")
            if st.button("确认清空", key="confirm_reset_button"):
                st.session_state.crawling = False
                st.session_state.show_results = False
                st.session_state.new_content = False
                st.session_state.higher_requests = False
                st.session_state.custom_fields = []
                delete_json()

                # 清除确认状态 & 重置
                st.session_state.confirm_reset = False
                st.rerun()

            # 可选：添加取消按钮
            if st.button("取消", key="cancel_reset"):
                st.session_state.confirm_reset = False

    with col2:
        if st.button("继续爬取", help="输入参数不变", key="continue"):
            st.session_state.crawling = False
            st.session_state.show_results = False
            st.rerun()


# --------------------------------主爬虫运行----------------------------
def do_crawling():
    options = Options()
    options.add_argument("--disable-features=EdgeChinaBrowsersImport")
    st.warning("爬取进行中，请稍候...")
    if st.session_state.headless:
        options.add_argument("--headless")
    service = EdgeService(executable_path=st.session_state.driver_path)
    driver = webdriver.Edge(service=service, options=options)

    # 是否新闻详情页，新闻详情页没有主元素
    if st.session_state.new_content:
        main_locator = ("", "")


        # 勾选新闻详情 - 未勾选爬取整页 - 是否勾选高级筛选
        if st.session_state.higher_requests:

            # 勾选新闻详情 - 未勾选爬取整页 - 勾选高级筛选
            crawler = WebCrawler(
                driver=driver,
                url=st.session_state.url,
                header=st.session_state.header_request,
                wait_time=st.session_state.wait_time,
                time_sleep=st.session_state.time_sleep,
                main_locator=main_locator,
                title_locator=(
                    st.session_state.by_mapping[st.session_state.title_key],
                    st.session_state.title_column
                ),
                content_locator=(
                    st.session_state.by_mapping[st.session_state.content_key],
                    st.session_state.content_column
                ),
                image_locator=(
                    st.session_state.by_mapping[st.session_state.image_key],
                    st.session_state.image_column
                ),
                total_need=st.session_state.total_to_fetch,
                custom_fields=st.session_state.custom_fields,
                main_tag=st.session_state.main_tag,
                main_key_words=st.session_state.main_key_words,
            )

            crawler.content()
            save_json()
            st.session_state.crawling = False
            st.session_state.show_results = True
            st.session_state.final_content = crawler.results

            # 勾选新闻详情 - 未勾选高级筛选 - 使用关键字
        elif st.session_state.main_key_words:

            crawler = WebCrawler(
                driver=driver,
                url=st.session_state.url,
                header=st.session_state.header_request,
                wait_time=st.session_state.wait_time,
                time_sleep=st.session_state.time_sleep,
                main_locator='',
                title_locator='',
                content_locator='',
                image_locator='',
                total_need='',
                custom_fields='',
                main_tag='',
                main_key_words=st.session_state.main_key_words,
            )

            crawler.zhengze_calculate()
            save_json()
            st.session_state.crawling = False
            st.session_state.show_results = True
            st.session_state.final_content = crawler.zhengze_text



    # 未勾选新闻详情 - 勾选高级筛选
    if not st.session_state.new_content:

        if st.session_state.higher_requests:
            crawler = WebCrawler(
                driver=driver,
                url=st.session_state.url,
                header=st.session_state.header_request,
                wait_time=st.session_state.wait_time,
                time_sleep=st.session_state.time_sleep,
                main_locator=(
                    st.session_state.by_mapping[st.session_state.main_key],
                    st.session_state.main_column
                ),
                title_locator=(
                    st.session_state.by_mapping[st.session_state.title_key],
                    st.session_state.title_column
                ),
                content_locator=(
                    st.session_state.by_mapping[st.session_state.content_key],
                    st.session_state.content_column
                ),
                image_locator=(
                    st.session_state.by_mapping[st.session_state.image_key],
                    st.session_state.image_column
                ),
                total_need=st.session_state.total_to_fetch,
                custom_fields=st.session_state.custom_fields,
                main_tag=st.session_state.main_tag,
                main_key_words=st.session_state.main_key_words,
            )

            crawler.result_()
            save_json()
            st.session_state.crawling = False
            st.session_state.show_results = True
            st.session_state.final_content = crawler.results

        # 未勾选新闻详情 - 未勾选高级筛选 - 未勾选标签搜索
        else:

            crawler = WebCrawler(
                driver=driver,
                url=st.session_state.url,
                header=st.session_state.header_request,
                wait_time=st.session_state.wait_time,
                time_sleep=st.session_state.time_sleep,
                main_locator='',
                title_locator=(
                    st.session_state.by_mapping[st.session_state.title_key],
                    st.session_state.title_column
                ),
                content_locator=(
                    st.session_state.by_mapping[st.session_state.content_key],
                    st.session_state.content_column
                ),
                image_locator=(
                    st.session_state.by_mapping[st.session_state.image_key],
                    st.session_state.image_column
                ),
                total_need=st.session_state.total_to_fetch,
                custom_fields=st.session_state.custom_fields,
                main_tag=st.session_state.main_tag,
                main_key_words=st.session_state.main_key_words,
            )

            st.write("正在爬取关键词...")
            crawler.zhengze_calculate()
            save_json()
            st.session_state.crawling = False
            st.session_state.show_results = True
            st.session_state.higher_requests = False
            st.session_state.final_content = crawler.zhengze_text


initial()