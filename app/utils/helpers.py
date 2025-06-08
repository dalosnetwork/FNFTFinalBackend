import pyotp
import jwt
from datetime import datetime, timedelta
from app.config import settings

def verify_2fa_code(secret_key: str, code: str) -> bool:
    totp = pyotp.TOTP(secret_key)
    return totp.verify(code)

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=3)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")
