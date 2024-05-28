import os
from django.conf import settings
from django.core.files.storage import default_storage
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def delete_files(files):
  # Accepts list of file path to be removed.
  logger.info(f'Removing {files} from storage s3/disk.')

  for file_path in files:
    if default_storage.exists(file_path):
        default_storage.delete(file_path)
        logger.info(f"File '{file_path}' has been successfully deleted.")
    else:
        logger.info(f"File '{file_path}' does not exist")  
 
  
def soft_delete(filename):
    """
    This function needs to be made changes to support s3 and disk
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
