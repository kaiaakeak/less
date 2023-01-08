# -*- coding: utf-8 -*-
"""
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
import re

def get_ip_from_cfg (config_filename):
    final_lst=list()
    regex = (r' ip address (?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})\s'
            r'(?P<mask>255.\d{1,3}.\d{1,3}.\d{1,3})')

    with open(config_filename) as config:
        for line in config:
            match = re.match(regex, line)
            if match:
                final_lst.append(match.group('ip', 'mask'))
        return(final_lst)