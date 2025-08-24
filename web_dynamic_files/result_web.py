import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v136.dom import get_attributes
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import re


class WebCrawler:
    def __init__(self, driver, url, wait_time, time_sleep,
                 main_locator, title_locator, content_locator, image_locator, total_need, custom_fields, main_key_words,
                 header, main_tag, main_url_key_words, main_url_key_elements, higher_requests):
        self.driver = driver
        self.url = url
        self.wait_time = wait_time
        self.time_sleep = time_sleep
        self.main_locator = main_locator
        self.title_locator = title_locator
        self.content_locator = content_locator
        self.image_locator = image_locator
        self.total_need = total_need
        self.main_key_words  = main_key_words
        self.main_tag = main_tag
        self.main_url_key_words = main_url_key_words
        self.header = header
        self.main_url_key_elements = main_url_key_elements
        self.higher_requests = higher_requests
        # 页面元素
        # 在新闻列表收集到的新闻详情页url
        self.collected_urls = []

        self.results = []
        # 自定义详情
        self.custom_fields = custom_fields
        # 正则输出信息
        self.zhengze_text = []

    # 高级筛选未勾选新闻详情页
    def result_(self):

        try:
            self.driver.get(self.url)
            # 是否有高级选项
            if  not self.higher_requests:
                select_1 = re.findall(r'.+(?==)', f'{self.main_url_key_elements}')[0]
                select_2 = re.findall(r'(?<=")[^"]*(?=")', f'{self.main_url_key_elements}')[0]

                if not select_2:
                    st.error("元素格式有误,请重新输入")

                else:
                    page_source = self.driver.page_source
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]"))
                    )

                    st.write(f"正在打开{self.url}")

                    # 获取新闻通用单链
                    if self.main_key_words:
                        elements = self.driver.find_elements(By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]")
                        total_available = len(elements)
                        st.success(f"按元素查找成功，当前页面共{total_available}条")
                        if self.total_need > total_available:
                            self.scroll_and_collect()
                        else:
                            self.collect()

                    else:
                        st.warning("关键词格式有误，请重新输入")


            else:
                # 勾选按高级选项
                page_source = self.driver.page_source
                WebDriverWait(self.driver, self.wait_time).until(
                    EC.presence_of_element_located(self.main_locator)
                )

                # 原始页面元素
                elements = self.driver.find_elements(*self.main_locator)
                total_available = len(elements)
                st.success(f"按元素查找成功，当前页面共{total_available}条")
                if self.total_need > total_available:
                    self.scroll_and_collect()
                else:
                    self.collect()


        except Exception as e:
            st.error(e)
        finally:
            self.driver.close()

    def scroll_and_collect(self):
        y = 0
        while len(self.collected_urls) < self.total_need:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.time_sleep)
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located(self.main_locator)
            )
            y += 1
            st.write(f"下拉次数: {y}")

            st.success(f"下拉后页面共 {len(self.driver.find_elements(*self.main_locator))} 条")
            self.collect()



    def collect(self):
        page_source = self.driver.page_source
        if not self.higher_requests:
            # 未勾选高级选项（关键词）
            select_1 = re.findall(r'.+(?==)', f'{self.main_url_key_elements}')[0]
            select_2 = re.findall(r'(?<=")[^"]*(?=")', f'{self.main_url_key_elements}')[0]
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]"))
            )

            if self.main_key_words:
                all_elements = self.driver.find_elements(By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]")
                zhengze_list = []
                # Fix: iterate over all_elements, not a single element by index
                for element in all_elements[:self.total_need]:
                    zhengze_url = element.get_attribute("href")
                    zhengze_list.append(zhengze_url)

                # Fix: iterate over zhengze_list, not a single element by index
                for url in zhengze_list:
                    hurl = urljoin(self.url, url)
                    self.zhengze_calculate(hurl)



        # 勾选高级选项
        else:
            # 获取当前页面所有元素
            all_elements = self.driver.find_elements(*self.main_locator)

            if all_elements:
            # 遍历所有元素,获得题目链接
                if len(self.collected_urls) < self.total_need:

                    for text in all_elements:
                        content_url = text.get_attribute("href")
                        # 循环次数小于需求次数 且 之前没有储存过的元素时 储存
                        if  content_url not in self.collected_urls and len(self.collected_urls) < self.total_need:
                            self.collected_urls.append(content_url)

                            st.write(f"当前已获取: {len(self.collected_urls)} 条")

                self.content()

            else:
                st.error("当前页面未找到指定元素")



    def content(self):
        # 新闻详情页 未勾选高级筛选
        if len(self.collected_urls) > 1:
            i = 0
            st.write("正在依次进入url中...")
            for sin_url in self.collected_urls:
                final_content = {"title": "", "url": sin_url, "content": "", "image": "", "HTML": ""}
                # 识别当前第几条，并在没有值时弹出提示
                i += 1
                self.driver.get(sin_url)
                # 防止进入太快元素没加载出来
                time.sleep(self.time_sleep)
                # 获取HTML信息
                page = self.driver.page_source
                content = BeautifulSoup(page, "lxml")
                final_content["HTML"] = str(content)

                # 根据title元素爬取title
                title_element = self.driver.find_elements(*self.title_locator)
                if title_element:
                    # st.success( "发现title元素")
                    for titles in title_element:
                        if titles:
                            title_content = titles.text
                            # st.write(content_text)
                            final_content["title"] = title_content
                else:
                    st.warning(f"第 {i} 条未发现title元素")

                # 根据内容元素爬取内容
                content_element = self.driver.find_elements(*self.content_locator)
                if content_element:
                    # st.success( "发现content元素")

                    for contents in content_element:
                        if contents:
                            content_text = contents.text
                            # st.write(content_text)
                            final_content["content"] = content_text
                    # st.write("内容获取成功")
                else:
                    st.warning(f"第 {i} 条未发现content元素")

                # 根据图片元素爬取图片url
                img_urls = []
                img_element = self.driver.find_elements(*self.image_locator)
                if img_element:
                    # st.success("发现image元素")
                    for src in img_element:
                        if src:
                            img_url = src.get_attribute("src")
                            img_urls.append(img_url)
                    final_content["image"] = "\n".join(img_urls)
                else:
                    st.warning(f"第 {i} 条未发现image元素")




                custom_result = self.custom_()

                if custom_result:
                    final_content.update(custom_result)
                    self.results.append(final_content)
                else:
                    self.results.append(final_content)


            st.write("爬取完成")

            return self.results

        # 新闻详情页 勾选高级筛选
        else:
            st.write(f"正在进入{self.url}")
            final_content = {"title": "", "url": self.url, "content": "", "image": "", "HTML": ""}
            self.driver.get(self.url, headers=self.header)
            # 获取HTML信息
            page = self.driver.page_source
            content = BeautifulSoup(page, "lxml")
            final_content["HTML"] = str(content)

            # 根据title元素爬取title
            title_element = self.driver.find_elements(*self.title_locator)
            if title_element:
                for titles in title_element:
                    if titles:
                        title_content = titles.text
                        # st.write(titles)
                        final_content["title"] = title_content
            else:
                st.warning("当前页面未发现title元素")

            # 根据内容元素爬取内容
            content_element = self.driver.find_elements(*self.content_locator)
            if content_element:
                for contents in content_element:
                    if contents:
                        content_text = contents.text

                        final_content["content"] = content_text
            else:
                st.warning("当前页面未发现content元素")


            # 根据图片元素爬取图片url
            img_urls = []
            img_element = self.driver.find_elements(*self.image_locator)
            if img_element:
                for src in img_element:
                    if src:
                        img_url = src.get_attribute("src")
                        img_urls.append(img_url)
            else:
                 st.warning("当前页面未发现image元素")
            final_content["image"] = "\n".join(img_urls)

            custom_result = self.custom_()
            if custom_result:
                final_content.update(custom_result)
                self.results.append(final_content)
            else:
                self.results.append(final_content)
        st.write("爬取完成")
        return self.results

        # 用户有是否有自定义

    def custom_(self):
        st.session_state.by_mapping = {
            "XPATH": By.XPATH,
            "CSS选择器": By.CSS_SELECTOR,
            "ID": By.ID,
            "CLASS": By.CLASS_NAME,
            "TAG": By.TAG_NAME
        }
        i = 0
        custom_Data = {}
        # 如果自定义有内容
        for field in self.custom_fields:
            type = field.get("type")
            name = field.get("name")
            custom_data = {name: ""}
            by = field.get("by")
            by_locator = st.session_state.by_mapping[by]
            locator = field.get("selector")
            i += 1
            elements = self.driver.find_elements(by_locator, locator)
            if elements:
                # st.success(f"成功找到 {field["type"]} 元素")
                if type in ["文本"]:
                    content = []
                    for element in elements:
                        if element:
                            text = element.text.strip()
                            content.append(text)
                    custom_data[name] = "\n ".join(content)

                elif type in ["链接" or "网址"]:
                    for element in elements:
                        link = element.get_attribute("href")
                        custom_data[name] = link

                elif type == "图片":
                    for element in elements:
                        link = element.get_attribute("src")
                        custom_data[name] = link


            else:
                st.warning(f"第 {i} 条无 {field["type"]} 元素")

            custom_Data.update(custom_data)
        return custom_Data


    # 关键词（正则算法）
    def zhengze_calculate(self, hurl):

        time.sleep(self.time_sleep)
        if hurl:
            self.url = hurl
            self.driver.get(self.url)
        else:
            self.driver.get(self.url)

        page = self.driver.page_source
        content = BeautifulSoup(page, "lxml")

        zhengze_content = {
            "URL":self.url,
        }
        key_words = self.main_key_words
        pattern_map = {
            "网址": r'https?://[^\s<>"]+',
            "电话": r'\b(?:\+[()\d]{2,3})?1\d{10}\b|\b(?:\d{3}[-\s]){3}\b',
            "邮箱": r'[\w\.]+@[\w]+\.[\w]{0,4}',
            "年龄": r'^(?:120|1[01][0-9]|[1-9][0-9]?|[1-9])$',
            "图片": r'<img.*?src="([^"]+)[.jpg|.png|.gif|.image]*"',
        # 可扩展其它关键词及对应正则
        }

        if key_words in pattern_map:
            matches = re.findall(pattern_map[key_words], str(content))

            if matches:
                results = set([f"{m}" for m in matches])
                zhengze_content[key_words] = "\n".join(results)
            else:
                zhengze_content[key_words] = f"未找到匹配内容"


        self.zhengze_text.append(zhengze_content)

