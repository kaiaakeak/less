#-*- coding: utf-8 -*-
"""
?
"""


from send_commands import send_commands

def define_params(file_src = devices.yaml, file_dst):
    with open(file_src) as f:
        devices = yaml.safe_load(f)

