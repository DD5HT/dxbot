import redis

def create_user(user_id):
    """Creates a new user account in the database"""
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    user_id_calls = "CALLS:" + str(user_id)
    user_id_dxcc = "DXCC:" + str(user_id)
    r.set(user_id_calls, "")
    r.set(user_id_dxcc, "")

    success = "Your account was created successfully, good DX!"
    return success

def add_call(user_id, call):
    """Adds new call in capitals to the database"""
    user_id = "CALLS:" + str(user_id)
    call = call.upper() + " "

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.append(user_id, call)

    newcall = "Added: " + call +"to callsign list"
    return newcall


def delete_call(user_id, call): #TODO remove more than one call with one command
    user_id = "CALLS:" + str(user_id) 
    call = call.upper() + " "
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    new_calls = r.get(user_id).decode("utf-8")
    new_calls = new_calls.replace(call, "")
    r.set(user_id, new_calls)
    newcall = "Removed: " + call +"from callsign list"
    return newcall

def get_calls(user_id):
    user_id = "CALLS:" + str(user_id) 
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = r.get(user_id).decode('utf-8')
    failstring = "You have entered no calls so far!"
    if data:
        data = data.split()  #TODO sort after 
        data.sort()
        data = "  ".join(data)
        return data
    else:
        return failstring

def add_dxcc(user_id, dxcc):
    """Adds new dxcc to the database"""
    user_id = "DXCC:" + str(user_id)
    dxcc = dxcc.upper() + " "
    #TODO Check if DXCC is in list:
    #TODO Generate DXCC name
    
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.append(user_id, dxcc)

    new_dxcc = "Added: " + dxcc +"to dxcc list"
    return new_dxcc

def delete_dxcc(user_id):
    pass

def get_dxcc(user_id):
    user_id = "DXCC:" + str(user_id) 
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    data = r.get(user_id).decode('utf-8')
    failstring = "You have entered no dxcc so far!"
    if data:
        return data
    else:
        return failstring

def get_all_chats_ids():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    ids = list()
    for name in r.keys("CALLS:*"):
        ids.append(name.decode("utf-8").replace("CALLS:",""))
    return ids
