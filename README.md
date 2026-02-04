# 🕷️ 动态网页爬虫工具 | Dynamic Web Crawler

一个基于 **Streamlit** 和 **Selenium** 的动态网页爬虫工具，支持无限滚动加载页面的数据抓取，并可将数据存储至 MySQL 数据库。

A dynamic web crawler built with **Streamlit** and **Selenium**, supporting infinite scroll pages and MySQL database storage.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.33+-green.svg)

---

## ✨ 功能特性 | Features

### 🔍 爬虫功能 | Crawler Functions

| 中文 | English |
|------|---------|
| 动态页面爬取：支持无刷加载网页（如今日头条、稀土掘金等） | Dynamic page crawling: Supports infinite scroll pages (e.g., Toutiao, Juejin) |
| 新闻详情页爬取：可直接爬取单个新闻详情页面 | Detail page crawling: Directly scrape individual article pages |
| 智能滚动加载：自动滚动页面以加载更多内容 | Smart scroll loading: Automatically scroll to load more content |
| 自定义字段提取：支持添加自定义字段（文本、图片、网址、链接） | Custom field extraction: Support text, image, URL, and link fields |

### 🎯 元素定位方式 | Element Locators

| 中文 | English |
|------|---------|
| 高级筛选模式：通过 XPath、CSS选择器、ID、CLASS、TAG 精确定位 | Advanced mode: Precise targeting via XPath, CSS Selector, ID, CLASS, TAG |
| 关键词模式：通过正则表达式自动提取网址、电话、邮箱、图片等 | Keyword mode: Auto-extract URLs, phones, emails, images via regex |

### 💾 数据导出 | Data Export

| 中文 | English |
|------|---------|
| 导出为 Excel 文件 (.xlsx) | Export to Excel (.xlsx) |
| 导出为 CSV 文件 | Export to CSV |
| 存储至 MySQL 数据库 | Store to MySQL database |

### 🔎 数据库搜索 | Database Search

| 中文 | English |
|------|---------|
| 支持从已爬取的数据中按关键词搜索 | Search crawled data by keywords |
| 支持正则匹配：网址、电话、姓名、邮箱、图片 | Regex matching: URLs, phones, names, emails, images |

---

## 📦 安装 | Installation

### 1. 克隆项目 | Clone Repository
```bash
git clone <repository-url>
cd Crawler_c
```

### 2. 创建虚拟环境 | Create Virtual Environment
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

### 3. 安装依赖 | Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. 下载 Edge WebDriver | Download Edge WebDriver

| 中文 | English |
|------|---------|
| 访问 Microsoft Edge WebDriver 官网 | Visit Microsoft Edge WebDriver website |
| 下载与你的 Edge 浏览器版本匹配的 WebDriver | Download WebDriver matching your Edge browser version |
| 记录 WebDriver 的路径 | Note the WebDriver path |

