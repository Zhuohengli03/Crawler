import re

import streamlit as st
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from db_link_web import link_db
from db_write_web import insert_news


class web_research():
    def __init__(self):
        st.title("📊 MySQL 表格数据搜索")
        self.table = ""
        with st.expander("数据库参数(以下为默认参数，按需修改)"):
            self.host = st.text_input("HOST", "127.0.0.1")
            self.user = st.text_input("USER", "root")
            self.password = st.text_input("PASSWORD")
            self.database = st.text_input("DATABASE", "pages")
            self.port = st.text_input("PORT", "3306")
            self.research_content = ""
        self.UI()


    def UI(self):

        self.table = st.text_input("输入表名：", help="输入table名称")

        key_words = {
            "网址": "",
            "电话(+86)": "",
            "姓名": "",
            "邮箱": "",
            "国际电话": "",
            "图片": ""
        }
        self.research_content = st.selectbox("关键词", key_words,
                                        help="通过关键词搜索该页信息", key=f"key_select")

        if st.button("加载数据"):
            try:
                data = self.research_()
                st.dataframe(data)
            except Exception as e:
                st.error(f"出错了：{e}")



    def research_(self):

        key_map = {
            "网址": r'https?://[^\s<>"]+',
            "电话(+86)": r'(?:\+86)?[\s-]?1[3-9]\d{9}',
            "姓名": r'^[\u4e00-\u9fa5]{2,4}$',
            "邮箱": r'[\w\.]+@[\w]+\.[\w]{0,4}',
            "国际电话": r'\(?\+?[0-9]{1,3}\)?[\s-]?[0-9]{8}',
            "图片": r'https?://.*\.(jpg|png|jpeg|gif)'
        }

        conn = link_db(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

        if conn:
            st.success("正在搜索...")
            df = pd.read_sql(f"SELECT * FROM {self.table}", conn)
            # st.write(df)
            # 关键词所输出的正则模式
            pattern = key_map[self.research_content]

            # 输出结果
            final_results = []

            # 从HTML列来筛选出信息
            for HTML in df['HTML']:
                HTML = str(HTML)
                content_match = re.findall(pattern, HTML)
                # 去重
                content = set(content_match)
                final_results.append(content)

            # 将输出呈现为表格
            df[self.research_content] = final_results

            st.dataframe(df)



        if st.button("储存数据库"):
            insert_news(table_name=self.table,
                        schema="",
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database,
                        port=self.port,

                        )








web_research()