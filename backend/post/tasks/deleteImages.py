#from celery import shared_task
import os
from helpers.deleteFiles import delete_files

#@shared_task
def delete_images(path):
  # Get all the related files and pass to the file delete function.
  filename = os.path.basename(path)
  name, extension = os.path.splitext(filename)
  directory = os.path.dirname(path)

  files = [
    path,
    os.path.join(directory, f'{name}_md.webp'),
    os.path.join(directory, f'{name}_lg.webp')
  ]

  delete_files(files)


  