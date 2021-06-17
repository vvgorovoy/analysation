# -*- coding: utf-8 -*-
"""
Модуль объединения всех таблиц в одну
Автор: Алексей Маркин
"""

import pandas as pd
import numpy as np


def remove_unused_rows_from_table(some_list):
    """
    Удаление строк с искаженными данными
    Автор: Алексей Маркин
    Вход: some_list – исходный список pd.DataFrame
    Выход: some_list – очищенная таблица pd.DataFrame
    """
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'INFO'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'KEYS'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'MS'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'ATVI'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'KR'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'MCK'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'ADM'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'HLT'].index)
    some_list = some_list.drop(index = some_list[some_list['Ticker'] == 'AMCR'].index)
    some_list = some_list.reset_index(drop = True)
    return some_list

def checknan(num):
    """
    Проверка на None
    Автор: Алексей Маркин
    Вход: num – значение
    Выход: True/False в зависимости от результат проверки
    """
    return num != num

def add_multiples(stn, multiples):
    """
    Добавление нескольких названий столбцов одного мультипликатора
    Автор: Алексей Маркин
    Вход: stn – мультипликатор(строка), multiples – список всех названий столбцов
    Выход: multiples – измененный список всех названий столбцов
    """
    for i in np.arange(2006,2022):
        multiples.append(stn + ' ' + str(i))

