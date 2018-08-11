#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from telnetlib import Telnet
from time import sleep
from sys import argv

def dxcluster():#TODO retry if internet drops
    """Starts the DX-Cluster"""
    CALLSIGN = b"DD5HT"
    AMOUNT = 100000
    
    print("DX-Cluster started!")
    with Telnet('cluster.dl9gtb.de', 8000) as tn:
        #login into dx cluster
        sleep(0.5)
        print(tn.read_very_eager().decode('utf-8'))
        tn.write(CALLSIGN + b'\r\n')
        sleep(0.5)
        print(tn.read_until(b'arc6>\r\n').decode('utf-8'))
        #now dx messages are comming
        for i in range(0,AMOUNT):
            output = tn.read_until(b'\n').decode('utf-8')
            get_call(output)

def get_call(clusteroutput):
    formated_output = []
    for i in clusteroutput.split():
        formated_output.append(i)
    
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    call = formated_output[4]
    print(call)
    test = r.get(call)
    if test != None:
        for i in test.decode("utf-8").split(" "):
            key = "BUCKET:"+ i
            r.append(key, clusteroutput+";*;*;*;*;")
            print(key)

dxcluster()
