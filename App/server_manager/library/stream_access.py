from server_manager.models.stream_access import StreamAccess
from accounts.models import Member
import uuid

"""
    @name: generate_key

    @description: The "generate_key" function is used to create a new key for a user when 
    they request to watch a live stream. The function takes in two parameters, 
    "member_id" and "stream_id", and uses them to create a unique key for the user.
    We than proceed to check the table if any old keys are found, if so, it is 
    removed to prevent multiple connections from one account, the key then is then 
    stored in a table along with the member_id and stream_id.

    @param member_id: The user's id
    @param stream_id: The stream's id

    @return: The key that was generated or None if an error occurred
"""
def generate_key(member_id: uuid, stream_id: uuid) -> StreamAccess or None:

    # -- Check if the key already exists
    #    If so, Invalidate the key
    key = get_key_by_member_id(member_id)
    if key != None:
        invalidate_key_by_id(key.id, True)

    # -- Attempt to locate the user and stream
    member = Member.objects.filter(id=member_id).first()

    # TODO: Change this to the actual stream model
    # stream = Stream.objects.filter(id=stream_id).first()

    # -- Check if the user and stream exists
    if member == None: # or stream == None:
        return None

    # -- Create a new entry in the table
    try:
        return StreamAccess.objects.create(
            member=member,
            stream=str(stream_id)
        )
        
    
    except Exception as e:
        print(e)
        return None
        


#                                         #
# ======== invalidate_key suite ========= #
#                                         #

"""
    @name: invalidate_key_by_id

    @description: Makes a key invalid, causing 'validate_key' to return false
    
    @param key: The key to invalidate
    @param pass_check: If true, the function will not check if the key exists
"""
def invalidate_key_by_id(key_id, pass_check=False) -> bool:

    if pass_check == False:
        if key_exists_by_id(key_id) == False:
            return False

    # -- Remove the key from the table
    StreamAccess.objects.filter(id=key_id).delete()
    return True


"""
    @name: invalidate_key_by_member_id

    @description: Makes a key invalid, causing 'validate_key' to return false

    @param member_id: The user's id
    @param pass_check: If true, the function will not check if the key exists
"""
def invalidate_key_by_member_id(member_id, pass_check=False) -> bool:
    
    if pass_check == False:
        if key_exists_by_member_id(member_id) == False:
            return False

    # -- Get the member
    member = Member.objects.filter(id=member_id).first()

    if member == None:
        return False

    # -- Remove the key from the table
    StreamAccess.objects.filter(member=member).delete()
    return True



"""
    @name: invalidate_key

    @description: Makes a key invalid, causing 'validate_key' to return false
    @param key: The key to invalidate
"""
def invalidate_key(key, pass_check=False) -> bool:
    if pass_check == False:
        if key_exists(key) == False:
            return False

    # -- Remove the key from the table
    StreamAccess.objects.filter(key=key).delete()
    return True



#                                    #
# ======== key_exists suite ======== #
#                                    #

"""
    @name: key_exists_by_id

    @description: Checks if a key exists in the table
    @param key: The key to check
    @return: True if the key exists, False otherwise
"""
def key_exists_by_id(key_id: uuid) -> StreamAccess or None:
    return StreamAccess.objects.filter(id=key_id).first()



"""
    @name: key_exists_by_member_id

    @description: Checks if a key exists in the table
    @param member_id: The user's id
    @return: True if the key exists, False otherwise
"""
def key_exists_by_member_id(member_id: uuid) -> StreamAccess or None:
    return StreamAccess.objects.filter(member=member_id).first()



"""
    @name: key_exists

    @description: Checks if a key exists in the table
    @param key: The key to check
"""
def key_exists(key: str) -> StreamAccess or None:
    return StreamAccess.objects.filter(key=key).first()



#                                    #
# ========= get_keys suite ========= #
#                                    #

"""
    @name: get_keys_by_member

    @description: Returns a list of keys that are associated with a user
    @param member_id: The user's id
    @return: A list of keys or an empty list if an error occurred
"""
def get_key_by_member_id(member_id) -> StreamAccess or None:
    # -- Get the member
    member = Member.objects.filter(id=member_id).first()

    if member == None:
        return None

    return StreamAccess.objects.filter(member=member).first()



"""
    @name: get_keys_by_stream_id

    @description: Returns a list of keys that are associated with a user
    @param stream_id: The stream's id
    @return: A list of keys or an empty list if an error occurred
"""
def get_keys_by_stream_id(stream_id) -> list[StreamAccess]:
    # TODO: We'd actually want to first get the stream, then get the keys
    #      associated with the stream, but for now, we dont have a stream model
    return StreamAccess.objects.filter(stream=stream_id).all()



"""
    @name: get_key

    @description: Returns a list of keys that are associated with a user
    @param key: The key to check
    @return: A StreamAccess object or None if an error occurred or the key does not exist
"""
def get_key(key) -> StreamAccess or None:
    return StreamAccess.objects.filter(key=key).first()



"""
    @name: get_key_by_id

    @description: Returns a list of keys that are associated with a user
    @param key_id: The key id to check
    @return: A StreamAccess object or None if an error occurred or the key does not exist
"""
def get_key_by_id(key_id) -> StreamAccess or None:
    return StreamAccess.objects.filter(id=key_id).first()