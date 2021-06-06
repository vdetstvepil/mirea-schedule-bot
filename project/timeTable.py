from datetime import date
from pathlib import Path

import openpyxl
import requests
import xlrd
from bs4 import BeautifulSoup
from dateutil import parser

import dbFunctions
import parameters

def init_timetable():
    if needToUpdate():
        get_timetable()

def get_timetable():
    # Адрес сайта расписания РТУ МИРЭА.
    url = 'https://www.mirea.ru/schedule/'

    # Получаем страницу, парсим через BeautifulSoup.
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # Получаем куски тегов с ссылками.
    result = soup.find("div", {"class": "rasspisanie"}). \
        find(string="Институт информационных технологий"). \
        find_parent("div"). \
        find_parent("div"). \
        findAll('a', class_='uk-link-toggle')

    # Словарь.
    dictTimetables = {1: None, 2: None, 3: None}

    # Выводим ссылки на расписание.
    print("Links to timetables:")
    for x in result:
        print("  link: " + str(x["href"]))
        if "ИИТ_1к" in x["href"] and "весна" in x["href"]:
            print("    Downloading started.")
            f = open("file1.xlsx", "wb")
            resp = requests.get(x["href"])
            f.write(resp.content)
            dictTimetables[1] = f
            print("    Downloading completed.")
        elif "ИИТ_2к" in x["href"] and "весна" in x["href"]:
            print("    Downloading started.")
            f = open("file2.xlsx", "wb")
            resp = requests.get(x["href"])
            f.write(resp.content)
            dictTimetables[2] = f
            print("    Downloading completed.")
        elif "ИИТ_3к" in x["href"] and "весна" in x["href"]:
            print("    Downloading started.")
            f = open("file3.xlsx", "wb")
            resp = requests.get(x["href"])
            f.write(resp.content)
            dictTimetables[3] = f
            print("    Downloading completed.")
    insert_timetable_into_db(dictTimetables)


def insert_timetable_into_db(dictTimetables):
    print("Inserting to database started.")

    sqlite_connection = dbFunctions.sqlite_connection
    cursor = sqlite_connection.cursor()
    command = "DELETE FROM timetable_pairs;"
    cursor.execute(command)

    xlsx = openpyxl.load_workbook('file1.xlsx')
    ws = xlsx.active

    for row in ws.iter_rows():
        for cell in row:
            if str(cell.value).find("ИАБО-") != -1 \
                    or str(cell.value).find("ИВБО-") != -1 \
                    or str(cell.value).find("ИКБО-") != -1 \
                    or str(cell.value).find("ИМБО-") != -1 \
                    or str(cell.value).find("ИНБО-") != -1:
                print("  found group: " + str(cell.value))
                record_timetable_into_db(str(cell.value), int(cell.row), int(cell.column), ws)

    # print(ws["F2"].value)
    # print(ws.cell(2, 311).value)


    command = "INSERT INTO timetable_updates (session) VALUES (\'" + date.today().strftime('%Y-%m-%d') + "\');"
    cursor.execute(command)
    cursor.close()
    sqlite_connection.commit()

    print(parameters.OKGREEN + "Database updated" + parameters.ENDC)


def record_timetable_into_db(group_name, cell_row, cell_col, ws):
    print("    Recording started.")

    sqlite_connection = dbFunctions.sqlite_connection
    cursor = sqlite_connection.cursor()

    for days in range(1, 7):
        for pair in range(1, 7):
            for k in range(1, 3):
                even = False
                if k == 1:
                    even = False
                else:
                    even = True
                pair_name = str(ws.cell(((cell_row + 2) + 2 * (pair - 1) + (k - 1)) * days, cell_col).value)
                pair_type = str(ws.cell(((cell_row + 2) + 2 * (pair - 1) + (k - 1)) * days, cell_col + 1).value)
                pair_teacher = str(ws.cell(((cell_row + 2) + 2 * (pair - 1) + (k - 1)) * days, cell_col + 2).value)
                pair_room = str(ws.cell(((cell_row + 2) + 2 * (pair - 1) + (k - 1)) * days, cell_col + 3).value)
                command = "INSERT INTO timetable_pairs VALUES(\'" + group_name + "\', \'" + str(days) + "\', \'" + str(pair) +\
                          "\', \'" + str(even) + "\', \'" + pair_name + "\', \'" + pair_type + "\', \'" + \
                          pair_teacher + "\', \'" + pair_room + "\');"
                cursor.execute(command)
    cursor.close()
    sqlite_connection.commit()
    print("    Recording completed.")


def needToUpdate():
    sqlite_connection = dbFunctions.sqlite_connection
    cursor = sqlite_connection.cursor()

    command = "SELECT MAX(id) FROM timetable_updates;"
    c = cursor.execute(command)
    for row in c:
        if row[0] is None:
            return True

    command = "SELECT * FROM timetable_updates ORDER BY id DESC LIMIT 1;"
    c = cursor.execute(command)
    for row in c:
        if int(row[0]) < 1:
            return True
        else:
            date = parser.parse(row[1])
            if date.date() < date.today().date():
                return True
            else:
                print(parameters.OKGREEN + "Database was recently updated (" + str(
                    date.today().date()) + ")" + parameters.ENDC)
                return False
    return False


def findGroup(group_name):
    print("Trying to find group " + group_name)
    sqlite_connection = dbFunctions.sqlite_connection
    cursor = sqlite_connection.cursor()
    command = "SELECT DISTINCT group_name FROM timetable_pairs WHERE group_name = \'" + group_name + "\';"
    c = cursor.execute(command)
    for row in c:
        if row[0] is None:
            return False
        else:
            return True
    return False