def modify():
    """
    Функция вызова из другого скрипта
    Автор: Алексей Маркин
    Вход: 6 спарсенных таблиц в виде csv-фалов:
        fin_data.csv, first_year_list.csv, splist.csv,
        splist_with_mc.csv, price_list.csv, splist_with_mc_old.csv
    Выход: единая таблица в виде csv-файла: data.csv
    """
    #Загружаем данные
    fin_data = pd.read_csv(r"Data/financial_data.csv")
    first_year_list = pd.read_csv(r"Data/first_year_list.csv")
    splist_with_mc = pd.read_csv(r"Data/splist_with_mc.csv")
    price_list = pd.read_csv(r"Data/price_list.csv")
    splist = pd.read_csv(r"Data/splist.csv")
    splist_with_mc_old = pd.read_csv(r"Data/splist_with_mc_old.csv")

    #Очищаем таблицы
    splist_with_mc = remove_unused_rows_from_table(splist_with_mc)
    splist_with_mc_old = remove_unused_rows_from_table(splist_with_mc_old)
    price_list = remove_unused_rows_from_table(price_list)
    fin_data = remove_unused_rows_from_table(fin_data)
    splist = remove_unused_rows_from_table(splist)
    first_year_list = remove_unused_rows_from_table(first_year_list)

    #Обработка текущих капитализаций
    new_mc_pr_list = pd.DataFrame(columns = splist_with_mc.columns.tolist())
    new_mc_pr_list['Company'] = splist['Company']
    new_mc_pr_list['Ticker'] = splist['Ticker']
    for i in np.arange(len(fin_data.index)):
        try:
            new_mc_pr_list['Market Cap'][i] = splist_with_mc['Market Cap'][splist_with_mc[splist_with_mc['Ticker'] == fin_data['Ticker'][i]].index[0]]
            new_mc_pr_list['Price'][i] = splist_with_mc['Price'][splist_with_mc[splist_with_mc['Ticker'] == fin_data['Ticker'][i]].index[0]]
        except:
            new_mc_pr_list['Market Cap'][i] = splist_with_mc_old['Market Cap'][splist_with_mc_old[splist_with_mc_old['Ticker'] == fin_data['Ticker'][i]].index[0]]
            new_mc_pr_list['Price'][i] = splist_with_mc_old['Price'][splist_with_mc_old[splist_with_mc_old['Ticker'] == fin_data['Ticker'][i]].index[0]]

    #Возвращение компаниям настоящих названий
    for i in np.arange(len(fin_data.index)):
        fin_data.loc[i, 'Company'] = splist.loc[i, 'Company']

    #Растчет коэффициентов для расчета капитализаций
    koefs = []
    for i in np.arange(len(new_mc_pr_list)):
        koefs.append(new_mc_pr_list.loc[i,'Market Cap']/new_mc_pr_list.loc[i,'Price'])

    #Добавление столбцов для цен и капитализаций
    mc_pr_columns = []
    for i in np.arange(2006,2022):
        mc_pr_columns.append(f'Market Cap {i}')
    for i in np.arange(2006,2022):
        mc_pr_columns.append(f'Price {i}')

    fin_data = fin_data.reindex(columns = fin_data.columns.tolist() + mc_pr_columns)

    #Рассчитываем капитализации на предыдущие года
    for i in np.arange(len(koefs)):
        for j in np.arange(2006,2022):
            fin_data.loc[i, f'Market Cap {j}'] = round(
                koefs[i] * price_list.loc[i, f'Price {j}'],
                2)
            fin_data.loc[i, f'Price {j}'] = price_list.loc[i, f'Price {j}']

    #Преобразование некорректных значений в np.nan
    for i in np.arange(len(fin_data.index)):
        for j in np.arange(2005, 2021):
            if checknan(fin_data[f'Revenue {j}'][i]):
                continue
            if fin_data.loc[i, f'Revenue {j}'] == '-':
                fin_data.loc[i, f'Revenue {j}'] = np.nan
            if fin_data.loc[i, f'Net Income {j}'] == '-':
                fin_data.loc[i, f'Net Income {j}'] = np.nan
            if fin_data.loc[i, f'EBITDA {j}'] == '-':
                fin_data.loc[i, f'EBITDA {j}'] = np.nan
            if fin_data.loc[i, f'Cash {j}'] == '-':
                fin_data.loc[i, f'Cash {j}'] = 0.0
            if fin_data.loc[i, f'Debt {j}'] == '-':
                fin_data.loc[i, f'Debt {j}'] = 0.0
            if fin_data.loc[i, f'Total Assets {j}'] == '-':
                fin_data.loc[i, f'Total Assets {j}'] = np.nan
            if fin_data.loc[i, f'Total Liabilities {j}'] == '-':
                fin_data.loc[i, f'Total Liabilities {j}'] = np.nan

    fin_data = fin_data.apply(pd.to_numeric, errors='ignore')

    #Добавляем новые столбцы для мультипликаторов
    multiples = []
    add_multiples('P/E', multiples)
    add_multiples('P/S', multiples)
    add_multiples('P/B', multiples)
    add_multiples('EV/EBITDA', multiples)
    add_multiples('NetDebt/EBITDA', multiples)
    add_multiples('D/E', multiples)
    add_multiples('ROE', multiples)
    add_multiples('ROA', multiples)
    add_multiples('EPS', multiples)

    fin_data = fin_data.reindex(columns = fin_data.columns.tolist() + multiples)

    #Расчет мультипликаторов
    for i in np.arange(2006,2022):
        for j in np.arange(len(fin_data.index)):
            if not(pd.isna(fin_data.loc[j, f'Market Cap {i}']) \
                   and pd.isna(fin_data.loc[j, f'Net Income {i-1}'])):
                fin_data.loc[j, f'P/E {i}'] = round(
                    fin_data.loc[j, f'Market Cap {i}'] / fin_data.loc[j, f'Net Income {i-1}'],
                    2)
            if not(pd.isna(fin_data.loc[j, f'Market Cap {i}']) \
                   and pd.isna(fin_data.loc[j, f'Revenue {i-1}'])):
                fin_data.loc[j, f'P/S {i}'] = round(
                    fin_data.loc[j, f'Market Cap {i}'] / fin_data.loc[j, f'Revenue {i-1}'],
                    2)
            if not(pd.isna(fin_data.loc[j, f'Market Cap {i}']) \
                   and pd.isna(fin_data.loc[j, f'Total Assets {i-1}']) \
                       and pd.isna(fin_data.loc[j, f'Total Liabilities {i-1}'])):
                fin_data.loc[j, f'P/B {i}'] = round(
                    fin_data.loc[j, f'Market Cap {i}'] / (fin_data.loc[j, f'Total Assets {i-1}'] - fin_data.loc[j, f'Total Liabilities {i-1}']),
                    2)
            if not(pd.isna(fin_data.loc[j, f'Market Cap {i}']) \
                   and pd.isna(fin_data.loc[j, f'Debt {i-1}']) \
                       and pd.isna(fin_data.loc[j, f'Cash {i-1}']) \
                           and pd.isna(fin_data.loc[j, f'EBITDA {i-1}'])):
                fin_data.loc[j, f'EV/EBITDA {i}'] = round(
                    (fin_data.loc[j, f'Market Cap {i}'] + fin_data.loc[j, f'Debt {i-1}'] - fin_data.loc[j, f'Cash {i-1}']) / fin_data.loc[j, f'EBITDA {i-1}'],
                    2)
            if not(pd.isna(fin_data.loc[j, f'Debt {i-1}']) \
                   and pd.isna(fin_data.loc[j, f'Cash {i-1}']) \
                       and pd.isna(fin_data.loc[j, f'EBITDA {i-1}'])):
                fin_data.loc[j, f'NetDebt/EBITDA {i}'] = round(
                    (fin_data.loc[j, f'Debt {i-1}'] - fin_data.loc[j, f'Cash {i-1}']) / fin_data.loc[j, f'EBITDA {i-1}'],
                    2)
            if not(pd.isna(fin_data.loc[j, f'Debt {i-1}']) \
                   and pd.isna(fin_data.loc[j, f'Total Assets {i-1}']) \
                       and pd.isna(fin_data.loc[j, f'Total Liabilities {i-1}'])):
                fin_data.loc[j, f'D/E {i}'] = round(
                    fin_data.loc[j, f'Debt {i-1}'] / (fin_data.loc[j, f'Total Assets {i-1}'] - fin_data.loc[j, f'Total Liabilities {i-1}']),
                    2)
            if not(pd.isna(fin_data.loc[j, f'Net Income {i-1}']) \
                   and pd.isna(fin_data.loc[j, f'Total Assets {i-1}']) \
                       and pd.isna(fin_data.loc[j, f'Total Liabilities {i-1}'])):
                fin_data.loc[j, f'ROE {i}'] = round(
                    fin_data.loc[j, f'Net Income {i-1}'] / (fin_data.loc[j, f'Total Assets {i-1}'] - fin_data.loc[j, f'Total Liabilities {i-1}']),
                    2)
            if not(pd.isna(fin_data.loc[j, f'Net Income {i-1}']) \
                   and pd.isna(fin_data.loc[j, f'Total Assets {i-1}'])):
                fin_data.loc[j, f'ROA {i}'] = round(
                    fin_data.loc[j, f'Net Income {i-1}'] / fin_data.loc[j, f'Total Assets {i-1}'],
                    2)
            if not(pd.isna(fin_data.loc[j, f'Market Cap {i}']) \
                   and pd.isna(fin_data.loc[j, f'Net Income {i-1}']) \
                       and pd.isna(fin_data.loc[j, f'Price {i}'])):
                fin_data.loc[j, f'EPS {i}'] = round(
                    fin_data.loc[j, f'Net Income {i-1}'] * fin_data.loc[j, f'Price {i}'] / fin_data.loc[j, f'Market Cap {i}'],
                    2)
    #Вывод
    fin_data = fin_data.astype(dtype='float', errors='ignore')
    fin_data = fin_data.round(2)
    fin_data.to_csv(r"Data/data.csv", index = False)
