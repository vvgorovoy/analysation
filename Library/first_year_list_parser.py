# -*- coding: utf-8 -*-
"""
Программа для парсинга первого года финансовой отчетности,
представленной на сайте и для занесения этой информации в таблицу
Автор: Владимир Горовой
"""

#Загрузка необходимых библиотек
import time
import pandas as pd
import numpy as np
from selenium import webdriver


def get_year(page, browser):
    """
    Получение года первой финансовой отчетности, представленной на сайте
    Автор: Владимир Горовой
    Вход: page – ссылка на веб-страницу, browser –  драйвер браузера
    Выход: year – год
    """
    browser.get(page)
    i = 2005
    while i<=2021:
        if browser.find_element_by_xpath('/html/body/div[2]/div[2]/h2').text.find(f'{i}-') > -1:
            year = i
            break
        i+=1
    return year

def activate_first_year_list_parser():
    """
    Функция для вызова из другого скрипта
    Автор: Владимир Горовой
    Вход: преобразованный под парсеры список компаний в виде csv-файла:
        splist_for_parser.csv
    Выход: таблица с первыми годами финансовых отчетов, представленных на сайте,
        в виде csv-файла: first_year_list.csv
    """
    #Получение списка компаний из файла
    splist = pd.read_csv(r"Data/splist_for_parser.csv")

    #Создание новой таблицы
    first_year_list = splist.reindex(
        columns = splist.columns.tolist() + ['Year of first statement']
        )

    #Создание списка ссылок для парсинга
    links = []
    for ind in np.arange(len(splist.index)):
        link = f'https://www.macrotrends.net/stocks/charts/{splist.Ticker[ind]}/{splist.Company[ind]}/income-statement'
        links.append(link)

    #Открытие браузера Google Chrome
    browser = webdriver.Chrome()
    browser.set_window_size(1555, 883)

    #Выполнение парсинга и заполнение таблицы
    for ind in np.arange(len(splist.index)):  #len(splist.index)
        link = links[ind]
        first_year_list['Year of first statement'][ind] = get_year(link, browser)

    #Занесение готовой таблицы в новый файл и закрытие браузера
    first_year_list.to_csv(r"Data/first_year_list.csv", index = False)
    time.sleep(2)
    browser.quit()
