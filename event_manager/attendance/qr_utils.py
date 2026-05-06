import hmac
import hashlib
from django.conf import settings


def generate_qr_token(user_id: int) -> str:
    """Generate a signed token for a user: '<user_id>:<hmac>'"""
    key = settings.SECRET_KEY.encode()
    msg = str(user_id).encode()
    signature = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return f"{user_id}:{signature}"


def verify_qr_token(token: str):
    """
    Verify a QR token. Returns user_id (int) on success, None on failure.
    """
    try:
        user_id_str, signature = token.split(":", 1)
        user_id = int(user_id_str)
    except (ValueError, AttributeError):
        return None

    key = settings.SECRET_KEY.encode()
    msg = str(user_id).encode()
    expected = hmac.new(key, msg, hashlib.sha256).hexdigest()

    if hmac.compare_digest(expected, signature):
        return user_id
    return None
