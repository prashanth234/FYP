import os
import logging
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

def remove_exisiting_files_in_dir(filename):
    """
    Removes all files in the directory in which given file contains.
    """

    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    directory_path = os.path.dirname(file_path)
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    deleted_path = os.path.join(directory_path, f'deleted_{current_datetime}')

    try:
        os.makedirs(deleted_path)
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.rename(file_path, os.path.join(deleted_path, filename))
                logger.info(f"File '{file_path}' successfully removed.")
    except OSError as e:
        logger.error(f"Error: {e.strerror}")