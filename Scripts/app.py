# -*- coding: utf-8 -*-
"""
Модуль интерфейса
Авторы:
    Владимир Горовой
    Алексей Маркин
"""

import os
import shutil
import pandas as pd
import numpy as np
import PySimpleGUI as sg
import plotly.express as px
import plotly.offline as offline


def activate_app(fin_data):
    """
    Функция вызова из другого скрипта
    Авторы:
        Владимир Горовой
        Алексей Маркин
    Вход: fin_data - pd.DataFrame - таблица всей базы данных
    Выход: -
    """
    names = []
    tickers = []
    for i in np.arange(len(fin_data)):
        names.append(fin_data.iloc[i,0])
        tickers.append(fin_data.iloc[i,1])

    sg.theme('LightBrown1')

    layout = [
        [sg.Text(
            'Choose name of company or its ticker below'
            ), sg.Button('See'), sg.Button('Delete')],
        [sg.Combo(values=names, default_value='Choose company',
                  size=(45,1), key='NAME',  enable_events=True),
         sg.Combo(values=tickers, default_value='Choose ticker',
                  size=(12,1), key='TICK', enable_events=True)],
        [sg.Button('Find by name', size=(40,1)), sg.Button('Find by ticker', size=(12,1))]
                 ]

    headings = ['Parameter']
    for i in np.arange(2005,2021):
        headings.append(str(i))

    param_list = ['Revenue', 'Net Income', 'EBITDA',
                  'Cash', 'Debt', 'Total Assets', 'Total Liabilities',
                  'Market Cap', 'Price',
                  'P/E', 'P/S', 'P/B', 'EV/EBITDA',
                  'NetDebt/EBITDA', 'D/E', 'ROE', 'ROA', 'EPS']
    year_list = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012,
                 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]


    def get_values_by_name(name):
        values_data = []
        for i in np.arange(len(param_list)):
            row = []
            row.append(param_list[i])
            end_of_row = [fin_data.iloc[
                fin_data[fin_data['Company'] == name].index[0], j
                ] for j in np.arange(i*(len(headings)-1)+4, i*(len(headings)-1)+20)]
            for j in np.arange(len(end_of_row)):
                row.append(end_of_row[j])
            values_data.append(row)
        return values_data

    def get_values_by_ticker(tick):
        values_data = []
        for i in np.arange(len(param_list)):
            row = []
            row.append(param_list[i])
            end_of_row = [fin_data.iloc[
                fin_data[fin_data['Ticker'] == tick].index[0], j
                ] for j in np.arange(i*(len(headings)-1)+4, i*(len(headings)-1)+20)]
            for j in np.arange(len(end_of_row)):
                row.append(end_of_row[j])
            values_data.append(row)
        return values_data

    def add_company_by_name(name):
        c_lay = [[sg.Text('Company:'), sg.Text(name),
                  sg.Text('Ticker:'),
                  sg.Text(fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]),
                  sg.Text('Sector:'),
                  sg.Text(fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 2]),
                  sg.Text('Sub-sector:'),
                  sg.Text(fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 3]),
                  sg.Text('Visualize'),
                  sg.Combo(values=param_list, default_value='Revenue', key='PARAM'),
                  sg.Button('Interactively'), sg.Button('Non-interactively')
                  ],
                 [sg.Table(values=get_values_by_name(name), headings=headings,
                           auto_size_columns=True, display_row_numbers=False, row_height=20,
                           num_rows=len(param_list), justification='left',
                           hide_vertical_scroll=True,
                           enable_events=True)],
                 [sg.Button('Return')]
                 ]
        return c_lay

    def add_company_by_ticker(tick):
        c_lay = [[sg.Text('Company:'),
                  sg.Text(fin_data.iloc[fin_data[fin_data['Ticker'] == tick].index[0], 0]),
                  sg.Text('Ticker:'), sg.Text(tick),
                  sg.Text('Sector:'),
                  sg.Text(fin_data.iloc[fin_data[fin_data['Ticker'] == tick].index[0], 2]),
                  sg.Text('Sub-sector:'),
                  sg.Text(fin_data.iloc[fin_data[fin_data['Ticker'] == tick].index[0], 3]),
                 sg.Text('Visualize'),
                 sg.Combo(values=param_list, default_value='Revenue', key='PARAM'),
                 sg.Button('Interactively'), sg.Button('Non-interactively')
                 ],
                 [sg.Table(values=get_values_by_ticker(tick), headings=headings,
                           auto_size_columns=True, display_row_numbers=False, row_height=20,
                           num_rows=len(param_list), justification='left',
                           hide_vertical_scroll=True,
                           enable_events=True)],
                 [sg.Button('Return')]
                 ]
        return c_lay

    def visualize(name, par):
        """
        Визуализация параметра по названию компании в формате html 
        Автор: Алексей Маркин
        Вход: name – название компании, par – наименование параметра
        Выход: файл в формате html с графиком параметра
        """
        for i in np.arange(len(fin_data.index)):
            if fin_data.iloc[i]['Company'] == name:
                ind = i
        for xxx in np.arange(len(param_list)):
            if param_list[xxx] == par:
                min = xxx*(len(headings)-1)+4
                max = xxx*(len(headings)-1)+20
                break
        while min < max:
            if not pd.isna(fin_data.iloc[ind][min]):
                break
            min += 1
        sr1 = fin_data.iloc[ind][min:max]
        sr1[:] = sr1[:].apply(pd.to_numeric)
        nnn = 16 - (max - min)
        sr1.index = year_list[nnn:16]
        sr1.name = f"{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}"
        if par not in ('Market Cap', 'Price'):
            fig = px.bar(sr1,
                title= f"{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}_{par}"
                         )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if par in ('Market Cap', 'Price'):
            fig = px.line(sr1,
                title= f"{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}_{par}"
                    )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if os.path.exists(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0],1]}"
                ) == 0:
            os.mkdir(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0],1]}"
                )
        offline.plot(fig, auto_open=True,
            filename=rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}/{par.replace('/', '')}.html",
            validate=False)

    def visualize3(name, par):
        """
        Визуализация параметра по наименованию тикера в формате html 
        Автор: Алексей Маркин
        Вход: name – наименование тикера, par – название параметра
        Выход: файл в формате html с графиком параметра
        """
        for i in np.arange(len(fin_data.index)):
            if fin_data.iloc[i]['Ticker'] == name:
                ind = i
        for xxx in np.arange(len(param_list)):
            if param_list[xxx] == par:
                min = xxx*(len(headings)-1)+4
                max = xxx*(len(headings)-1)+20
                break
        while min < max:
            if not pd.isna(fin_data.iloc[ind][min]):
                break
            min += 1
        sr1 = fin_data.iloc[ind][min:max]
        sr1[:] = sr1[:].apply(pd.to_numeric)
        nnn = 16 - (max - min)
        sr1.index = year_list[nnn:16]
        sr1.name = f"{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}"
        if par not in ('Market Cap', 'Price'):
            fig = px.bar(sr1,
                title= f"{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}_{par}"
                )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if par in ('Market Cap', 'Price'):
            fig = px.line(sr1,
                title= f"{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}_{par}"
                )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if os.path.exists(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0],1]}"
                ) == 0:
            os.mkdir(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0],1]}"
                )
        offline.plot(fig, auto_open=True,
            filename=rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}/{par.replace('/', '')}.html",
            validate=False)

    def visualize2(name, par):
        """
        Визуализация параметра по названию компании в формате png 
        Автор: Алексей Маркин
                     Владимир Горовой
        Вход: name – название компании, par – наименование параметра
        Выход: файл в формате png с графиком параметра
        """
        for i in np.arange(len(fin_data.index)):
            if fin_data.iloc[i]['Company'] == name:
                ind = i
        for xxx in np.arange(len(param_list)):
            if param_list[xxx] == par:
                min = xxx*(len(headings)-1)+4
                max = xxx*(len(headings)-1)+20
                break
        while min < max:
            if not pd.isna(fin_data.iloc[ind][min]):
                break
            min += 1
        sr1 = fin_data.iloc[ind][min:max]
        sr1[:] = sr1[:].apply(pd.to_numeric)
        nnn = 16 - (max - min)
        sr1.index = year_list[nnn:16]
        sr1.name = f"{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}"
        if par not in ('Market Cap', 'Price'):
            fig = px.bar(sr1,
                title= f"{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}_{par}"
                    )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if par in ('Market Cap', 'Price'):
            fig = px.line(sr1,
                title= f"{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}_{par}"
                    )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if os.path.exists(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0],1]}"
                ) == 0:
            os.mkdir(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0],1]}"
                )
        fig.write_image(
            rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == name].index[0], 1]}/{par.replace('/', '')}.png",
            engine="kaleido")

    def visualize4(name, par):
        """
        Визуализация параметра по наименованию тикера в формате png 
        Автор: Алексей Маркин
                     Владимир Горовой
        Вход: name – наименование тикера, par – название параметра
        Выход: файл в формате png с графиком параметра
        """
        for i in np.arange(len(fin_data.index)):
            if fin_data.iloc[i]['Ticker'] == name:
                ind = i
        for xxx in np.arange(len(param_list)):
            if param_list[xxx] == par:
                min = xxx * (len(headings) - 1) + 4
                max = xxx * (len(headings) - 1) + 20
                break
        while min < max:
            if not pd.isna(fin_data.iloc[ind][min]):
                break
            min += 1
        sr1 = fin_data.iloc[ind][min:max]
        sr1[:] = sr1[:].apply(pd.to_numeric)
        nnn = 16 - (max - min)
        sr1.index = year_list[nnn:16]
        sr1.name = f"{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}"
        if par not in ('Market Cap', 'Price'):
            fig = px.bar(sr1,
                title=f"{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}_{par}"
                )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if par in ('Market Cap', 'Price'):
            fig = px.line(sr1,
                title=f"{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}_{par}"
                )
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text=f'{par}')
        if os.path.exists(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}"
                ) == 0:
            os.mkdir(
                rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}"
                )
        fig.write_image(
            rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == name].index[0], 1]}/{par.replace('/', '')}.png",
            engine="kaleido")

    if os.path.exists('Graphics') == 0:
        os.mkdir(r'Graphics')

    win1 = sg.Window('Main screen', layout, resizable = True)
    win2_active = False

    while True:
        ev1, val1 = win1.read()
        if ev1 == sg.WIN_CLOSED:
            break
        if ev1 == 'See':
            if os.path.exists('Graphics') == 1:
                os.startfile("Graphics")
        if ev1 == 'Delete':
            if os.path.exists('Graphics') == 1:
                shutil.rmtree(r'Graphics')
        if ev1 == 'Find by name' and not win2_active:
            try:
                win2_active = True
                win1.Hide()
                com_layout = add_company_by_name(val1['NAME'])
                win2 = sg.Window('Table', com_layout, resizable = True)
                while True:
                    ev2,val2 = win2.read()
                    if ev2 in (sg.WIN_CLOSED, 'Return'):
                        win2.close()
                        win2_active = False
                        win1.UnHide()
                        break
                    if ev2 == 'Interactively':
                        visualize(val1['NAME'], val2['PARAM'])
                    if ev2 == 'Non-interactively':
                        visualize2(val1['NAME'], val2['PARAM'])
                        graph_layout = [
                                        [sg.Image(rf"Graphics/{fin_data.iloc[fin_data[fin_data['Company'] == val1['NAME']].index[0], 1]}/{val2['PARAM'].replace('/', '')}.png")],
                                        [sg.Button('Close')]]
                        win2.Hide()
                        win3 = sg.Window('Graph', graph_layout, resizable = True)
                        while True:
                            ev3, val3 = win3.read()
                            if ev3 == sg.WIN_CLOSED:
                                win3.close()
                                win2.UnHide()
                                break
                            if ev3 == 'Close':
                                win3.close()
                                win2.UnHide()
                                break
            except:
                win2_active = False
                sg.popup_error("Wrong or not existing company name")
                win1.UnHide()
        if ev1 == 'Find by ticker' and not win2_active:
            try:
                win2_active = True
                win1.Hide()
                com_layout = add_company_by_ticker(val1['TICK'])
                win2 = sg.Window('Table', com_layout, resizable = True)
                while True:
                    ev2,val2 = win2.read()
                    if ev2 in (sg.WIN_CLOSED, 'Return'):
                        win2.close()
                        win2_active = False
                        win1.UnHide()
                        break
                    if ev2 == 'Interactively':
                        visualize3(val1['TICK'], val2['PARAM'])
                    if ev2 == 'Non-interactively':
                        visualize4(val1['TICK'], val2['PARAM'])
                        graph_layout = [
                                        [sg.Image(rf"Graphics/{fin_data.iloc[fin_data[fin_data['Ticker'] == val1['TICK']].index[0], 1]}/{val2['PARAM'].replace('/', '')}.png")],
                                        [sg.Button('Close')]]
                        win2.Hide()
                        win3 = sg.Window('Graph', graph_layout, resizable = True)
                        while True:
                            ev3, val3 = win3.read()
                            if ev3 == sg.WIN_CLOSED:
                                win3.close()
                                win2.UnHide()
                                break
                            if ev3 == 'Close':
                                win3.close()
                                win2.UnHide()
                                break
            except:
                win2_active = False
                sg.popup_error("Wrong or not existing ticker")
                win1.UnHide()
    win1.close()
