import string, random



EVENT_ID_CHARS = list(string.ascii_uppercase + string.ascii_lowercase + "1234567890")
EVENT_ID_LEN = 8

def generate_event_id():
    event_id = ""

    for _ in range(EVENT_ID_LEN):
        event_id += EVENT_ID_CHARS[random.randint(0, len(EVENT_ID_CHARS)-1)]

    return event_id

    
APP_SLUG_CHARS = list("1234567890")
APP_SLUG_LEN = 9

def new_application_id():
    id = ""

    for _ in range(APP_SLUG_LEN):
        id += APP_SLUG_CHARS[random.randint(0, len(APP_SLUG_CHARS) - 1)]

    return id
    
TICKET_ID_CHARS = list("1234567890abcdef")
TICKET_ID_LEN = 7

def new_ticket_id():
    id = ""

    for _ in range(TICKET_ID_LEN):
        id += TICKET_ID_CHARS[random.randint(0, len(TICKET_ID_CHARS) - 1)]

    return id


PURCHASE_ID_LEN = 20
def new_purchase_id():
    id = ""

    for _ in range(PURCHASE_ID_LEN):
        id += TICKET_ID_CHARS[random.randint(0, len(TICKET_ID_CHARS) - 1)]

    return id