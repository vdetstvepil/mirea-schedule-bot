import os
import sqlite3

import parameters

sqlite_connection = sqlite3.connect("")

# Создание базы данных.
def createDb():
    global sqlite_connection
    sqlite_connection = sqlite3.connect('sqlite_python.db')
    cursor = sqlite_connection.cursor()
    command = "CREATE TABLE timetable_pairs(group_name VARCHAR(10), day_number INTEGER, pair_number INTEGER, " \
              "pair_even BOOLEAN, pair_name VARCHAR(300), pair_type VARCHAR(10), pair_teacher VARCHAR(100), " \
              "pair_room VARCHAR(50), PRIMARY KEY(group_name, day_number, pair_number, pair_even));"
    cursor.execute(command)
    command = "CREATE TABLE timetable_updates(id INTEGER PRIMARY KEY AUTOINCREMENT, session TIMESTAMP);"
    cursor.execute(command)
    command = "CREATE TABLE users(id INTEGER PRIMARY KEY, group_name VARCHAR(10));"
    cursor.execute(command)
    cursor.close()
    sqlite_connection.commit()
    print("Tables created")

# Запуск базы данных.
def loadDb():
    global sqlite_connection
    try:
        needToCreate = False
        if not os.path.isfile('sqlite_python.db'):
            needToCreate = True
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print(parameters.OKGREEN + "SQLite database connected" + parameters.ENDC)
        cursor.close()
        if needToCreate:
            createDb()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
