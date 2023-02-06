from django.core.exceptions import ValidationError
import os
import uuid

supported_content = [ 'image/bmp', 'image/png', 'image/pjpeg','image/jpeg', 'video/webm', 'video/mp4', 'video/h264', 'video/quicktime' ]

def validate_event_media(obj):
    if obj.file.content_type not in supported_content:
        raise ValidationError(f'Content of type {obj.file.content_type} is not supported.')

def generate_file_media(instance, filename):
    path = "media/"
    
    #format = filename + str(uuid.uuid4)[:12] + instance.file_extension

    ext = filename.split(".")[-1]

    if ext is not filename: # if file has an extension
        filename = filename[:len(filename) - len(ext) - 1]

    format = (str(uuid.uuid4())[:9] + filename)[:24] + "." + ext

    return os.path.join(path, format)