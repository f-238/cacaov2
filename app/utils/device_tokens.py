import hashlib
import hmac
import secrets

from app.config import get_settings


TOKEN_PREFIX = "dvt_"
TOKEN_SIZE_BYTES = 32


def generate_device_token() -> str:
    return f"{TOKEN_PREFIX}{secrets.token_urlsafe(TOKEN_SIZE_BYTES)}"


def hash_device_token(token: str) -> str:
    settings = get_settings()
    return hmac.new(
        settings.secret_key.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
