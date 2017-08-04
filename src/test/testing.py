import redis

def generate_master_list2():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    s = set()
    for name in r.keys("CALLS:*"):
        print(name.decode("utf-8").replace("CALLS:",""))
        data = r.smembers(name).decode('utf-8') ##Auto
        for item in data.split():
            s.add(item)
        print(s)
    return list(s)


def get_all_chats_ids():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    ids = list()
    for name in r.keys("CALLS:*"):
        ids.append(name.decode("utf-8").replace("CALLS:",""))
    return ids

#print(generate_master_list2())
#print(get_all_chats_ids())


def user_cluster():
    masteroutput = ["DD5HT CLUSTERSTUFF", "DM5EE CLUSTERSTUFF", "DL0IU CLUSTERSTUFF"]
    
    user0 = ["DL0IU", "DD5HT"]
    user1 = ["DL0IU", "DM5EE"]
    userlist = [user0, user1]
    
    for i in masteroutput:
        for user in userlist: #ALL Users
            for call in user: #ALL Calls
                if call in i: #Check if Call Matches                 
                    print("WRITE to USERID "+ i) ####WE CAN AVOID ONE LOOP IF WE ADD AN IDENTIFER TO EACH DX CLUSTER ENTRY



user_cluster()