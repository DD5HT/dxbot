import redis

def create_user(user_id):
    """Creates a new user account in the database"""
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    user_id_calls = "CALLS:" + str(user_id)
    user_id_dxcc = "DXCC:" + str(user_id)
    #r.set(user_id_calls, "")
    #r.set(user_id_dxcc, "")

    success = "Your account was created successfully, good DX!"
    return success

def add_call(user_id, call):
    """Adds new call in capitals to the database"""
    call_user_id = "CALLS:" + str(user_id)
    call = call.upper() + " "

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    for entry in call.split(" "):
        if sanitize_call(entry):
            print(entry)
            if r.exists(entry):
                r.append(entry, " " + str(user_id) )
            else:
                r.set(entry, str(user_id)) 
            r.append(call_user_id, call)
            return "Added: " + call +"to callsign list"
        else:
            return "INVALID CALL FORMAT"


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
    try:
        data = r.get(user_id).decode('utf-8') 
        data = data.split()
        data.sort()
        data = "  ".join(data)
        return data

    except AttributeError:
        return "You have entered no calls so far!"
 
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

def sanitize_call(call):
    #TODO look if call contains atleast 1 number
    if len(call) >= 15 or len(call) <= 2:
        return False
    elif ":" in call:
        return False
    elif "CALL" in call:
        return False
    elif "DXCC" in call:
        return False
    elif " " in call:
        return False
    else:
        return True


