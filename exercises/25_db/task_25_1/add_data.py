#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2 скрипт add_data.py - с помощью этого скрипта, выполняется добавление данных в БД.
Скрипт должен добавлять данные из вывода sh ip dhcp snooping binding
и информацию о коммутаторах

Соответственно, в файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно
   также заполнять. Имя коммутатора определяется по имени файла с данными

Пример выполнения скрипта, когда база данных еще не создана:
$ python add_data.py
База данных не существует. Перед добавлением данных, ее надо создать

Пример выполнения скрипта первый раз, после создания базы данных:
$ python add_data.py
Добавляю данные в таблицу switches...
Добавляю данные в таблицу dhcp...

Пример выполнения скрипта, после того как данные были добавлены в таблицу
(порядок добавления данных может быть произвольным, но сообщения должны
выводиться аналогично выводу ниже):

$ python add_data.py
Добавляю данные в таблицу switches...
При добавлении данных: ('sw1', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw2', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
При добавлении данных: ('sw3', 'London, 21 New Globe Walk') Возникла ошибка: UNIQUE constraint failed: switches.hostname
Добавляю данные в таблицу dhcp...
При добавлении данных: ('00:09:BB:3D:D6:58', '10.1.10.2', '10', 'FastEthernet0/1', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:04:A3:3E:5B:69', '10.1.5.2', '5', 'FastEthernet0/10', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:05:B3:7E:9B:60', '10.1.5.4', '5', 'FastEthernet0/9', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:07:BC:3F:A6:50', '10.1.10.6', '10', 'FastEthernet0/3', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:09:BC:3F:A6:50', '192.168.100.100', '1', 'FastEthernet0/7', 'sw1') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:BC:3F:A6:50', '100.1.1.6', '3', 'FastEthernet0/20', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:E9:22:11:A6:50', '100.1.1.7', '3', 'FastEthernet0/21', 'sw3') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BB:3D:D6:58', '10.1.10.20', '10', 'FastEthernet0/7', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:B4:A3:3E:5B:69', '10.1.5.20', '5', 'FastEthernet0/5', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:C5:B3:7E:9B:60', '10.1.5.40', '5', 'FastEthernet0/9', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac
При добавлении данных: ('00:A9:BC:3F:A6:50', '10.1.10.60', '20', 'FastEthernet0/2', 'sw2') Возникла ошибка: UNIQUE constraint failed: dhcp.mac


На данном этапе, оба скрипта вызываются без аргументов.

Код в скриптах должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.

"""
import sqlite3
import yaml
import re
import subprocess


def write_rows_to_db(connection, query, data, verbose=True):
        ''' Функция ожидает аргументы:
        * connection - соединение с БД
        * query - запрос, который нужно выполнить
        * data - данные, которые надо передать в виде списка кортежей

        Функция пытается записать поочереди кортежи из списка data.
        Если кортеж удалось записать успешно, изменения сохраняются в БД.
        Если в процессе записи кортежа возникла ошибка, транзакция откатывается.

        Флаг verbose контролирует то, будут ли выведены сообщения об удачной
        или неудачной записи кортежа.
        '''
        for row in data:
            try:
                with connection:
                    connection.execute(query, row)
            except sqlite3.IntegrityError as e:
                if verbose:
                    print("При записи данных '{}' возникла ошибка".format(
                        ', '.join(row), e))
            else:
                if verbose:
                    print("Запись данных '{}' прошла успешно".format(
                        ', '.join(row)))

def info_dhcp(files, glob=True):
    """ Function arguments:
    * files - define list files of dhcp_snooping from switches
    flag glob - out cli (ls -l *.txt) OR list of files

    Function returns list of informations from dhcp_snooping files
    """

    regex = re.compile(
                        r'(?P<mac>(?:\w{2}:){5}\w{2})'                # mac address
                        r'\s+'
                        r'(?P<ip>(?:\d{1,3}.){3}\d{1,3})'             # ip address
                        r'\s+\S+\s+dhcp\S+\s+'
                        r'(?P<vlan>\d+)'                              # vlan id
                        r'\s+'
                        r'(?P<intf>\S+)'                              # interface
                        , re.S)

    if glob:
        out_ls_glob = subprocess.run(files, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        dhcp_files = []
        out_str = out_ls_glob.split('\n')
        for l in range(len(out_str)):
            if out_str[l]:
                if '/' in out_str[l].split()[-1]:
                    dir_l = out_str[l].split()[-1]
                    dhcp_files.append(dir_l.split('/')[-1])
                else:
                    dhcp_files.append(out_str[l].split()[-1])
    else:
        if isinstance(files, str):
            dhcp_files = [files]
        elif isinstance(files, list):
            dhcp_files=files

    data_dhcp=[]
    for dhcp_file in dhcp_files:
        hostname = dhcp_file.replace('_dhcp_snooping.txt', '')
        with open(dhcp_file) as f:
            data = f.read()
        data_iter = regex.finditer(data)
        for i in data_iter:
            temp = [i.group('mac'), i.group('ip'), i.group('vlan'), i.group('intf')]
            temp.append(hostname)
            data_dhcp.append(tuple(temp))
    return data_dhcp


if __name__ == "__main__":
    db_name = 'dhcp_snooping.db'
    #dhcp_files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']

    with open('switches.yml') as f:
        switches_d = yaml.safe_load(f)
    switches = [(sw, switches_d['switches'][sw]) for sw in switches_d['switches']]

    query_sw = 'INSERT into switches (hostname, location) values (?, ?)'
    query_dhcp = 'INSERT into dhcp values (?, ?, ?, ?, ?)'

    connection = sqlite3.connect(db_name)
    write_rows_to_db(connection, query_sw, switches)
    write_rows_to_db(connection, query_dhcp, info_dhcp('ls -l *dhcp_snoop*.txt'))