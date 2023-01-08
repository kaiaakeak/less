# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
import re


from netmiko.cisco.cisco_ios import CiscoIosSSH


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super().__init__(**device_params)
        self.enable()

    def _check_error_in_command(self, cmd, out_cmd):
        regex = (r'(?P<err>%\s+\S+.+)(?:\n)?')
        msg_err = 'Была обнаружена ошибка "{err}" на устройстве "{device}" при вызове команды "{cmd}"'
        match = re.search(regex, out_cmd)
        if match:
            raise ErrorInCommand(msg_err.format(err=match.group('err'), device=self.host, cmd=cmd))

    def send_command(self, cmd, *args, **kwargs):
        out = super().send_command(cmd, *args, **kwargs)
        self._check_error_in_command(cmd, out)
        return out

    def send_config_set(self, cmd, *args, **kwargs):
        if isinstance(cmd, str):
            cmd = [cmd]
        result = list()
        for cmd_n in cmd:
            out = super().send_config_set(cmd_n,  exit_config_mode = False)
            self._check_error_in_command(cmd_n, out)
            result.append(out)
        return result


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """

if __name__ == "__main__":
    device_params = {
        "device_type": "cisco_ios",
        "ip": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }
    r1 = MyNetmiko(**device_params)
    commands = ['int fa0/1', 'no ip addr 10.252.245.2/30', 'do sh ip int bri']
    print(r1.send_config_set(commands))