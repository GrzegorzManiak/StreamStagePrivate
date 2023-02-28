import random

SLUG_CHARS = list("1234567890")
SLUG_LEN = 9

def new_application_id():
    id = ""

    for _ in range(SLUG_LEN):
        id += SLUG_CHARS[random.randint(0, len(SLUG_CHARS) - 1)]

    return id