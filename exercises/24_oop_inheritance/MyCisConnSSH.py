from netmiko.cisco.cisco_ios import CiscoIosSSH
import logging
from datetime import datetime
import re


logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)


class MyCisConnSSH(CiscoIosSSH):
    def __init__(self, **device_params):
        params = {
            "username": "Введите имя пользователя: ",
            "password": "Введите пароль: ",
        }
        for param in params:
            if not param in device_params:
                device_params[param] = input(params[param])
        super().__init__(**device_params)
        if device_params.get('secret'):
            self.enable()

    def send_commands(self, show=None, config=None, *args, **kwargs):
        """Function for send commands (config or show).
        Return the result (type=str) of executing commands

        Keywords argument:
        show - command mode enable
        config - command mode conf t
        *args
        **kwargs
        """
        start_msg = '===> {} Connection: {}'
        recevied_msg = '<=== {} Received:    {}'
        ip = self.host
        logging.info(start_msg.format(datetime.now().time(), ip))

        result = str()
        if show and config:
            raise ValueError('Nessery only one argument show or config\n')
        elif show:
            result_show_cmd = """{host}{cmd}\n{out_cmd}\n"""
            if isinstance(show, str):
                show = [show,]
                hostname = self.find_prompt()
                for show_cmd in show:
                    output = super().send_command(show_cmd, *args, **kwargs)
                    self._check_err_in_cmd(show_cmd, output)
                    result = result + result_show_cmd.format(host=hostname, cmd=show_cmd, out_cmd=output)
        elif config:
            if isinstance(config, str):
                config = [config,]
            for cfg_cmd in config:
                out_cfg = super().send_config_set(cfg_cmd, *args, exit_config_mode = False,  **kwargs)
                self._check_err_in_cmd(cfg_cmd, out_cfg)
                result = result + out_cfg
            self.exit_config_mode()
        logging.info(recevied_msg.format(datetime.now().time(), ip))

        return result

    def _check_err_in_cmd(self, command, result):
        regex = "% (?P<err>.+)"
        message = (
            'При выполнение команды "{cmd}" на устройстве "{dev}" '
            'возникла ошибка "{error}" '
        )

        err_in_cmd = re.search(regex, result)
        if err_in_cmd:
            raise self.ErrorInCommand(
                message.format(
                    cmd=command, dev=self.host, error=err_in_cmd.group('err')
                )
            )

    def ErrorInCommand(self, Exception):
        """Исключение генерируется, если при выполнение комадны на оборудовании, возникла ошибка.
        """

