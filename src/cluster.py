from telnetlib import Telnet
from threading import Thread
from time import sleep
import redis

def clustersearch():
    """Starts the dx-cluster in a seperate thread"""
    print("Try to start cluster")
    thread = Thread(target=dxcluster)
    thread.start()
    print("JO")


def user_cluster(user_id): 
    """Checks if callsigns in user list match callsigns in master list"""
    r = redis.StrictRedis(host='localhost', port=6379, db=0)   
    user_id = "BUCKET:" + str(user_id)
    try: 
        user = r.get(user_id).decode('utf-8')
    except  AttributeError: #TODO report error to higher function instead of ""
        user = ""
    r.set(user_id,"")
    return user


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
            get_dxcc(output)


def get_call(clusteroutput): 
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    
    call = clusteroutput.split()[4]
    test = r.get(call)
    if test != None:
        for i in test.decode("utf-8").split(" "):
            key = "BUCKET:"+ i
            r.append(key, clusteroutput)
            print(key)


def get_dxcc(clusteroutput):
    formated_output = clusteroutput.split()[4]
    print(formated_output)


def reset_callsignlist():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set("CALLSIGNS", "") 



