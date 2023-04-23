from datetime import datetime
from events.models import EventShowing, Event
from accounts.models import Member


rooms = dict()
last_update = dict()


def get_new_messages(user, showing_id, last_msg):
    chat = get_chat_obj(showing_id)

    new_messages = chat.messages[last_msg:]

    return new_messages

def send_message(user, showing_id, message):
    chat :list = get_chat_obj(showing_id)
    
    last_id = 0 if chat.count() == 0 else chat[chat.count() - 1].id

    chat.append({
        "id": last_id + 1,
        "time": datetime.now(),
        "sender": user.username,
        "message": message
    })


def get_chat_obj(showing_id):
    if not rooms.has_key(showing_id):
        rooms[showing_id] = []

    return rooms[showing_id]
