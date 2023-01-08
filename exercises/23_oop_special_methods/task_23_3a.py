# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""

class Topology():
    "Class for create topology from dict of links"
    def __init__(self, dict_links):
        self.topology = self._topology_normalize(dict_links)

    def _topology_normalize(self, all_links):
        return {min(link_L, link_R) : max(link_L, link_R) for link_L, link_R in all_links.items()}

    def delete_link(self, local, remote):
        if local in self.topology:
            del self.topology[local]
        elif remote in self.topology:
            del self.topology[remote]
        else:
            print('Такого соединения нет')

    def delete_node(self, node):
        temp_k = [l for l, r in self.topology.items() if node in (l+r)]
        if temp_k:
            for k in temp_k:
                del self.topology[k]
        else:
            print('Такого устройства нет')

    def add_link(self, local, remote):
        if self.topology.get(local) == remote or self.topology.get(remote) == local:
            print('Такое соединение существует')
        elif local in (self.topology.keys() | self.topology.values()) or remote in (self.topology.keys() | self.topology.values()):
            print('Cоединение с одним из портов существует')
        else:
            self.topology[local] = remote

    def __add__(self, other):
        return Topology({**self.topology, **other.topology})

    def __iter__(self):
        return iter(self.topology.items())

    def __getitem__(self, index):
        return self.topology.items()[index]

if __name__ == "__main__":

    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }

    topology_example2 = {
        ("R1", "Eth0/4"): ("R7", "Eth0/0"),
        ("R1", "Eth0/6"): ("R9", "Eth0/0"),
    }
    t1 = Topology(topology_example)
    for n in t1:
        print(n)