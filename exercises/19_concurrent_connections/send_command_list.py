# -*- coding: utf-8 -*-
"""
Функция для
"""
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import yaml
from pprint import pprint
import logging
from datetime import datetime


logging.basicConfig(
    format = '%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_show_command(device, commands):
    out = "{}{}\n{}"
    start_msg = '===> {} Connection: {}'
    received_msg = '<=== {} Received:   {}'
    ip = device["host"]
    output = str()
    logging.info(start_msg.format(datetime.now().time(), ip))


    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            hostname = ssh.find_prompt()
            if type(commands) == list:
                for command in commands:
                    result = ssh.send_command(command)
                    result = out.format(hostname, command, result)
                    output = output + '\n' + result
            elif type(commands) == str:
                result = ssh.send_command(commands)
                result = out.format(hostname, commands, result)
                output = output + '\n' + result

            logging.info(received_msg.format(datetime.now().time(), ip))
        return output
    except NetmikoAuthenticationException or NetmikoTimeoutException as err:
        logging.warning(err)


if __name__ == "__main__":
    with open("devices.yaml") as file_src:
        devices = yaml.safe_load(file_src)

    print(send_show_command(devices[0], 'sh int des'))