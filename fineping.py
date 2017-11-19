#!/usr/bin/python3
""" Using python as interpreter """

import os
import sys
import time
import subprocess
import _thread


def ping(host, desc):
    """ Ping a host without output in terminal """
    fnull = open(os.devnull, 'w')
    fail = subprocess.call(['ping', "-c 1", host], stdout=fnull, stderr=subprocess.STDOUT)
    if not fail:
        print('ping to ' + host + ' ' + desc + ' is gut', flush=True)
    else:
        print('wth', flush=True)



if sys.argv[1] == '-s':
    while True:
        _thread.start_new_thread(ping, (str(sys.argv[2].split(',')[0]), sys.argv[2].split(',')[1],))
        time.sleep(2)
        subprocess.call('clear')

if sys.argv[1] == '-S':
    ARGVLIST = sys.argv[2].split(",")
    ARGVTHREAD = []
    ARGVTHREAD.append([",".join(ARGVLIST[i:i+2]) for i in range(0, len(ARGVLIST), 2)])
    for item in ARGVTHREAD:
        print(item)
    #for x in ARGVTHREAD.split(' '):
    #    print('t')
    #while True:
    #    _thread.start_new_thread(ping, (str(sys.argv[2].split(',')[0]), sys.argv[2].split(',')[1],))
    #    time.sleep(2)
    #    subprocess.call('clear')

elif len(sys.argv) == 1 or sys.argv[1] == '-h':
    print('-h | shows this')
    print('-s | manual host entry, sample syntax: 8.8.8.8,GoogleDNS')
    print('-S | mulitple manual host entry, sample syntax: ', end='')
    print('8.8.8.8,Google DNS,8.8.4.4,GoogleDNSBackup')
    print('-l | entry from list (file), same syntax as -s with newline as divider')
