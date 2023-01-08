# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
"""
def get_int_vlan_map (config_filename):
    config_filename=str(config_filename) # Для передачи имени файла
    config_dict=dict() # Создаем словарь, который будет содержать конфигурации интерфейсов
    with open(config_filename) as f: # Открываем файл, указанный как аргумент функции
        for line in f: # Перебираем по строкам
            if line.startswith('interface Fast'): # Если совпадает:
                port=line.replace('\n','')        #
                config_dict[port]=[]              # то создаем ключ, с пустым значением
            elif line.startswith(' switchport'):  # Если совпадает:
                config_dict[port].append(line.replace('\n', '')) # Добавляем в значение по данному ключу
    access={} # Создаем словарь для конфига портов доступа
    trunk={}  # Создаем словарь для конфига портов магистральных
    for intf in list(config_dict.keys()):   # пробегаемся по ключам словаря конфигураций, перебираем интерфейсы
        for mode in config_dict[intf]:      # пробегаемся по строкам конфигураций интерфейсов
            if 'access vlan' in mode:       # ищем строчку
                for vlan in mode.split(' '):  #если находим, разделяем строчку
                    if vlan.isdigit():  # ищем нужную строчку с числом
                        access[intf.replace('interface', '').replace(' ', '')]=int(vlan) # записываем в словарь
            elif 'trunk allowed vlan' in mode:
                vlans_trunk=mode.split(' ')[-1].split(',')
                port_of_trunk=intf.replace('interface', '').replace(' ', '')
                trunk[port_of_trunk]=[]
                for vlan_tr in vlans_trunk:
                    trunk[port_of_trunk].append(int(vlan_tr))
    tuple_conf=(access, trunk)
    return(tuple_conf)

"""
def get_int_vlan_map (config_filename):
    access_dict=dict()
    trunk_dict=dict()

    with open(config_filename) as config:
        for line in config:
            line = line.rstrip()
            if line.startswith('interface'):
                intf = line.split()[-1]
            elif 'access vlan' in line:
                access_dict[intf]=int(line.split()[-1])
            elif 'trunk allowed vlan' in line:
                trunk_dict[intf]=[]                     # { = trunk_dict[intf] = [int(v) for v in line.split()[-1].split(",")]
                for vl in line.split()[-1].split(','):  # { =
                    trunk_dict[intf].append(int(vl))
        tuple_fin=(access_dict, trunk_dict)
        return(tuple_fin)