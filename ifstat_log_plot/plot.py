#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print 'usage:'
    print '    <this.py> <log file name> - handle log file and generate <log file name>.csv'

try:
    log_name = sys.argv[1]
except Exception as e:
    print e.message

result = []

with open(log_name, 'r') as log_file: 
    # interface
    interfaces = log_file.readline().split()
    # KB/s in/out
    log_file.readline()
    # data start
    data = log_file.readlines()
    
    for interface in interfaces:
        result.append({'interface': interface+'_in', 'data': []})
        result.append({'interface': interface+'_out', 'data': []})
    for row in data:
        row_splited = row.split()
        # filter
        try:
            float(row_splited[0])
        except ValueError:
            print row_splited[0] + 'is not a float'
            continue
        # 
        for index, speed in enumerate(row_splited):
            result[index]['data'].append(float(speed))
            
# print result

plot_index = 1
total_interface_number = len(result)/2
'''
for record in result:
    plt.subplot(total_interface_number, 2, plot_index)
    plt.title(record['interface'])
    plt.plot(record['data'])
    
    plot_index += 1

'''
y = result[6]['data']
print y
plt.plot(y)


plt.show()
        