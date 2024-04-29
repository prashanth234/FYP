#from celery import shared_task
from PIL import Image
import os

#@shared_task
def process_image(input_path, webp_quality=95, jpeg_quality=95):
    target_sizes = {
        'md': 800,
        'lg': 1000
    }

    # Open the image
    img = Image.open(input_path)

    # Calculate new dimensions while maintaining the aspect ratio
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    for size_label, size in target_sizes.items():

        if original_width < size:

            resized_img = img

        else:

            # Calculate new width and height based on the target size and aspect ratio
            new_width = size
            new_height = int(size / aspect_ratio)

            # Resize the image
            resized_img = img.resize((new_width, new_height))

        # Get the parent directory of the input file
        output_folder = os.path.dirname(input_path)

        # Create a subdirectory for resized images
        # output_folder = os.path.join(input_directory, "resized_images")
        # os.makedirs(output_folder, exist_ok=True)

        # Get the file name (without extension) from the input path
        file_name = os.path.splitext(os.path.basename(input_path))[0]

        # Generate output paths based on the input path and output folder
        output_path_webp = os.path.join(output_folder, f"{file_name}_{size_label}.webp")
        # output_path_jpeg = os.path.join(output_folder, f"{file_name}_resized.jpg")

        # Save as WebP format with specified quality
        resized_img.save(output_path_webp, "WEBP", quality=webp_quality)

        # Save as JPEG format with specified quality after converting to RGB
        # resized_img.convert("RGB").save(output_path_jpeg, "JPEG", quality=jpeg_quality)