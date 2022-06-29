# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from textfsm import clitable
import yaml
from pprint import pprint
from datetime import datetime
import logging

from task_21_3 import parse_command_dynamic

#logging.basicConfig(
#    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
#    level=logging.INFO)

def send_and_parse_show_command(
    device_dict, command, templates_path='/home/python/venv/pyneng-py3-7/lib/python3.7/site-packages/ntc_templates/templates', index='index'
    ):

    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device_dict["host"]
    #logging.info(start_msg.format(datetime.now().time(), ip))

    attributes = {'Command': command, 'Platform': device_dict['device_type']}
    ssh = ConnectHandler(**device_dict)
    try:
        ssh.enable()
        cmd_out = ssh.send_command(command)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as err:
        print(err)
    #logging.info(received_msg.format(datetime.now().time(), ip))
    return parse_command_dynamic(cmd_out, attributes, index_file = index, templ_path = templates_path)


if __name__=="__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)

    for d in devices:
        print(send_and_parse_show_command(d, 'sh ip int br'))