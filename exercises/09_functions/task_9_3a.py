# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map (config_filename):
    access_dict=dict()
    trunk_dict=dict()
    temp_access_dict=dict()
    with open(config_filename) as config:
        for line in config:
            line = line.rstrip()

            if line.startswith('interface'):
                intf = line.split()[-1]
            elif 'switchport mode access' in line:
                temp_access_dict[intf]=[]
                temp_access_dict[intf].append(line)
            elif 'switchport access vlan' in line:
                temp_access_dict[intf].append(line)
            elif 'trunk allowed vlan' in line:
                trunk_dict[intf]=[]
                for vl in line.split()[-1].split(','):
                    trunk_dict[intf].append(int(vl))

        for temp_key in list(temp_access_dict.keys()):
            if 'access vlan' in (('').join(temp_access_dict[temp_key])):
              access_dict[temp_key] = int((('').join(temp_access_dict[temp_key])).split()[-1])
            else:
                access_dict[temp_key] = 1

        tuple_fin=(access_dict, trunk_dict)
        return(tuple_fin)
