#!/usr/bin/env python3
from sys import argv

ignore = ["duplex", "alias", "configuration"]
src_file = argv[1]
dst_file = argv[2]
with open(src_file) as f:
    with open(dst_file, 'w') as df:
        for line in f:
            check = True
            for word_ignore in ignore:
                if word_ignore in line or line.startswith('!'):
                    check = False
            if check:
                df.write(line)
