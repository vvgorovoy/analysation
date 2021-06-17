# -*- coding: utf-8 -*-
"""
Модуль обработки базы данных на локальном сервере MySQL
Автор: Владимир Горовой
"""

import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine

def create_server_connection(host_name, user_name, user_password):
    """
    Подключение к локальному серверу MySQL
    Автор: Владимир Горовой
    Вход: host_name – имя хоста, user_name – имя пользователя, password – пароль
    Выход: connection – переменная соединения с сервером
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to server is successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, db_name):
    """
    Создание базы данных
    Автор: Владимир Горовой
    Вход: connection – переменная соединения с сервером, db_name – имя базы данных
    Выход: cursor – переменная работы с базой данных (курсор)
    """
    cursor = connection.cursor()
    query = f'CREATE DATABASE IF NOT EXISTS {db_name}'
    cursor.execute(query)
    return cursor

def fill_table_in_database(host_name, user_name, user_password, db_name, data):
    """
    Заполнение таблицы базы данных
    Автор: Владимир Горовой
    Вход: host_name – имя хоста, user_name – имя пользователя, password – пароль,
        database_name – имя базы данных, data – pd.DataFrame - вставляемая таблица
    Выход: -
    """
    #dialect+driver://username:password@host:port/database
    try:
        engine = create_engine(f'mysql+pymysql://{user_name}:{user_password}@{host_name}/{db_name}')
        data.to_sql(db_name, con=engine, if_exists='replace', index = False)
        print('Data recorded into database table')
    except Exception as err:
        print('Error: ', err)

def get_data_from_database(host_name, user_name, user_password, database_name):
    """
    Выгрузка данных из БД локального сервера MySQL
    Автор: Владимир Горовой
    Вход: имя хоста, имя пользователя, пароль, имя базы данных
    Выход: data – pd.DataFrame – полученная таблица
    """
    engine = create_engine(
        f'mysql+pymysql://{user_name}:{user_password}@{host_name}/{database_name}'
        )
    data = pd.read_sql(f"SELECT * FROM {database_name}", con=engine)
    return data
