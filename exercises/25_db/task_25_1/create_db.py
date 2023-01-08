#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
1 скрипт create_db.py - в этот скрипт должна быть вынесена функциональность по созданию БД:
* должна выполняться проверка наличия файла БД
* если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
  должна быть создана БД
* имя файла бд - dhcp_snooping.db

В БД должно быть две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - тут хранится информация полученная из вывода sh ip dhcp snooping binding

Пример выполнения скрипта, когда файла dhcp_snooping.db нет:
$ python create_db.py
Создаю базу данных...

После создания файла:
$ python create_db.py
База данных существует
"""
import sqlite3
import os


def create_db(db_name, file_sql=None):
    """
    Фунция ожидает аргументы:
    * db_name - имя базы данных для создания
    * file_sql - имя файла со схемой создания базы данных,
    если не задан будет использоваться db_name.replace('.db', '_schema.sql')
    Функция создает базу данных.
    """

    if file_sql:
        db_schema = file_sql
    else:
        db_schema = db_name.replace('.db', '_schema.sql')

    db_exist = os.path.isfile(db_name)
    connection = sqlite3.connect(db_name)
    if not db_exist:
        print('Создаю базу данных...')
        with open(db_schema) as f:
            connection.executescript(f.read())
    else:
        print('База данных существует')

if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    create_db(db_name)
