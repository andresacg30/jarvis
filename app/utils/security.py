import jwt

from datetime import datetime, timedelta

from app.utils import config


class TokenError(Exception):
    """
    Raised if JWT can not be decoded or signature is expired.
    """


def encode_jwt_tokens(payload: dict,
                      days_before_expiration: int,
                      secret_key: str,
                      encryption_algorithm: str) -> bytes:
    key = config.bytes_from_str(secret_key)
    expiration_date = _get_expiration_date(days_before_expiration)
    payload["exp"] = expiration_date
    encoded_token = jwt.encode(payload, key=key, algorithm=encryption_algorithm)
    return encoded_token


def decode_jwt_tokens(token: str,
                      secret_key: str,
                      encryption_algorithm: str) -> dict:
    key = config.bytes_from_str(secret_key)
    try:
        decoded = jwt.decode(token, key=key, algorithms=encryption_algorithm)
    except jwt.DecodeError as e:
        raise TokenError("Error decoding signature") from e
    except jwt.ExpiredSignatureError as e:
        raise TokenError("Signature has expired") from e
    return decoded


def _get_expiration_date(days_before_expiration: int) -> datetime:
    if days_before_expiration < 0:
        raise ValueError("Amount of days can not be negative value")
    return datetime.utcnow() + timedelta(days=days_before_expiration)
