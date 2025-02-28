from .functions.lessons import resolve_edge as get_dates
import hashlib
import base64


def hash_password(password: str) -> str:
    p1 = hashlib.sha256(password.encode()).digest()
    r = base64.b64encode(p1).decode()
    return r
