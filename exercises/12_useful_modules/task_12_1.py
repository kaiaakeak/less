# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

def ping_ip_addresses(list_ipaddress):
    lst_pingable=list()
    lst_pingunable=list()

    for ip in list_ipaddress:
        result = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        #print(result.stdout)
        if result.returncode == 0:
            lst_pingable.append(ip)
        else:
            lst_pingunable.append(ip)

    return lst_pingable, lst_pingunable

if __name__ == "__main__":
    print(ping_ip_addresses(['8.8.8.8', 'ya.ru', '192.168.102.193', '192.168.1.129']))