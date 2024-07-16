import os
from PIL import Image
from django.core.management.base import BaseCommand
from post.models.Post import PostFile

class Command(BaseCommand):
    help = 'Updates width and height of images in PostFile model'

    def handle(self, *args, **kwargs):
        # Fetch all PostFile objects
        post_files = PostFile.objects.all()

        # Iterate through each object
        for post_file in post_files:
            image_path = post_file.file.path
            try:
                with Image.open(image_path) as img:
                    width, height = img.size

                    # Update width and height
                    post_file.width = width
                    post_file.height = height
                    post_file.save()

                    self.stdout.write(self.style.SUCCESS(
                        f"Updated dimensions for {os.path.basename(image_path)}: width={width}, height={height}"
                    ))
            except FileNotFoundError:
                self.stdout.write(self.style.ERROR(f"File not found at path: {image_path}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))