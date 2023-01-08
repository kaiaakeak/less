# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из любого задания 22.2x и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""
import telnetlib
import time


class CiscoTelnet():
    def __init__(self, **params):
        self.ip = self._check_ip(params['ip'])
        self.username = params['username']
        self.password = params['password']
        self.secret = params['secret']
        self.telnet = telnetlib.Telnet(self.ip)
        self.telnet.read_until(b"Username")
        self._write_cmd(self.username)
        self.telnet.read_until(b"Password")
        self._write_cmd(self.password)
        self.telnet.read_until(b">", timeout=5)
        self._write_cmd('enable')
        self.telnet.read_until(b"Password")
        self._write_cmd(self.secret)
        #self.telnet.write(b"terminal length 0\n")
        self.telnet.read_until(b"#", timeout=5)
        self.telnet.read_very_eager()
    def _check_ip(self, ip_check):
        octets = [
                  octet for octet in ip_check.split('.') if octet.isdigit() and 0 <= int(octet) <= 255
                  ]
        if len(octets) == 4:
            return ip_check
        else:
            raise ValueError('Incorrect IPv4 address')

    def _write_cmd(self, line):
        self.telnet.write(line.encode("utf-8") + b"\n")

    def send_show_command(self, command, parse=False, templates="templates", index="index"):
        self._write_cmd(command)
        time.sleep(1)
        command_output = self.telnet.read_very_eager().decode("ascii")
        if not parse:
            return command_output
        attributes = {"Command": command, "Vendor": "cisco_ios"}
        cli = clitable.CliTable("index", templates)
        cli.ParseCmd(command_output, attributes)
        return [dict(zip(cli.header, row)) for row in cli]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.telnet.close()