import base64
import graphene
from django.conf import settings
import os

class getImageQuery(graphene.ObjectType):
    image_data = graphene.String()

    def resolve_image_data(self, info):
        user = info.context.user
        if user.is_authenticated:
            # Retrieve the image binary data (replace this with your own logic)
            image = 'user_64/post_59/post_59_lg.webp'
            file_path = os.path.join(settings.MEDIA_ROOT, 'private', image)
            if os.path.exists(file_path):
              extension = os.path.splitext(file_path)[1][1:]
              with open(file_path, 'rb') as file:
                base64_image_data = base64.b64encode(file.read()).decode("utf-8")
                return base64_image_data
        else:
            return None  # or raise an exception, return an error message, etc.