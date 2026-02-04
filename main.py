"""
动态网页爬虫 - 主入口 | Dynamic Web Crawler - Main Entry
"""
import streamlit as st
from i18n import t

# 页面配置
st.set_page_config(
    page_title="Dynamic Web Crawler",
    page_icon="🕷️",
    layout="wide"
)

# 初始化状态
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'lang' not in st.session_state:
    st.session_state.lang = 'zh'


def go_home():
    """返回主页"""
    st.session_state.page = 'home'


def go_dynamic():
    """进入动态爬虫页面"""
    st.session_state.page = 'dynamic'


def go_research():
    """进入数据库搜索页面"""
    st.session_state.page = 'research'


def switch_language():
    """切换语言"""
    st.session_state.lang = 'en' if st.session_state.lang == 'zh' else 'zh'


# ==================== 侧边栏 - 语言切换 ====================
with st.sidebar:
    st.markdown("### " + t("language", st.session_state.lang))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇨🇳 中文", 
                     key="lang_zh",
                     use_container_width=True,
                     type="primary" if st.session_state.lang == "zh" else "secondary"):
            st.session_state.lang = "zh"
            st.rerun()
    with col2:
        if st.button("🇺🇸 English", 
                     key="lang_en",
                     use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
    
    st.markdown("---")
    
    # 显示当前页面
    page_names = {
        "home": "🏠 " + ("主页" if st.session_state.lang == "zh" else "Home"),
        "dynamic": "🔍 " + ("动态爬虫" if st.session_state.lang == "zh" else "Dynamic Crawler"),
        "research": "📊 " + ("数据库搜索" if st.session_state.lang == "zh" else "Database Search")
    }
    st.info(page_names.get(st.session_state.page, "Unknown"))


# ==================== 页面路由 ====================
lang = st.session_state.lang

if st.session_state.page == 'home':
    # 主页
    st.title(t("welcome", lang))
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t("web_crawler", lang))
        st.write(t("crawler_desc", lang))
        if st.button(t("enter_dynamic", lang), key="btn_dynamic", use_container_width=True):
            go_dynamic()
            st.rerun()
    
    with col2:
        st.subheader(t("db_search", lang))
        st.write(t("db_search_desc", lang))
        if st.button(t("enter_search", lang), key="btn_research", use_container_width=True):
            go_research()
            st.rerun()

elif st.session_state.page == 'dynamic':
    # 动态爬虫页面
    if st.button(t("back_home", lang), key="back_from_dynamic"):
        go_home()
        st.rerun()
    
    st.markdown("---")
    
    # 导入并运行动态爬虫模块
    from web_dynamic_files import web_dynamic
    web_dynamic.initial()

elif st.session_state.page == 'research':
    # 数据库搜索页面
    if st.button(t("back_home", lang), key="back_from_research"):
        go_home()
        st.rerun()
    
    st.markdown("---")
    
    # 导入并运行数据库搜索模块
    from web_research.web_research import web_research
    web_research()
