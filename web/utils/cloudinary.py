from cloudinary.utils import cloudinary_url

from ..config import Config


def get_image(public_id, is_admin=False):
    if "http" in public_id:
        return public_id 

    source = f"{Config.CLOUDINARY_FOLDER}/default"
    if is_admin:
        source = 'isf/logo'
    if public_id:
        source = public_id

    url, options = cloudinary_url(source, format="jpg", crop="fill")
    return url
