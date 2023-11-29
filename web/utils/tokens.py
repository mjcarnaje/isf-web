from flask import current_app
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from ..config import Config


def generate_verification_token(user_id: int, email: str):
    current_app.logger.info("Generating token for verification..")
    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
    return serializer.dumps(
        {'user_id': user_id, 'email': email},
        salt='verify-account'
    )

def check_verification_token(token: str):
    try:
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        data = serializer.loads(token, salt='verify-account', max_age=3600)
        return {
            'is_valid': data.get('email') is not None,
            'is_expired': False
        }
    except SignatureExpired:
        return {
            'is_valid': False,
            'is_expired': True
        }
    

