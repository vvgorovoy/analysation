# -*- coding: utf-8 -*-
"""
Модуль запуска программы
Автор: Владимир Горовой
"""

import os
import pandas as pd
from Scripts.setup import HOST, USER, PASSWORD, DB_NAME, CHANGED, HAS_SQL
from Scripts.app import activate_app

if not os.path.exists(r"Data/splist_for_parser.csv"):
    from Library.creator_splist_for_parser import activate_creator_splist_for_parser
    activate_creator_splist_for_parser()

if not os.path.exists(r"Data/splist_with_mc.csv"):
    from Library.splist_with_mc_parser import activate_splist_with_mc_parser
    activate_splist_with_mc_parser()

if not os.path.exists(r"Data/first_year_list.csv"):
    from Library.first_year_list_parser import activate_first_year_list_parser
    activate_first_year_list_parser()

if not os.path.exists(r"Data/financial_data.csv"):
    from Library.fin_data_parser import activate_fin_data_parser
    activate_fin_data_parser()

if not os.path.exists(r"Data/data.csv"):
    from Library.modifier import modify
    modify()

if CHANGED and HAS_SQL:
    fin_data = pd.read_csv(r"Data/data.csv")
    try:
        from Library.db_creator import create_server_connection, create_database, \
                       fill_table_in_database, get_data_from_database
        con = create_server_connection(HOST, USER, PASSWORD)
        check = con.cursor()
        check.execute('SHOW DATABASES')
        if (DB_NAME,) in check.fetchall():
            print("Database exists and table is filled in")
        else:
            cur = create_database(con, DB_NAME)
            fill_table_in_database(HOST, USER, PASSWORD, DB_NAME, fin_data)

        fin_data = get_data_from_database(HOST, USER, PASSWORD, DB_NAME)
    except Exception:
        print("Имя пользователя или пароль неправильные")
elif HAS_SQL and not CHANGED:
    try:
        from Library.db_creator import get_data_from_database
        fin_data = get_data_from_database(HOST, USER, PASSWORD, DB_NAME)
    except Exception:
        print("Имя пользователя или пароль неправильные")
else:
    fin_data = pd.read_csv(r"Data/data.csv")

activate_app(fin_data)
