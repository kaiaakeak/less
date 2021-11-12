# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ipaddr_prefix=input("Enter ip address and prefix (format is x.x.x.x/xx): ")
ip, mask=ipaddr_prefix.split('/')
ip_list=ip.split('.')
mask=int(mask)
bin_mask=("1"*mask)+("0"*(32-mask))
out_ip="""
    Network:
    {0:8} {1:8} {2:8} {3:8}
    {0:08b} {1:08b} {2:08b} {3:08b}
"""
out_mask="""
    Mask:
    {4}
     {0:8} {1:8} {2:8} {3:8}
    {0:08b} {1:08b} {2:08b} {3:08b}
"""
oct1=int(bin_mask[0:8],2)
oct2=int(bin_mask[8:16],2)
oct3=int(bin_mask[16:24],2)
oct4=int(bin_mask[24:],2)
print(out_ip.format(int(ip_list[0]), int(ip_list[1]), int(ip_list[2]), int(ip_list[3])))
print(out_mask.format(oct1, oct2, oct3, oct4, mask))
