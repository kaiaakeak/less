# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re


def parse_sh_cdp_neighbors(cdp_neigh_str):
        regex = re.compile(
            r'^(?P<neigh>\w+\d+)\s+'
            r'(?P<loc_intf>\w+ \d{1,2}/\d{1,2}).*?'
            r'(?P<neigh_intf>\w+ \d{1,2}/\d{1,2}).*?'
            ,re.DOTALL|re.MULTILINE)
        test_dict={}

        hostname = re.search(r'(\w+)>show cdp neighbors\n', cdp_neigh_str).group(1)
        match = regex.finditer(cdp_neigh_str)
        if match:
            test_dict[hostname]={m.group(2) : {m.group(1):m.group(3)} for m in match}
            return test_dict

if __name__ == "__main__":
    with open('sh_cdp_n_sw1.txt') as f:
        print(parse_sh_cdp_neighbors(f.read()))