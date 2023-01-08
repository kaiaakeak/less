# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
from itertools import repeat
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import yaml
from pprint import pprint
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_show_command(device, command):
    out = "{}{}\n{}"
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device["host"]
    logging.info(start_msg.format(datetime.now().time(), ip))

    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            hostname = ssh.find_prompt()
            result = ssh.send_command(command)
            logging.info(received_msg.format(datetime.now().time(), ip))
            result = out.format(hostname, command, result)
        return result
    except NetMikoAuthenticationException as err:
        logging.warning(err)


def send_show_command_to_devices(devices, command, filename, limit=3):
        with ThreadPoolExecutor(max_workers=limit) as executor:
            result = executor.map(send_show_command, devices, repeat(command))
            list_result = [[device['host'], res] for device, res in zip(devices, result)]
        with open(filename, 'w') as file:
            for temp in list_result:
                file.write(temp[-1]+('\n'))



if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices  = yaml.safe_load(f)

    pprint(send_show_command_to_devices(devices, 'sh ip int br', 'temp.txt'))