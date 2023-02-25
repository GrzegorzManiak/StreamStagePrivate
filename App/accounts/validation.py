from django.apps import apps 

def check_unique_broadcaster_handle(handle):
    if handle.length == 0:
        return False
    
    # Thank python for not being able to comprehend circular imports
    broadcaster_model = apps.get_model('accounts', 'Broadcaster')

    # Search for a existing broadcaster with this handle. 
    existing = broadcaster_model.objects.filter(broadcaster_handle = handle)
    
    if existing.count() == 0:
        return True

    return False

