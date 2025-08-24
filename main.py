
import streamlit as st



if 'page' not in st.session_state:
    st.session_state.page = 'home'
if "dynamic" not in st.session_state:
    st.session_state.dynamic_obtain = True
if "static" not in st.session_state:
    st.session_state.static_obtain = True





# 页面导航
if st.session_state.page == 'home':

    st.title("🏠 欢迎页面")
    with st.expander("进入网页爬虫"):

        # if st.form_submit_button("传统页爬取", help="传统页介绍：\n 1.页面中有显示1、2、3页\n 2.网址不同子级分页的url不同"):
        #     st.session_state.static_obtain = True
        #     go_to()

        if st.button("动态页爬取"):
            from web_dynamic_files import web_dynamic

            web_dynamic.initial()


    if st.button("搜索数据库"):
        from web_research.web_research import web_research
        web_research.web_research()


