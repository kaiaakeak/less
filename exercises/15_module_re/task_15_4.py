# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.


Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""
import re
from pprint import pprint


def get_ints_without_description(filename):
    with open(filename) as f:
        lst_without = list()
        regex = (
            r'interface (\w\S+\d)\n'
            r'( .*\n)*'
            )

        for m in re.finditer(regex, f.read()):
            if not 'description' in m.group(): # and not 'shutdown' in m.group() and not 'no ip add' in m.group()
                lst_without.append(m.group(1))
        return(lst_without)

if __name__ == "__main__":
    pprint(get_ints_without_description('config_r1.txt'))
