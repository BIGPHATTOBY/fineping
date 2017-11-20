#!/usr/bin/python3
""" Using python as interpreter """

import os
import sys
import time
import subprocess
import _thread

### Global Variables ###

HOSTS_ARR = []


### FUNCTIONS ###

def split_second_comma(s):
    """ Split a list on every 2nd comma """

    arr = s.split(',')
    arr = [x.strip() for x in arr]

    new_arr = []
    for x, y in zip(arr[0::2], arr[1::2]):
        new_arr.append(x + ',' + y)

    return new_arr

def ping(host, desc):
    """ Ping a host without output in terminal and updating it's state """
    fnull = open(os.devnull, 'w')
    fail = subprocess.call(['ping', "-c 1", host], stdout=fnull, stderr=subprocess.STDOUT)
    if not fail:
        for item in HOSTS_ARR:
            if item[0] == host and item[1] == desc:
                item[2] = 'Connected'
    else:
        for item in HOSTS_ARR:
            if item[0] == host and item[1] == desc:
                item[2] = 'Disconnected'

def update():
    """ Updating state to host """
    longest_ip = 0
    longest_desc = 0
    for hosts in HOSTS_ARR:
        if len(hosts[0]) > longest_ip:
            longest_ip = len(hosts[0])
        if len(hosts[1]) > longest_desc:
            longest_desc = len(hosts[1])

    while True:
        pre_string = '{0:<' + str(longest_desc) + 's} | {1:' + str(longest_ip) + 's} | {2:15s}'
        print(pre_string.format('DESC.', 'IP', 'STATE'))
        pre_string = '{0:-^' + str(longest_desc + longest_ip + 18) + 's}'
        print(pre_string.format(''))
        for hosts in HOSTS_ARR:
            pre_string = '{0:<' + str(longest_desc) + 's} | {1:' + str(longest_ip) + 's} | {2:15s}'
            print(pre_string.format(hosts[1], hosts[0], hosts[2]))

        for update_hosts in HOSTS_ARR:
            _thread.start_new_thread(ping, (str(update_hosts[0]), str(update_hosts[1],)))
        time.sleep(5)
        subprocess.call('clear')



### RUNNING CODE ####

if len(sys.argv) == 1 or sys.argv[1] == '-h':
    print('-h | shows this')
    print('-s | manual host entry, sample syntax: 8.8.8.8,GoogleDNS')
    print('-S | mulitple manual host entry, sample syntax: ', end='')
    print('8.8.8.8,Google DNS,8.8.4.4,GoogleDNSBackup')
    print('-l | entry from list (file), same syntax as -s with newline as divider')
    print('Example: python3 fineping.py -S 8.8.8.8,Google,8.8.4.4,GoogleBackup')

elif sys.argv[1] == '-s':
    while True:
        _thread.start_new_thread(ping, (str(sys.argv[2].split(',')[0]), sys.argv[2].split(',')[1],))
        time.sleep(2)
        subprocess.call('clear')


elif sys.argv[1] == '-S':
    ARGV_ARR = split_second_comma(sys.argv[2])
    for items in ARGV_ARR:
        HOSTS_ARR.append([items.split(',')[0], items.split(',')[1], 'init'])
    update()


elif sys.argv[1] == '-l':
    f = open(sys.argv[2], 'r')
    for lines in f:
        formattedLine = lines.split()[0]
        HOSTS_ARR.append([formattedLine.split(',')[0], formattedLine.split(',')[1], 'init'])
    update()
