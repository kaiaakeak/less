from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import logging
from datetime import datetime, date
import re
import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


class ConnectionNetEngi:
    """Пользовательский класс для работы с сетевым оборудованием. Имеются следующие основные методы:
    send.info() - выводит список сетевых устройств.

    send_commands() - отправляет на одно устройство команды в режимах "просмотра" или "конфигурации",
    возвращает результат (тип-строка) или ошибку.

    send_commands_to_devices() -  отправляет на устройства команды (в параллельных потоках) в режимах "просмотра" или
    "конфигурации", возвращает результат (тип-строка) или ошибку.
    """

    def __init__(self, dict_dicts_of_devices):
        self.devices = self._define_devices(dict_dicts_of_devices)
        self.hosts = [host['host'] for host in self.devices]
        auth_params = {
            "username": input("Введите имя пользователя: "),
            "password": getpass.getpass("Введите пароль: "),
        }
        [dev.update(auth_params) for dev in self.devices]
        logging.basicConfig(
            format='%(threadName)s %(name)s %(levelname)s: %(message)s',
            level=logging.INFO)

    def __iter__(self):
        return iter(self.devices)

    def info(self):
        for e, hsts in enumerate(self.hosts, 1):
            print(e, hsts)

    def _define_devices(self, dict_dicts_of_devices):
        if not isinstance(dict_dicts_of_devices, dict):
            raise TypeError(
                f"unsupported operand type(s): 'params of devices' and '{type(dict_dicts_of_devices).__name__}'")
        hosts_re = input(
            "Enter the hostnames devices for executing operations in format is re (hostname, exmpl=cis\d+.+ ):"
        )
        return [dict_dicts_of_devices.get(hostname) for hostname in dict_dicts_of_devices if
                re.search(hosts_re, hostname)]

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
        """Sends commands (config or show).

        Parameters
        ----------
        device : dict
            Dictionaries containing device parameters.
        show : str or list
            view mode command(s).
        config : str or list
            configuration mode command(s).
        ignore_err : bool (True or False)
            Flag affects ignoring errors in device output.
        *args : list
            The same *args that you might provide to the netmiko.ssh_dispatcher.ConnectHandler.
        **kwargs : Dict
            The same *kwargs that you might provide to the netmiko.ssh_dispatcher.ConnectHandler.

        Returns
        ----------
        result : str
            The result of executing commands
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
                        show = [show, ]
                    hostname = ssh.find_prompt()
                    for show_command in show:
                        output = ssh.send_command(show_command)
                        if not ignore_err:
                            self._check_err_in_cmd(device['host'], show_command, output)
                        result = result + result_show_cmd.format(
                            host=hostname,
                            cmd=show_command,
                            out_cmd=output
                        )
                elif config:
                    if isinstance(config, str):
                        config = [config, ]
                    for cfg_command in config:
                        out_cfg = ssh.send_config_set(cfg_command, *args, exit_config_mode=False, **kwargs)
                        if not ignore_err:
                            self._check_err_in_cmd(device['host'], cfg_command, out_cfg)
                        result = result + cfg_command
                    ssh.exit_config_mode()
                logging.info(recevied_msg.format(datetime.now().time(), ip))

            return result
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as err_netmiko:
            print(f"{'=' * 50}\n\n'{err_netmiko}'")

    def copy_config_scp_cisdev(self, device, cmd_copy):
        """Sends a command to save the device configuration (ru or startup) to a remote server via SCP

        Parameters
        ----------
        device : dict
            Dictionary containing device parameters.
        cmd_copy : str
            Command to save the device configuration (ru or startup) to a remote server via SCP.

        Returns
        ----------
        result : str
            The result as a string of execution command
        """
        start_msg = '===> {} Connection: {}'
        recevied_msg = '<=== {} Received:    {}'
        ip = device.get('host')
        logging.info(start_msg.format(datetime.now().time(), ip))
        try:
            with ConnectHandler(**device) as ssh:
                hostname = ssh.find_prompt()
                command = f"{cmd_copy}{hostname.replace('#','')}-config_{str(date.today()).replace('-','')}"
                """
                cmd_copy - copy ru scp://fw_saver:fwsave_ftp@10.252.246.27/config_SCP_ONLY/cisco/lpu/
                ip - pm-swc01hq
                copy ru scp://fw_saver:fwsave_ftp@10.252.246.27/config_SCP_ONLY/cisco/lpu/pm-swc01hq-config_20230111
                """
                result = ssh.send_command_timing(command, strip_prompt=False, strip_command=False)
                result += ssh.send_command_timing("\n", strip_prompt=False, strip_command=False)
                result += ssh.send_command_timing("\n", strip_prompt=False, strip_command=False)
                result = f"{hostname}\n{result}\n"
                logging.info(recevied_msg.format(datetime.now().time(), ip))

            return result
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as err:
            print('='*30, '\n', err)

    def send_commands_to_devices(self, devices, filename_dst, *, show=None, config=None, limit=3):
        """Sends commands(config or show) to multiple devices through concurrent.futures.ThreadPoolExecutor

        Parameters
        ----------
        devices : list
            List of dictionaries containing device parameters;
        filename_dst : str
            Name of the file to save the result
        show : str or list
            view mode command(s).
        config : str or list
            configuration mode command(s).
        limit : int
            number of threads.

        Returns
        ----------
        result : list
            The result as a list of execution commands for multiple devices
        """
        limit = int(limit)
        with ThreadPoolExecutor(max_workers=limit) as executor:
            future_ssh = [
                executor.submit(self.send_commands, device, show=show, config=config) for device in devices
            ]
            result_list = [
                future.result() for future in as_completed(future_ssh)
            ]

        with open(filename_dst, 'w') as dst:
            for line in result_list:
                if line:
                    dst.write(line)

        return result_list

    def copy_config_scp_cis_multidevices(self, devices, cmd_copy, limit=3):
        """Sends a command to save the multiple devices configuration (ru or startup) to a remote server via SCP

        Parameters
        ----------
        devices : list
            List of dictionaries containing device parameters.
        cmd_copy : str
            Command to save the device configuration (ru or startup) to a remote server via SCP.
        limit : int
            number of threads.

        Returns
        ----------
        result : list
            The result as a list of execution commands for multiple devices
        """
        limit = int(limit)
        with ThreadPoolExecutor(max_workers=limit) as executor:
            future_ssh = [
                executor.submit(self, send_wr_cfg_scp, device, cmd_copy) for device in devices
            ]
            result_list = [
                future.result() for future in as_completed(future_ssh)
            ]

        return result


if __name__ == "__main__":
    devices_params = {
        'pm-swc01hq': {
            'device_type': 'cisco_ios',
            'ip': '192.168.100.1',
            'host': 'pm-swc02hq',
            'secret': 'cisco'},
        'pm-swc02hq':
            {'device_type': 'cisco_ios',
             'ip': '192.168.100.2',
             'host': 'pm-swc02hq',
             'secret': 'cisco'},
        'l-swc03kp':
            {'device_type': 'cisco_ios',
             'ip': '192.168.100.3',
             'host': 'l-swc03kp',
             'secret': 'cisco'},
        'l-swc02ss':
            {'device_type': 'cisco_ios',
             'ip': '192.168.100.2',
             'host': 'l-swc02ss',
             'secret': 'cisco'},
        'ne-swc01abk':
            {'device_type': 'cisco_ios',
             'ip': '192.168.100.1',
             'host': 'ne-swc01abk',
             'secret': 'cisco'}}
