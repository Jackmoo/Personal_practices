#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess as sub
import select
import time


log_name = 'ifstat.log.' + str(time.time())
cmd_obj = sub.Popen('ifstat', bufsize=1, stdin=sub.PIPE, stdout=sub.PIPE, shell=True)

with open(log_name, 'w+', 4096) as log_file:
    while True:
        reads = [cmd_obj.stdout.fileno()]
        read_fds = select.select(reads, [], [])[0]
        output = cmd_obj.stdout.readline()
        print output
        log_file.write(output)
        log_file.flush()
