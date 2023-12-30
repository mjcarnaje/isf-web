from cloudinary.utils import cloudinary_url
from ..config import Config
from cloudinary.uploader import upload as cloudinary_upload
import io
import base64
from PIL import Image


def get_image(public_id, is_admin=False):
    if "http" in public_id:
        return public_id 

    source = f"{Config.CLOUDINARY_FOLDER}/default"
    if is_admin:
        source = 'isf/logo'
    if public_id:
        source = public_id

    url, options = cloudinary_url(source)
    return url

def reduce_image_quality(base64_image, quality=85):
    # Decode base64 string into bytes
    image_bytes = base64.b64decode(base64_image)

    # Open the image using Pillow
    img = Image.open(io.BytesIO(image_bytes))

    # Convert the image to RGB mode (optional, but can be necessary)
    img = img.convert("RGB")

    # Reduce image quality
    output_buffer = io.BytesIO()
    img.save(output_buffer, format="JPEG", quality=quality)

    # Encode the reduced quality image to base64
    reduced_image_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

    return reduced_image_base64


def upload_images(files) -> [str]:
    results = []

    for file in files:
        file_data = file.split(",")
        data_scheme = file_data[0]
        
        encoded_data = file_data[1]
        new_encoded_data = reduce_image_quality(encoded_data, 60)

        upload_result = cloudinary_upload(f"{data_scheme},{new_encoded_data}", folder=Config.CLOUDINARY_FOLDER)
        
        secure_url = upload_result.get('secure_url', '')
        public_id = upload_result.get('public_id', '')

        results.append(public_id)
    
    return results
