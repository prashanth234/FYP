import os
from django.conf import settings

def custom_upload(path, newfilename, filename):
    """
    Custom upload_to function to generate image file names.
    """
    # Get the original file extension
    file_extension = os.path.splitext(filename)[1] or '.jpeg'

    # Remove image before creating if image already exists
    # file_path = os.path.join(settings.MEDIA_ROOT, f'{path}/{newfilename}{file_extension}')
    # if os.path.exists(file_path):
    #     os.remove(file_path)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

    # Return the custom file path
    return os.path.join(f'{path}/', newfilename + file_extension)