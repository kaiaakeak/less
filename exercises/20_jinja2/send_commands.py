#-*- coding: utf-8 -*-
"""
Функция возвращает строку с выводом команд show или config
В качестве аргументов принимает список с параметрами устройств, как ключевые передаются список команд на просмотр конфигураций
или на выполнение конфигураций
"""
from datetime import datetime
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import yaml
import logging


logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


def send_commands(device, *, show = None, config = None):
    start_msg = '============> {} Connection: {}'
    received_msg = '<============ {} Received:  {}'
    ip = device['host']
    output = str()
    out = "{}{}\n{}\n"
    logging.info(start_msg.format(datetime.now().time(), ip))

    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            if show and config:
                raise ValueError("должен передаваться только один из аргументов show или config")
            elif show:
                if type(show) == str:
                    show=[show]
                for show_command in show:
                    hostname = ssh.find_prompt()
                    result = ssh.send_command(show_command)
                    output = output + out.format(hostname, show_command, result)
            elif config:
                output = ssh.send_config_set(config)

            logging.info(received_msg.format(datetime.now().time(), ip))
        return output

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


commands_config = ['router ospf 55', 'no network 0.0.0.0 255.255.255.255 area 0', 'exit', 'no router ospf 55']
commands_show = ['sh int des', 'sh ip int bri | ex una']


if __name__ == "__main__":
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)

    print(send_commands(devices[0], config=commands_config))
    print(send_commands(devices[1], show=commands_show))