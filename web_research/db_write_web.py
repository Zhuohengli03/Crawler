from urllib.parse import urlparse
import streamlit as st
from db_link_web import link_db, close_db
from mysql.connector import Error




def insert_news(host, user, password, database, port):
    connection = link_db(host, user, password, database, port)
    cursor = connection.cursor()

    "ALTER TABLE [database] ADD COLUMN id INTEGER AUTO_INCREMENT"

    close_db(connection, cursor)

