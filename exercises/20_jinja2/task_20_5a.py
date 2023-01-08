# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import yaml
from pprint import pprint

from send_commands import send_commands
from task_20_1 import generate_config

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    #cfg_src = generate_config(src_template, vpn_data_dict)
    #cfg_dst = generate_config(dst_template, vpn_data_dict)
    tu_src = (send_commands(src_device_params, show='sh int des | i Tu'))
    tu_dst = (send_commands(dst_device_params, show='sh int des | i Tu'))
    data_src, data_dst = vpn_data_dict, vpn_data_dict

    if tu_src:
         tu_n_src = re.findall(r'Tu(\d+).*', tu_src)
    else:
        tu_n_src = None
    commands = {
    src_device_params['host'] : {'command' : generate_config(src_template, vpn_data_dict)},
    dst_device_params['host'] : {'command' : generate_config(dst_template, vpn_data_dict)}}
    print(send_commands(src_device_params, config=commands[src_device_params['host']]['command']))
    print(send_commands(dst_device_params, config=commands[dst_device_params['host']]['command']))
    return commands[src_device_params['host']]['command'] , commands[dst_device_params['host']]['command']



data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}


if __name__ == "__main__":
    with open ("devices.yaml") as f:
        devices = yaml.safe_load(f)
    pprint (configure_vpn(devices[0], devices[1], "./templates/gre_ipsec_vpn_1.txt", "./templates/gre_ipsec_vpn_2.txt", data))