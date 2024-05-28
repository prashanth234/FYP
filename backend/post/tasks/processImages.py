#from celery import shared_task
from io import BytesIO
from django.core.files.storage import default_storage
import os
from django.conf import settings

#@shared_task
def process_image(img, path, webp_quality=95, jpeg_quality=95):
    target_sizes = {
        'md': 800,
        'lg': 1000
    }

    directory = os.path.dirname(path)
    filename = os.path.basename(path)

    # Calculate new dimensions while maintaining the aspect ratio
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height
    is_storage_s3 = True if os.environ.get('AWS_S3_ENDPOINT_URL') else False

    for size_label, size in target_sizes.items():

        if original_width < size:

            resized_img = img

        else:

            # Calculate new width and height based on the target size and aspect ratio
            new_width = size
            new_height = int(size / aspect_ratio)

            # Resize the image
            resized_img = img.resize((new_width, new_height))


         # New filename
        new_filename = filename.replace(".jpeg", f"_{size_label}.webp")

        # Path
        path = f"{directory}/{new_filename}"

        if is_storage_s3:
            upload_to_s3(resized_img, webp_quality, path)
        else:
            upload_to_disk(resized_img, webp_quality, path)


def upload_to_s3(resized_img, webp_quality, path):

    # Convert image to bytes
    image_bytes = BytesIO()
    resized_img.save(image_bytes, format="WEBP", quality=webp_quality)
    image_bytes.seek(0)

    # Save as WebP format with specified quality
    default_storage.save(path, image_bytes)

def upload_to_disk(resized_img, webp_quality, path):

    # Save as WebP format with specified quality
    resized_img.save(os.path.join(settings.MEDIA_ROOT, path), "WEBP", quality=webp_quality)

    # Save as JPEG format with specified quality after converting to RGB
    # resized_img.convert("RGB").save(output_path_jpeg, "JPEG", quality=jpeg_quality)