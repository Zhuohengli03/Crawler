import mysql.connector
from mysql.connector import Error
import streamlit as st


def link_db(host, user, password, database, port):
    try:
        connection = mysql.connector.connect(
            host= host,
            user= user,
            password=password,
            database=database,
            port=int(port),

        )

        if connection.is_connected():
            st.success("数据库连接成功")

            # print("数据库连接成功")
            # ---------注意要返回打开的链接，否则其他模块调用的时候链接默认被关闭--------
           # -------没有return默认返回none----------
            return connection

    except Error as e:
        st.error(f"链接数据库出错{e}")

def close_db(connection, cursor):
    if cursor:
        cursor.close()
    if connection and connection.is_connected():
        connection.close()
        st.success("数据库已关闭")

# link_db()
