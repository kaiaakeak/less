# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""
import re
import glob
import yaml
from pprint import pprint

def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    test={}
    regex = re.compile(
        r'^(?P<device_neigh>\w+\d)\s+'
        r'(?P<l_intf>\S+\s+\d{1,2}/\d{1,2}).*?'
        r'(?P<n_intf>\S+\s+\d{1,2}/\d{1,2}).*?'
        , re.DOTALL|re.MULTILINE
        )


    for file in list_of_files:
        with open(file) as f:
            hostname = file.replace('_', ' ').replace('.txt', '').split()[-1].upper()
            match = regex.finditer(f.read())
            test[hostname] = {m.group('l_intf') : {m.group('device_neigh'):m.group('n_intf')} for m in match}

    if not save_to_filename is None:
        with open(save_to_filename, 'w') as fl:
            yaml.dump(test, fl, default_flow_style=False)

    return test


sh_cdp_neighbors = glob.glob('sh_cdp_n*')
#sh_cdp_neighbors = ['sh_cdp_n_r1.txt']

if __name__ == "__main__":
    pprint(generate_topology_from_cdp(sh_cdp_neighbors, 'test.yaml'))