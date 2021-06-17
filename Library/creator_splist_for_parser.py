# -*- coding: utf-8 -*-
"""
Модуль формирования списка компаний для отправки в парсеры
Автор: Алексей Маркин
"""


import pandas as pd

def activate_creator_splist_for_parser():
    """
    Функция для вызова из другого скрипта
    Автор: Алексей Маркин
    Вход: splist.csv - список компаний в виде csv-файла
    Выход: преобразованный под парсеры список компаний в виде csv-файла:
        splist_for_parser.csv
    """
    splist = pd.read_csv(r"Data/splist.csv")

    full_companies = splist.Company.tolist()

    companies = [company.replace(
        "International Business Machines","IBM"
        ) for company in full_companies]
    companies = [company.replace("Advanced Micro Devices","AMD") for company in companies]
    companies = [company.replace("United Parcel Service","UPS") for company in companies]
    companies = [company.replace("Automatic Data Processing","ADP") for company in companies]
    companies = [company.replace("Altria Group","Altria") for company in companies]
    companies = [company.replace("Goldman Sachs Group","Goldman Sachs") for company in companies]
    companies = [company.replace("Simon Property Group","Simon Property") for company in companies]
    companies = [company.replace("WEC Energy Group","WEC Energy") for company in companies]
    companies = [company.replace("CBRE Group","CBRE") for company in companies]
    companies = [company.replace(
        "Citizens Financial Group","Citizens Financial"
        ) for company in companies]
    companies = [company.replace("J.M. Smucker","J M Smucker") for company in companies]
    companies = [company.replace(
        "Zions Bancorporation","Zions Bancorporation,"
        ) for company in companies]
    companies = [company.replace("Alaska Air Group","Alaska Air") for company in companies]

    companies = [company.replace(".com","") for company in companies]
    companies = [company.replace(" & Co.","") for company in companies]
    companies = [company.replace(" Co.","") for company in companies]
    companies = [company.replace(" Corp.","") for company in companies]
    companies = [company.replace(" Inc.","") for company in companies]
    companies = [company.replace(" Incorporated","") for company in companies]
    companies = [company.replace(" Inc","") for company in companies]
    companies = [company.replace(" Ltd.","") for company in companies]
    companies = [company.replace(".","") for company in companies]
    companies = [company.replace(" Corporation","") for company in companies]
    companies = [company.replace(" Corp","") for company in companies]
    companies = [company.replace(" and Company","") for company in companies]
    companies = [company.replace(" & Company","") for company in companies]
    companies = [company.replace(" Company","") for company in companies]
    companies = [company.replace(" Companies","") for company in companies]
    companies = [company.replace(" Class A","") for company in companies]
    companies = [company.replace(" Class B","") for company in companies]
    companies = [company.replace(" Class C","") for company in companies]
    companies = [company.replace(" Class P","") for company in companies]
    companies = [company.replace(" Plc","") for company in companies]
    companies = [company.replace(" plc","") for company in companies]
    companies = [company.replace(" PLC","") for company in companies]
    companies = [company.replace(" International","") for company in companies]
    companies = [company.replace(" Communications","") for company in companies]
    companies = [company.replace(" Wholesale","") for company in companies]
    companies = [company.replace(" NV","") for company in companies]
    companies = [company.replace(" Limited","") for company in companies]
    companies = [company.replace(
        "L3Harris Technologies","L3Harris Technologies Inc"
        ) for company in companies]
    companies = [company.replace("Merck &","Merck") for company in companies]

    companies = [company.lower() for company in companies]
    companies = [company.replace("&","-") for company in companies]
    companies = [company.replace(" ","-") for company in companies]
    companies = [company.replace("---","-") for company in companies]
    companies = [company.replace("--","-") for company in companies]

    tickers = splist.Ticker.tolist()
    sectors = splist.Sector.tolist()
    subsectors = splist['Sub-sector'].tolist()

    new_data = pd.DataFrame(zip(companies, tickers, sectors, subsectors),
                            columns=['Company','Ticker', 'Sector', 'Sub-sector'])

    new_data.to_csv("splist_for_parser.csv", index = False)
