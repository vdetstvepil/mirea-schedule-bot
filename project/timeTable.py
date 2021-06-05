from pathlib import Path

import openpyxl
import requests
import xlrd
from bs4 import BeautifulSoup

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
            f = open("file1.xlsx", "wb")
            resp = requests.get(x["href"])
            f.write(resp.content)
            dictTimetables[1] = f
        elif "ИИТ_2к" in x["href"] and "весна" in x["href"]:
            f = open("file2.xlsx", "wb")
            resp = requests.get(x["href"])
            f.write(resp.content)
            dictTimetables[2] = f
        elif "ИИТ_3к" in x["href"] and "весна" in x["href"]:
            f = open("file3.xlsx", "wb")
            resp = requests.get(x["href"])
            f.write(resp.content)
            dictTimetables[3] = f
  

