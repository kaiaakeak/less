# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
while True:
    ip=input('Enter ip address in format x.x.x.x \n')
    correct_ip=len(ip.split('.'))==4
    for i in ip.split('.'):
        correct_ip= i.isdigit() and 0 <= int(i) <= 255 and correct_ip
        
    if correct_ip:
        break
    print('Неправильный IP-адрес')
                
if int(ip.split('.')[0]) <=223 and int(ip.split('.')[0]) !=0:
    print('unicast')
elif int(ip.split('.')[0]) >= 224 and int(ip.split('.')[0]) <= 239 and int(ip.split('.')[0]) != 0:
    print('multicast')
elif ip == "255.255.255.255":
    print('local broadcast')
elif ip == "0.0.0.0":
    print('unassigned')
else:
    print('unused')
