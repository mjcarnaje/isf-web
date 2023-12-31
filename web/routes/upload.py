from cloudinary.uploader import upload
from flask import Blueprint, jsonify, request

from ..config import Config

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

@upload_bp.route('/cloudinary', methods=['POST'])
def cloudinary():
    file = request.files.get('upload')

    if not file:
        return jsonify({
            'is_success': False,
            'error': 'Missing file'
        })
    
    size = len(file.read())
    file.seek(0)

    MAX_FILE_SIZE = 1000 * 1000 * 4 # 4mb

    if size > MAX_FILE_SIZE:
        return jsonify({
            'is_success': False,
            'error': 'File too large'
        }), 413

    
    upload_result = upload(
        file, folder=Config.CLOUDINARY_FOLDER)

    return jsonify({
        'is_success': True,
        'public_id': upload_result['public_id'],
        'url': upload_result['secure_url']
    })