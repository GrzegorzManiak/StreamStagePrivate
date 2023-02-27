import string, random

EVENT_ID_CHARS = list(string.ascii_uppercase + string.ascii_lowercase + "1234567890")
EVENT_ID_LEN = 8

def generate_event_id():
    event_id = ""

    for i in range(EVENT_ID_LEN):
        event_id += EVENT_ID_CHARS[random.randint(0, len(EVENT_ID_CHARS)-1)]

    return event_id

    
SLUG_CHARS = list("1234567890")
SLUG_LEN = 9

def new_application_id():
    id = ""

    for _ in range(SLUG_LEN):
        id += SLUG_CHARS[random.randint(0, len(SLUG_CHARS) - 1)]

    return id