import base64


def bytes_from_str(key: str) -> bytes:
    """Get bytes from a string value.

    Assumes URLsafe-base64 encoding.
    """
    return base64.urlsafe_b64decode(key)
