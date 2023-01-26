from models import StreamAccess
from accounts.models import Member
import secrets


"""
    @name: generate_key

    @description: The "generate_key" function is used to create a new key for a user when 
    they request to watch a live stream. The function takes in two parameters, 
    "user_id" and "stream_id", and uses them to create a unique key for the user.
    We than proceed to check the table if any old keys are found, if so, it is 
    removed to prevent multiple connections from one account, the key then is then 
    stored in a table along with the user_id and stream_id.

    @param user_id: The user's id
    @param stream_id: The stream's id

    @return: The key that was generated or None if an error occurred
"""
def generate_key(user_id, stream_id):

    # -- Check if the key already exists
    #    If so, Invalidate the key
    for key in get_keys_by_user(user_id):
        invalidate_key(key, True)

    # -- Attempt to locate the user and stream
    user = Member.objects.filter(id=user_id).first()

    # TODO: Change this to the actual stream model
    # stream = Stream.objects.filter(id=stream_id).first()

    # -- Check if the user and stream exists
    if user == None: # or stream == None:
        return None

    # -- Create a new entry in the table
    StreamAccess.objects.create(
        user=user,
        stream=""
    )
        


"""
    @name: invalidate_key

    @description: Makes a key invalid, causing 'validate_key' to return false
    
    @param key: The key to invalidate
    @param pass_check: If true, the function will not check if the key exists
"""
def invalidate_key(key, pass_check=False):

    match key_exists(key) or pass_check:
        case True:
            # -- Remove the key from the table
            StreamAccess.objects.filter(id=key).delete()
            return True

        case False: return False


    
"""
    @name: key_exists

    @description: Checks if a key exists in the table
    @param key: The key to check
    @return: True if the key exists, False otherwise
"""
def key_exists(key):
    return StreamAccess.objects.filter(id=key).exists()



"""
    @name: get_keys_by_user

    @description: Returns a list of keys that are associated with a user
    @param user_id: The user's id
    @return: A list of keys or an empty list if an error occurred
"""
def get_keys_by_user(user_id):
    user = Member.objects.filter(id=user_id).first()

    if user == None:
        return []

    return StreamAccess.objects.filter(user=user).all()