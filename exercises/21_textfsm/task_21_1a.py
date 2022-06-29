# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""
from netmiko import ConnectHandler
import textfsm
from pprint import pprint


def parse_output_to_dict(template, command_output):
    result_list = []
    with open (template) as template:
        fsm = textfsm.TextFSM(template)
        parse_result = fsm.ParseText(command_output)
        headers = fsm.header
    for t in parse_result:
        temp = {}
        for e, v in enumerate(t):
            temp[headers[e]] = v
        result_list.append(temp)

    return result_list


if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    with ConnectHandler(**r1_params) as r1:
        r1.enable()
        output = r1.send_command("sh ip int br")
    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    pprint(result)