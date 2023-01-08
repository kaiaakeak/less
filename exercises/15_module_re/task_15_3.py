# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import re

# 1 вариант

def convert_ios_nat_to_asa(file_src, file_out):
    with open(file_src) as f:
        lst_test = list()
        regex = (
            r'ip nat.*\s(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) (?P<src_p>\d+) \S+ \S+ (?P<dst_p>\d+)'
            )


        for line in f:
            match = re.match(regex, line)
            ip = match.group('ip')
            src_p = match.group('src_p')
            dst_p = match.group('dst_p')
            #lst_test.append(out.format(match.group('ip', 'src_p', 'dst_p')))
            lst_test.append(f"object network LOCAL_{ip}\n host {ip}\n nat (inside,outside) static interface service tcp {src_p} {dst_p}\n")
            #print(match.groups())

        with open(file_out, 'w') as wr:
            wr.writelines(lst_test)



if __name__ == "__main__":
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'convert_ios_nat_to_asa.txt')