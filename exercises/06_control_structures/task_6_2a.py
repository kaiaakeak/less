# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса.
Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'

Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.
Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip=input('Enter ip address in format x.x.x.x \n')
correct_ip=len(ip.split('.'))==4
for i in ip.split('.'):
    correct_ip= i.isdigit() and 0 <= int(i) <= 255 and correct_ip
    
if correct_ip:
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
else:
    print('Неправильный IP-адрес')
