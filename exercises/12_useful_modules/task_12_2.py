# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию  ,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""
import ipaddress


def convert_ranges_to_ip_list(lst_ipadd):
    """
    Функция для конвертации списка адрессов и диапазона адрессов в список, состоящий из конкретных адрессов
    """

    lst_correct_ipaddresses = list() # Список корректных адрессов, является результатом функции

    for poss_ipadd in lst_ipadd:
        try:
            ipadd = ipaddress.ip_address(poss_ipadd)
            lst_correct_ipaddresses.append(str(ipadd))

        except ValueError:
            ipadd_1 = ipaddress.ip_address(poss_ipadd.split('-')[0])

            if len(poss_ipadd.split('-')[-1].split('.')) == 4:
                for i in range((int(ipaddress.ip_address(poss_ipadd.split('-')[-1])) - int(ipadd_1))+1):
                    lst_correct_ipaddresses.append(str(ipadd_1+i))
            elif (poss_ipadd.split('-')[-1]).isdigit():
                ipadd_1a = ipaddress.ip_address(poss_ipadd.split('-')[0])
                for i in range((int(poss_ipadd.split('-')[-1]) - int(poss_ipadd.split('-')[0].split('.')[-1]))+1):
                    lst_correct_ipaddresses.append(str(ipadd_1a+i))

    return(lst_correct_ipaddresses)

if __name__ == "__main__":
    print(convert_ranges_to_ip_list(["10.1.1.1", "10.4.10.10-13", "192.168.1.12-192.168.1.15"]))
