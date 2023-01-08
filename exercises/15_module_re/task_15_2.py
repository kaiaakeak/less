# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""
import re
from pprint import pprint

def parse_sh_ip_int_br(filename):
    with open(filename) as f:
        lst_result = list()
        regex = (
            r'(?P<intf>\S+\d{1,3}(/\d{1,3})?)\s*'
            r'(?P<ip>\S+|unassigned)\s*'
            r'\w+\s+\w+\s*'
            r'(?P<phys>up|down|administratively down)\s+(?P<logic>up|down|administratively down)'
            )

        for m in re.finditer(regex, f.read()):
            lst_result.append(m.group('intf', 'ip', 'phys', 'logic'))

        return lst_result

if __name__ == "__main__":
    pprint(parse_sh_ip_int_br('sh_ip_int_br.txt'))