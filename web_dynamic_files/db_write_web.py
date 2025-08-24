from urllib.parse import urlparse
import streamlit as st
from db_link_web import link_db, close_db
from mysql.connector import Error


def get_url_name(url):
    netloc = urlparse(url).netloc
    domain = netloc.split('.')[0]
    return domain


# 自动化表格格格式
def create_table(table_name, schema, host, user, password, database, port):

    connection = link_db(host, user, password, database, port)
    if not connection:
        st.error("连接失败，表格无法创建")
        return

    else:
        columns = ["id INT NOT NULL AUTO_INCREMENT PRIMARY KEY"]

        content_data = {
                "title": "varchar(255)",
                "url": "LONGTEXT NOT NULL",
                "content": "LONGTEXT",
                "image": "TEXT",
                "HTML": "LONGTEXT",
        }

        # 默认数据
        for field, data_type in content_data.items():
            if field not in schema:
                # 用反引号是防止ｆｉｅｌｄ即自定义名称中出现特殊字符，比如“空格”
                columns.append(f'`{field}` {data_type}')

        # 添加自定义的列名：格式
        for field, data_type in schema.items():

            # 转义字段名，防止SQL注入
            safe_field = field.replace('`', '``')
            columns.append(f'`{safe_field}` {data_type}')

        columns_sql = ",\n                        ".join(columns)
        create_table_sql = f'''
                CREATE TABLE IF NOT EXISTS `{table_name}` (
        {columns_sql}
                )'''
        cursor = connection.cursor()

        try:
            cursor.execute(create_table_sql)
            connection.commit()
            st.success("TABlE 创建成功")
        except Error as e:
            st.error(f"创建表格失败 {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()


# --------引用mian.py-------
def insert_news(finial_content, table_name, host, user, password, database, port):
    connection = link_db(host, user, password, database, port)
    cursor = connection.cursor()


    all_data = []
    if finial_content:
        all_data.extend(finial_content)


    if not all_data:
        st.warning("没有数据需要插入")
        close_db(connection, cursor)
        return

    try:
        success = 0
        failed = 0

        for news in all_data:
            fields = []
            placeholders = []
            values = []


            # 处理其他字段
            for field in ["title", "url", "content", "image", "HTML"]:
                if field in news:
                    fields.append(field)
                    placeholders.append("%s")
                    values.append(news[field])

            # 添加自定义字段
            for field in news:
                if field not in ["title", "url", "content", "image", "HTML"]:
                    fields.append(field)
                    placeholders.append("%s")
                    values.append(news[field])

            # 构建SQL语句
            fields_str = ", ".join([f"`{f}`" for f in fields])
            placeholders_str = ", ".join(placeholders)
            insert_sql = f"INSERT INTO `{table_name}` ({fields_str}) VALUES ({placeholders_str})"

            try:
                cursor.execute(insert_sql, values)
                connection.commit()
                success += 1
            except Exception as e:
                failed += 1
                st.warning(f"插入单条数据失败: {e}")
                connection.rollback()

        st.success(f"成功插入 {success} 条数据，失败 {failed} 条")

    except Exception as e:
        st.error(f"插入数据时发生错误: {e}")
        connection.rollback()

    close_db(connection, cursor)





# create_table()