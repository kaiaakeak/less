# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""
import subprocess
from concurrent.futures import ThreadPoolExecutor


#logging.basicConfig(
    #format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    #level=logging.INFO)

def ping_ip_only_1(ip_address):
    result1 = subprocess.run(['ping', '-c', '3', ip_address], stdout=subprocess.DEVNULL)
    if result1.returncode == 0:
        return True
    else:
        return False


def ping_ip_addresses(ip_list, limit=3):
    list_available=[]
    list_notavailable=[]

    with ThreadPoolExecutor(max_workers = limit) as executor:
        result = executor.map(ping_ip_only_1, ip_list)
        list_results=[[ip_add, available] for ip_add, available in zip(ip_list, result)]
        for temp in list_results:
            if temp[-1]:
                list_available.append(temp[0])
            elif not temp[-1]:
                list_notavailable.append(temp[0])
    return list_available, list_notavailable

list_ip_addresses = ['192.168.100.1', '192.168.100.211', '192.168.100.3', '192.168.100.121', '192.168.100.2']

if __name__ == "__main__":
    print(ping_ip_addresses(list_ip_addresses, 5))