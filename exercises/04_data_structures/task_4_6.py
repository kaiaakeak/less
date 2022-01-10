# -*- coding: utf-8 -*-
"""
Задание 4.6
print(f'''
Prefix{ospf_route.split()[0]:>25}
AD/Metric{ospf_route.split()[1]:>25}
Next-Hop{ospf_route.split()[3]:>25}
Last update{ospf_route.split()[4]:>25}
Outbound Interface{ospf_route.split()[5]:>25}
''')


Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.
"""

ospf_route = "      10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
os1=ospf_route.replace(","," ").replace("[", "").replace("]", "")
os1=os1.split()

out="\n{:25} {}"*5
print(out.format(
    "Prefix", os1[0],            
    "AD/Metric", os1[1],
    "Next-Hop", os1[3],
    "Last update",os1[4],
    "Outbound Interface", os1[5]
))















