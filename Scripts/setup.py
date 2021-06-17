# -*- coding: utf-8 -*-
"""
Модуль настроек приложения
Автор: Владимир Горовой
"""

import PySimpleGUI as sg


par = []
with open(r"Scripts/config.txt", "r") as file:
    for line in file:
        par.append(line[line.rfind('=')+1:-1])

layout1 = [[sg.Text('Установлен ли у вас на устройстве MySQL Server?')],
          [sg.Button('Да'), sg.Button('Нет')]]

layout2 = [[sg.Text('Хотите ли вы изменить старые настройки?')],
           [sg.Button('Да'), sg.Button('Нет')]]

layout3 = [[sg.Text('Настройте параметры, необходимые для работы с MySQL')],
           [sg.Text('username:'), sg.Input(key='-USER-')],
           [sg.Text('password:'), sg.Input(key='-PASS-')],
           [sg.Button('Сохранить')]]

win1 = sg.Window("Начало", layout1, no_titlebar=True)
while True:
    ev1, val1 = win1.read()
    if ev1 == 'Да':
        HAS_SQL = True
        win2 = sg.Window("Начало", layout2, no_titlebar=True)
        win1.Hide()
        while True:
            ev2, val2 = win2.read()
            if ev2 == 'Да':
                win3 = sg.Window("Настройка", layout3, no_titlebar=True)
                win2.Hide()
                while True:
                    ev3, val3 = win3.read()
                    if ev3 == 'Сохранить':
                        CHANGED = True
                        USER = val3['-USER-']
                        PASSWORD = val3['-PASS-']
                        win3.close()
                        break
                win2.close()
                break
            if ev2 == 'Нет':
                CHANGED = False
                win2.close()
                break
        win1.close()
        break
    if ev1 == 'Нет':
        HAS_SQL = False
        CHANGED = False
        win1.close()
        break

if not CHANGED:
    USER = par[1]
    PASSWORD = par[2]

HOST = par[0]
DB_NAME = par[3]

if CHANGED:
    with open(r"Scripts/config.txt", "w") as file:
        file.writelines(
        [f'HOST={HOST}\n', f'USER={USER}\n', f'PASSWORD={PASSWORD}\n', f'DB_NAME={DB_NAME}\n']
        )
