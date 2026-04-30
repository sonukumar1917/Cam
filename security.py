import hashlib
import hmac
from config import BOT_TOKEN

def generate_token(user_id: int) -> str:
    message = str(user_id).encode('utf-8')
    # Using BOT_TOKEN as the secret key for HMAC
    secret = BOT_TOKEN.encode('utf-8')
    signature = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return signature

def validate_token(token: str, user_id: int) -> bool:
    if not token or not user_id:
        return False
    expected = generate_token(user_id)
    return hmac.compare_digest(expected, token)
