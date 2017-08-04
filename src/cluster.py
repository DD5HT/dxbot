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

def generate_master_list():
    """Generates a list with all callsigns from all users which is used to match with the dxcluster output"""
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    s = set()
    for name in r.keys("CALLS:*"): #Matches all CALL KE
        #print(name.decode("utf-8").replace("CALLS:", ""))
        data = r.get(name).decode('utf-8')
        for item in data.split():
            s.add(item)
    #print(s)
    return list(s)

def get_matches():
    """Returns all DX spots generated out of the master list"""
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = []
    try:
        stringdata = r.get("CALLSIGNS").decode('utf-8') ##
        data = stringdata.split(u";;;;;")
        #data = data + "\n"
    except AttributeError:
        print("Missing CALLSIGNS KEY")
        print("Finally will create a new KEY")
    finally:
        return data # pylint: disable=W0150


def user_cluster(user_id):
    """Checks if callsigns in user list match callsigns in master list"""
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
 
    masteroutput = get_matches()
    
    user_id = "CALLS:" + str(user_id)
    user = r.get(user_id).decode('utf-8')
    user = user.split()

    bucket = []
    for entries in masteroutput:
        for call in user: #ALL Calls
            if call in entries: #Check if Call Matches !!!PROBLEM MASTER LISTE WIRD NACH JEDEM AUFRUF GELÖSCHT !!!!!
                print("We got a Match")
                print(entries)
                bucket.append(entries)
                print(bucket)
    
    answer = ""
    for i in bucket:
        answer = answer + str(i)
        print("IT WORKS NOW" + answer)
    return answer

def dxcluster():#TODO retry if internet drops
    """Starts the DX-Cluster"""
    CALLSIGN = b"DD5HT"
    AMOUNT = 10000
    
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
            #output = output.replace("\r\n", "")  ##WHY ?!
            for call in generate_master_list():
            
                if call in output:
                    print(str(i) + " FOUND")
                    #print(output)
                    matchedcall(output)
            #print(output)
    

def matchedcall(clusteroutput):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    clusteroutput = clusteroutput +";;;;;"
    print(clusteroutput)
    r.append("CALLSIGNS",clusteroutput)

def reset_callsignlist():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set("CALLSIGNS", "") 