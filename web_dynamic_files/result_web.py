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
            # Check driver health before starting
            if not self._check_driver_health():
                st.error("WebDriver状态异常，无法继续")
                return
            
            self.driver.get(self.url)
            # 是否有高级选项
            if  not self.higher_requests:
                select_1 = re.findall(r'.+(?==)', f'{self.main_url_key_elements}')[0]
                select_2 = re.findall(r'(?<=")[^"]*(?=")', f'{self.main_url_key_elements}')[0]

                if not select_2:
                    st.error("元素格式有误,请重新输入")

                else:
                    page_source = self.driver.page_source
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]"))
                        )
                    except Exception as e:
                        st.error(f"等待页面元素加载失败: {e}")
                        return

                    st.write(f"正在打开{self.url}")

                    # 获取新闻通用单链
                    if self.main_key_words:
                        try:
                            elements = self.driver.find_elements(By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]")
                            total_available = len(elements)
                            st.success(f"按元素查找成功，当前页面共{total_available}条")
                            
                            # Simple logic: if user needs more than available, scroll and collect
                            if self.total_need > total_available:
                                st.info(f"用户需要 {self.total_need} 条，当前页面只有 {total_available} 条，开始滚动加载更多内容...")
                                self.scroll_and_collect()
                            else:
                                st.info(f"用户需要 {self.total_need} 条，当前页面已有 {total_available} 条，直接收集...")
                                self.collect()
                        except Exception as e:
                            st.error(f"查找页面元素失败: {e}")
                            return

                    else:
                        st.warning("关键词格式有误，请重新输入")


            else:
                # 勾选按高级选项
                page_source = self.driver.page_source
                try:
                    WebDriverWait(self.driver, self.wait_time).until(
                        EC.presence_of_element_located(self.main_locator)
                    )
                except Exception as e:
                    st.error(f"等待页面元素加载失败: {e}")
                    return

                # 原始页面元素
                try:
                    elements = self.driver.find_elements(*self.main_locator)
                    total_available = len(elements)
                    st.success(f"按元素查找成功，当前页面共{total_available}条")
                    
                    # Simple logic: if user needs more than available, scroll and collect
                    if self.total_need > total_available:
                        st.info(f"用户需要 {self.total_need} 条，当前页面只有 {total_available} 条，开始滚动加载更多内容...")
                        self.scroll_and_collect()
                    else:
                        st.info(f"用户需要 {self.total_need} 条，当前页面已有 {total_available} 条，直接收集...")
                        self.collect()
                except Exception as e:
                    st.error(f"查找页面元素失败: {e}")
                    return


        except Exception as e:
            st.error(f"页面加载或元素查找失败: {e}")
        finally:
            try:
                self.driver.close()
            except:
                pass
    
    def _check_driver_health(self):
        """检查WebDriver是否健康"""
        try:
            # Try to get current URL to check if driver is responsive
            self.driver.current_url
            return True
        except:
            return False
    
    def _check_page_responsiveness(self):
        """检查页面是否仍然响应"""
        try:
            # Try to execute a simple JavaScript command
            self.driver.execute_script("return document.readyState")
            return True
        except Exception as e:
            st.warning(f"页面响应检查失败: {e}")
            return False
    
    def _safe_find_elements(self, locator):
        """安全地查找元素，防止WebDriver崩溃"""
        try:
            if self._check_page_responsiveness():
                return self.driver.find_elements(*locator)
            else:
                st.warning("页面无响应，跳过元素查找")
                return []
        except Exception as e:
            st.warning(f"查找元素时出现错误: {e}")
            return []

    def scroll_and_collect(self):
        y = 0
        max_scroll_attempts = 20  # Reduced max attempts
        previous_count = 0
        
        st.info("开始滚动收集内容...")
        
        while len(self.collected_urls) < self.total_need and y < max_scroll_attempts:
            try:
                # Check if driver is still responsive
                if not self._check_driver_health():
                    st.error("WebDriver已断开连接，尝试重新启动...")
                    if not self._restart_driver():
                        st.error("无法重新启动WebDriver，停止滚动")
                        break
                
                # Simple scroll to bottom
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    st.write(f"滚动到页面底部 (第 {y + 1} 次)")
                    time.sleep(self.time_sleep)  # Wait for content to load
                except Exception as e:
                    st.warning(f"滚动失败: {e}")
                    continue
                
                y += 1
                
                # Wait for new elements to load and check progress
                try:
                    # Try to find elements using the appropriate locator based on mode
                    if not self.higher_requests:
                        # For keyword mode, use the keyword-based locator
                        select_1 = re.findall(r'.+(?==)', f'{self.main_url_key_elements}')[0]
                        select_2 = re.findall(r'(?<=")[^"]*(?=")', f'{self.main_url_key_elements}')[0]
                        current_elements = self.driver.find_elements(
                            By.XPATH, 
                            f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]"
                        )
                    else:
                        # For advanced mode, use the main locator
                        current_elements = self._safe_find_elements(self.main_locator)
                    
                    st.write(f"滚动后页面共 {len(current_elements)} 条")
                    
                    # Check if we're making progress
                    if len(current_elements) == previous_count:
                        st.warning("本次滚动无新内容")
                        if y >= 3:  # If no progress for 3 consecutive scrolls
                            st.warning("连续3次滚动无新内容，停止滚动")
                            break
                    else:
                        st.success(f"发现新内容！元素数量: {previous_count} -> {len(current_elements)}")
                        previous_count = len(current_elements)
                        
                except Exception as e:
                    st.warning(f"获取元素数量失败: {e}")
                    current_elements = []
                
                # Collect URLs from current view
                try:
                    st.write("开始收集URL...")
                    self.collect()
                    st.write(f"当前已收集: {len(self.collected_urls)} 个URL")
                    
                    # If we have enough URLs, stop scrolling
                    if len(self.collected_urls) >= self.total_need:
                        st.success(f"已收集足够的URL ({len(self.collected_urls)}/{self.total_need})")
                        break
                        
                except Exception as e:
                    st.error(f"收集URL时出现错误: {e}")
                    continue
                
                # Add a small delay to prevent overwhelming the page
                time.sleep(1)
                
            except Exception as e:
                st.error(f"滚动过程中出现错误: {e}")
                y += 1
                continue
        
        if y >= max_scroll_attempts:
            st.warning(f"已达到最大滚动次数 ({max_scroll_attempts})，停止滚动")
        
        st.info(f"滚动完成，总共收集到 {len(self.collected_urls)} 个URL")
    
    def _restart_driver(self):
        """尝试重新启动WebDriver"""
        try:
            # Close current driver
            try:
                self.driver.quit()
            except:
                pass
            
            # Wait a moment
            time.sleep(2)
            
            # Import and recreate driver
            from selenium import webdriver
            from selenium.webdriver.edge.service import Service as EdgeService
            from selenium.webdriver.edge.options import Options
            
            options = Options()
            options.add_argument("--disable-features=EdgeChinaBrowsersImport")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--disable-javascript")
            options.add_argument("--disable-web-security")
            options.add_argument("--memory-pressure-off")
            options.add_argument("--max_old_space_size=4096")
            
            # Get driver path from session state
            import streamlit as st
            driver_path = getattr(st.session_state, 'driver_path', None)
            
            if driver_path:
                service = EdgeService(executable_path=driver_path)
                self.driver = webdriver.Edge(service=service, options=options)
                self.driver.set_page_load_timeout(30)
                self.driver.implicitly_wait(10)
                self.driver.set_script_timeout(30)
                
                # Navigate back to original URL
                self.driver.get(self.url)
                time.sleep(2)
                return True
            else:
                st.error("无法获取driver路径，无法重新启动")
                return False
                
        except Exception as e:
            st.error(f"重新启动WebDriver失败: {e}")
            return False


    def collect(self):
        try:
            st.write("=== 开始收集URL ===")
            
            # Check driver health before collecting
            if not self._check_driver_health():
                st.error("WebDriver状态异常，停止收集")
                return
            
            # Get current page info for debugging
            try:
                current_url = self.driver.current_url
                page_title = self.driver.title
                st.write(f"当前页面: {current_url}")
                st.write(f"页面标题: {page_title}")
            except Exception as e:
                st.warning(f"获取页面信息失败: {e}")
            
            if not self.higher_requests:
                # 未勾选高级选项（关键词）
                try:
                    st.write("使用关键词模式收集...")
                    select_1 = re.findall(r'.+(?==)', f'{self.main_url_key_elements}')[0]
                    select_2 = re.findall(r'(?<=")[^"]*(?=")', f'{self.main_url_key_elements}')[0]
                    
                    st.write(f"元素选择器: {select_1}={select_2}")
                    st.write(f"关键词元素: {self.main_url_key_words}")
                    
                    # Check driver health before waiting
                    if not self._check_driver_health():
                        st.error("WebDriver状态异常，停止收集")
                        return
                    
                    # Wait for elements with better error handling
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]"))
                        )
                        st.success("找到目标元素，开始收集")
                    except Exception as e:
                        st.error(f"等待元素超时: {e}")
                        # Try to find any elements anyway
                        st.write("尝试查找现有元素...")

                    if self.main_key_words:
                        # Try to find elements
                        xpath_query = f"//{self.main_url_key_words}[contains(@{select_1}, '{select_2}')]"
                        st.write(f"执行XPath查询: {xpath_query}")
                        
                        all_elements = self.driver.find_elements(By.XPATH, xpath_query)
                        st.write(f"找到 {len(all_elements)} 个元素")
                        
                        if len(all_elements) == 0:
                            st.warning("未找到任何元素，可能的原因:")
                            st.write("1. 元素选择器不正确")
                            st.write("2. 页面结构发生变化")
                            st.write("3. 内容需要更多时间加载")
                            
                            # Try alternative approach - find any elements with the tag
                            st.write("尝试查找所有相同标签的元素...")
                            alternative_elements = self.driver.find_elements(By.TAG_NAME, self.main_url_key_words)
                            st.write(f"找到 {len(alternative_elements)} 个 {self.main_url_key_words} 标签元素")
                            
                            if len(alternative_elements) > 0:
                                st.info("建议检查元素选择器格式")
                                return
                            else:
                                st.error("未找到任何元素，无法继续收集")
                                return
                        
                        # Collect URLs from elements that we haven't collected yet
                        zhengze_list = []
                        for i, element in enumerate(all_elements):
                            try:
                                zhengze_url = element.get_attribute("href")
                                if zhengze_url and zhengze_url not in self.collected_urls:
                                    zhengze_list.append(zhengze_url)
                                    # Only show progress every 10 URLs or at the end
                                    if len(zhengze_list) % 10 == 0 or i == len(all_elements) - 1:
                                        st.write(f"已收集 {len(zhengze_list)} 个新URL")
                                    
                                    # Stop if we have enough
                                    if len(self.collected_urls) + len(zhengze_list) >= self.total_need:
                                        break
                                else:
                                    if zhengze_url:
                                        st.write(f"跳过重复URL: {zhengze_url[:50]}...")
                            except Exception as e:
                                st.warning(f"获取元素 {i+1} href属性失败: {e}")
                                continue

                        st.write(f"本次收集到 {len(zhengze_list)} 个新URL")
                        
                        # Process the new URLs
                        for i, url in enumerate(zhengze_list):
                            try:
                                hurl = urljoin(self.url, url)
                                # Only show progress every 10 URLs or at the end
                                if (i + 1) % 10 == 0 or i == len(zhengze_list) - 1:
                                    st.write(f"正在处理URL {i + 1}/{len(zhengze_list)}")
                                self.zhengze_calculate(hurl)
                                # Add to collected URLs
                                self.collected_urls.append(url)
                            except Exception as e:
                                st.warning(f"处理URL {i+1} 失败: {e}")
                                continue
                                
                except Exception as e:
                    st.error(f"处理关键词模式时出现错误: {e}")
                    return

            # 勾选高级选项
            else:
                st.write("使用高级选项模式收集...")
                # 获取当前页面所有元素
                try:
                    st.write(f"主元素定位器: {self.main_locator}")
                    all_elements = self.driver.find_elements(*self.main_locator)

                    st.write(f"找到 {len(all_elements)} 个主元素")

                    if all_elements:
                        # 遍历所有元素,获得题目链接
                        new_urls_collected = 0
                        for i, text in enumerate(all_elements):
                            try:
                                content_url = text.get_attribute("href")
                                # 循环次数小于需求次数 且 之前没有储存过的元素时 储存
                                if content_url and content_url not in self.collected_urls and len(self.collected_urls) < self.total_need:
                                    self.collected_urls.append(content_url)
                                    new_urls_collected += 1
                                    # Only show progress every 10 URLs or at the end
                                    if new_urls_collected % 10 == 0 or new_urls_collected == self.total_need - len(self.collected_urls) + new_urls_collected:
                                        st.write(f"已收集 {len(self.collected_urls)} 个URL (本次新增 {new_urls_collected} 个)")
                                    
                                    # Stop if we have enough
                                    if len(self.collected_urls) >= self.total_need:
                                        break
                            except Exception as e:
                                st.warning(f"获取元素 {i+1} href属性失败: {e}")
                                continue

                        st.write(f"本次新增收集 {new_urls_collected} 个URL，总共 {len(self.collected_urls)} 个")
                        
                        # If we have enough URLs, process content
                        if len(self.collected_urls) >= self.total_need:
                            st.write(f"当前已收集 {len(self.collected_urls)} 个URL，开始处理内容...")
                            self.content()

                    else:
                        st.error("当前页面未找到指定元素")
                        st.write("可能的原因:")
                        st.write("1. 元素选择器不正确")
                        st.write("2. 页面结构发生变化")
                        st.write("3. 内容需要更多时间加载")
                        
                        # Try to find any elements for debugging
                        st.write("尝试查找页面上的所有链接...")
                        all_links = self.driver.find_elements(By.TAG_NAME, "a")
                        st.write(f"页面共有 {len(all_links)} 个链接元素")
                        
                        if len(all_links) > 0:
                            st.write("前5个链接:")
                            for i, link in enumerate(all_links[:5]):
                                try:
                                    href = link.get_attribute("href")
                                    text = link.text[:30] if link.text else "无文本"
                                    st.write(f"  {i+1}. {text} -> {href}")
                                except:
                                    st.write(f"  {i+1}. 无法获取链接信息")
                        
                except Exception as e:
                    st.error(f"收集高级选项元素时出现错误: {e}")
                    return
                    
        except Exception as e:
            st.error(f"收集过程中出现错误: {e}")
        finally:
            # Force garbage collection to free memory
            import gc
            gc.collect()
            st.write("=== 收集完成 ===")


    def content(self):
        # 新闻详情页 未勾选高级筛选
        if len(self.collected_urls) > 1:
            i = 0
            st.write("正在依次进入url中...")
            for sin_url in self.collected_urls:
                try:
                    final_content = {"title": "", "url": sin_url, "content": "", "image": "", "HTML": ""}
                    # 识别当前第几条，并在没有值时弹出提示
                    i += 1
                    # Only show progress every 10 URLs or at the end
                    if i % 10 == 0 or i == len(self.collected_urls):
                        st.write(f"正在处理第 {i}/{len(self.collected_urls)} 个URL")
                    
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
                        
                except Exception as e:
                    st.error(f"处理第 {i} 个URL时出现错误: {e}")
                    # Continue with next URL instead of crashing
                    continue

            st.write("爬取完成")

            return self.results

        # 新闻详情页 勾选高级筛选
        else:
            try:
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
                    
            except Exception as e:
                st.error(f"处理页面时出现错误: {e}")
                
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

