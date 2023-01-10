from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import logging
from datetime import datetime
from tabulate import tabulate
import re
import getpass



logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """

class ConnectionNetEngi():
    """Пользовательский класс для работы с сетевым оборудованием. Имеются следующие основные методы:
    send.info() - выводит список сетевых устройств.

    send_commands() - отправляет на одно устройство команды в режимах "просмотра" или "конфигурации",
    возвращает результат (тип-строка) или ошибку.

    send_commands_to_devices() -  отправляет на устройства команды (в параллельных потоках) в режимах "просмотра" или "конфигурации",
    возвращает результат (тип-строка) или ошибку.
    """
    def __init__(self, dict_dicts_of_devices):
        self.devices = self._define_devices(dict_dicts_of_devices)
        self.hosts = [host['host'] for host in self.devices]
        auth_params = {
            "username": input("Введите имя пользователя: "),
            "password": getpass.getpass("Введите пароль: "),
        }
        [dev.update(auth_params) for dev in self.devices]

    def __iter__(self):
        return iter(self.devices)

    def info(self):
        for e, hsts in enumerate(self.hosts, 1):
            print(e, hsts)

    def _define_devices(self, dict_dicts_of_devices):
        if not isinstance(dict_dicts_of_devices, dict):
            raise TypeError(
                f"unsupported operand type(s): 'params of devices' and '{type(other).__name__}'")
        hosts_re = input(
            "Enter the hostnames devices for executing operations in format is re (hostname, exmpl=cis\d+.+ ):"
        )
        return [dict_dicts_of_devices.get(hostname) for hostname in dict_dicts_of_devices if re.search(hosts_re, hostname)]

    def _check_err_in_cmd(self, host, command, result):
        regex = "% (?P<err>.+)"
        message = (
            'При выполнение команды "{cmd}" на устройстве "{dev}" '
            'возникла ошибка "{error}" '
        )

        err_in_cmd = re.search(regex, result)
        if err_in_cmd:
            raise ErrorInCommand(
                message.format(
                    cmd=command, dev=host, error=err_in_cmd.group('err')
                )
            )

    def send_commands(self, device, show=None, config=None, ignore_err=False, *args, **kwargs):
        """Function for send commands (config or show).
        Return the result (type=str) of executing commands

        Keywords argument:
        show - command mode "view"
        config - command mode "conf t"
        *args
        **kwargs
        """
        start_msg = '===> {} Connection: {}'
        recevied_msg = '<=== {} Received:    {}'
        ip = device.get('host')

        logging.info(start_msg.format(datetime.now().time(), ip))

        result_show_cmd = """{host}{cmd}\n{out_cmd}\n"""
        result = str()
        try:
            with ConnectHandler(**device) as ssh:
                ssh.enable()
                if show and config:
                    raise ValueError('Nessery only one argument show or config\n')
                elif show:
                    if isinstance(show, str):
                        show = [show,]
                    hostname = ssh.find_prompt()
                    for show_command in show:
                        output = ssh.send_command(show_command)
                        if not ignore_err:
                            self._check_err_in_cmd(device['host'], show_command, output)
                        result = result + result_show_cmd.format(
                            host = hostname,
                            cmd=show_command,
                            out_cmd=output
                        )
                elif config:
                    if isinstance(config, str):
                        config = [config,]
                    for cfg_command in config:
                        out_cfg = ssh.send_config_set(cfg_command, *args, exit_config_mode = False,  **kwargs)
                        if not ignore_err:
                            self._check_err_in_cmd(device['host'], sfg_command, out_cfg)
                        result = result + cfg_command
                    ssh.exit_config_mode()
                logging.info(recevied_msg.format(datetime.now().time(), ip))

            return result
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as err_netmiko:
            print(f"{'='*50}\n\n'{err_netmiko}'")


if __name__ == "__main__":
    devices_params = {
        'cis01abk': {
            'device_type': 'cisco_ios',
            'ip': '192.168.100.1',
            'host': 'cis01abk',
            'secret': 'cisco'},
    'cis02abk':
            {'device_type': 'cisco_ios',
            'ip': '192.168.100.2',
            'host': 'cis02abk',
            'secret': 'cisco'},
    'cisl03reb':
            {'device_type': 'cisco_ios',
            'ip': '192.168.100.3',
            'host': 'cisl03reb',
            'secret': 'cisco'},
    'cisl02ss':
            {'device_type': 'cisco_ios',
            'ip': '192.168.100.2',
            'host': 'cisl02ss',
            'secret': 'cisco'},
    'cisn01eb':
            {'device_type': 'cisco_ios',
            'ip': '192.168.100.1',
            'host': 'cisn01eb',
            'secret': 'cisco'}}