🔗 [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

---

## 🚀 使用方法 | Usage

### 启动应用 | Start Application
```bash
streamlit run main.py
```

### 基本配置 | Basic Configuration

| 参数 Parameter | 中文说明 | English Description |
|----------------|----------|---------------------|
| 目标URL | 输入要爬取的网页地址 | Enter the target webpage URL |
| Edge驱动路径 | 设置 WebDriver 的本地路径 | Set local WebDriver path |
| 等待时间 | 页面元素加载等待时间（建议 20-50 秒） | Element load wait time (recommended 20-50s) |
| 间隔时间 | 请求间隔（建议 ≥0.5 秒） | Request interval (recommended ≥0.5s) |
| 无窗口模式 | 后台运行浏览器 | Run browser in background |

### 爬取模式 | Crawling Modes

#### 模式一：关键词模式（简单） | Mode 1: Keyword Mode (Simple)

| 步骤 Step | 中文 | English |
|-----------|------|---------|
| 1 | 输入单条新闻的 HTML 标签（如 `a`、`div`） | Enter HTML tag for news items (e.g., `a`, `div`) |
| 2 | 输入关键元素（如 `class="title"`） | Enter key attribute (e.g., `class="title"`) |
| 3 | 选择要提取的关键词类型（网址/电话/邮箱/图片） | Select extraction type (URL/phone/email/image) |

#### 模式二：高级筛选模式（精确） | Mode 2: Advanced Mode (Precise)

| 步骤 Step | 中文 | English |
|-----------|------|---------|
| 1 | 勾选"高级筛选" | Check "Advanced Filter" |
| 2 | 设置新闻URL标签（用于定位新闻列表） | Set news URL locator (for news list) |
| 3 | 设置标题、内容、图片元素的定位器 | Set locators for title, content, image |
| 4 | 可添加自定义字段 | Add custom fields (optional) |

### 结果处理 | Result Handling

| 中文 | English |
|------|---------|
| 爬取完成后可预览数据表格 | Preview data table after crawling |
| 下载 Excel 或 CSV 文件 | Download Excel or CSV file |
| 配置 MySQL 连接信息后存储到数据库 | Store to database with MySQL config |

---

## 📁 项目结构 | Project Structure

```
Crawler_c/
├── main.py                    # 主入口 | Main entry
├── requirements.txt           # 依赖 | Dependencies
├── README.md                  # 文档 | Documentation
├── web_dynamic_files/         # 动态爬虫模块 | Dynamic crawler module
│   ├── web_dynamic.py         # 爬虫 UI | Crawler UI logic
│   ├── result_web.py          # 爬虫核心类 | WebCrawler core class
│   ├── db_link_web.py         # 数据库连接 | Database connection
│   └── db_write_web.py        # 数据库写入 | Database write
└── web_research/              # 搜索模块 | Search module
    ├── web_research.py        # 搜索 UI | Search UI
    ├── db_link_web.py         # 数据库连接 | Database connection
    └── db_write_web.py        # 数据库写入 | Database write
```

---

## ⚙️ 配置说明 | Configuration

### 数据库配置 | Database Configuration (MySQL)

| 参数 Parameter | 默认值 Default | 中文说明 | English |
|----------------|----------------|----------|---------|
| HOST | 127.0.0.1 | 数据库主机地址 | Database host |
| PORT | 3306 | 端口号 | Port number |
| USER | root | 用户名 | Username |
| PASSWORD | - | 密码 | Password |
| DATABASE | pages | 数据库名 | Database name |

### 爬虫配置 | Crawler Configuration

| 参数 Parameter | 建议值 Recommended | 中文说明 | English |
|----------------|-------------------|----------|---------|
| 等待时间 Wait Time | 20-50秒 | 动态少的页面设置较短 | Shorter for less dynamic pages |
| 间隔时间 Interval | ≥0.5秒 | 避免请求过快触发反爬 | Prevent anti-crawler detection |
| 爬取数量 Count | 根据需要 | 实际可能受页面限制 | May be limited by page |

---

## 🛠️ 技术栈 | Tech Stack

| 技术 Technology | 用途 | Purpose |
|-----------------|------|---------|
| **Streamlit** | Web UI 框架 | Web UI framework |
| **Selenium** | 浏览器自动化 | Browser automation |
| **BeautifulSoup** | HTML 解析 | HTML parsing |
| **Pandas** | 数据处理 | Data processing |
| **MySQL Connector** | 数据库连接 | Database connection |
| **lxml** | XML/HTML 解析器 | XML/HTML parser |

---

## ⚠️ 注意事项 | Important Notes

| 中文 | English |
|------|---------|
| **反爬机制**：部分网站有反爬保护，请合理设置请求间隔 | **Anti-crawler**: Some sites have protection, set reasonable intervals |
| **WebDriver 版本**：确保 Edge WebDriver 版本与浏览器版本匹配 | **WebDriver version**: Ensure WebDriver matches browser version |
| **页面结构**：网站改版可能导致元素定位失效，需及时更新选择器 | **Page structure**: Site updates may break locators, update accordingly |
| **法律合规**：请遵守目标网站的 robots.txt 和使用条款 | **Legal compliance**: Follow target site's robots.txt and ToS |
| **资源占用**：爬取大量数据时注意内存占用 | **Resources**: Monitor memory when crawling large datasets |

---

## 📝 更新日志 | Changelog

| 日期 Date | 中文 | English |
|-----------|------|---------|
| 2025.06.11 | 项目启动 | Project started |
| - | 支持动态页面爬取 | Support dynamic page crawling |
| - | 支持 MySQL 数据存储 | Support MySQL storage |
| - | 支持 Excel/CSV 导出 | Support Excel/CSV export |

---

## 📄 许可证 | License

本项目仅供学习和研究使用，请勿用于非法用途。

This project is for learning and research purposes only. Do not use for illegal purposes.

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

Welcome to submit Issues and Pull Requests!
