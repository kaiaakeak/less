# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
result={}
out="\n{:25} {}"*5

with open('ospf.txt') as f:
    for line in f:
        line = line.replace('[','').replace(']','').replace(',','')
        line = line.split()
        type_protocol, prefix, metric, via, nexthop, lastupd, outintf = line
        print(out.format(
        "Prefix", line[1],            
        "AD/Metric", line[2],
        "Next-Hop", line[4],
        "Last update", line[5],
        "Outbound Interface", line[6],
        ))

