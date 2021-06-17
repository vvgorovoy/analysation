# -*- coding: utf-8 -*-

"""
Модуль парсинга текущих цен и капитализаций
Автор: Алексей Маркин
"""


#Загрузка необходимых библиотек
import time
import pandas as pd
import numpy as np
from selenium import webdriver


def push_sorting_mc(browser):
    """
    Нажатие кнопки сортировки по капитализации
    Автор: Алексей Маркин
    Вход: browser – драйвер браузера
    Выход: -
    """
    sort_by_mc_button = browser.find_element_by_xpath(
        '//*[@id="js-screener-container"]/div[3]/table/thead/tr/th[7]'
        )
    sort_by_mc_button.click()
    time.sleep(1.5)
    sort_by_mc_button.click()
    time.sleep(1.5)

def push_load_more(browser):
    """
    Нажатие кнопки загрузить ещё для открытия всего контента страницы
    Автор: Алексей Маркин
    Вход: browser – драйвер браузера
    Выход: -
    """
    load_more_button = browser.find_element_by_xpath(
        '//*[@id="js-category-content"]/div/div[2]/div[3]/span'
        )
    for k in np.arange(3):
        load_more_button.click()
        time.sleep(1.5)

def activate_splist_with_mc_parser():
    """
    Функция для вызова из другого скрипта
    Автор: Алексей Маркин
    Вход: -
    Выход: таблица с капитализациями и ценами акций компаний в виде csv-файла:
        splist_with_mc_parser.csv
    """
    #Ссылка на сайт, с которого спарсятся данные
    link = 'https://www.tradingview.com/symbols/SPX/components/'

    #Открытие браузера
    browser = webdriver.Chrome()
    browser.set_window_size(1555, 883)

    browser.get(link)
    push_sorting_mc(browser)
    push_load_more(browser)

    num = int(browser.find_element_by_xpath(
        '//*[@id="js-screener-container"]/div[3]/table/thead/tr/th[1]/div/div/div[2]'
        ).text[:3])

    #Создание таблицы для новых данных
    splist = pd.DataFrame(np.arange(num*4).reshape(num,4),
                          columns = ['Company', 'Ticker', 'Market Cap', 'Price']
                          )

    #Выполнение парсинга и заполнение таблицы
    for ind in np.arange(num):
        company = browser.find_element_by_xpath(
            f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{ind+1}]/td[1]/div/div[2]/span[2]'
            ).text
        ticker = browser.find_element_by_xpath(
            f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{ind+1}]/td[1]/div/div[2]/a'
            ).text
        try:
            market_cap = round(float(browser.find_element_by_xpath(
                f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{ind+1}]/td[7]'
                ).text.replace('B',''))*1000, 1)
        except Exception:
            market_cap = round(float(browser.find_element_by_xpath(
                f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{ind+1}]/td[7]'
                ).text.replace('T',''))*1000000, 1)
        price = browser.find_element_by_xpath(
            f'//*[@id="js-screener-container"]/div[3]/table/tbody/tr[{ind+1}]/td[2]'
            ).text
        splist.loc[ind] = [company, ticker, market_cap, price]
    browser.quit()

    #Занесение готовой таблицы в новый файл
    splist.to_csv(r"Data/splist_with_mc.csv", index = False)
