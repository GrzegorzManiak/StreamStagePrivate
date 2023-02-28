from django.apps import apps 

valid_chars = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_")

def check_unique_broadcaster_handle(handle):
    if len(handle) == 0:
        return False
    
    # Thank python for not being able to comprehend "circular" imports
    broadcaster_model = apps.get_model('accounts', 'Broadcaster')

    # Search for a existing broadcaster with this handle. 
    existing = broadcaster_model.objects.filter(handle=handle)

    if existing.first() is None:
        return False
    
    for char in list(handle):
        if char not in valid_chars:
            return False
        
    return True

