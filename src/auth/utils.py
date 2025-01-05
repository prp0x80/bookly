import jwt.exceptions
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from src.config import settings
import uuid
import logging

ACCESS_TOKEN_EXPIRY = 3600

passwd_context = CryptContext(schemes=["bcrypt"])


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now(
    ) + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(payload=payload, key=settings.JWT_SECRET,
                       algorithm=settings.JWT_ALGORITHM)
    return token


def decode_token(token: str) -> str | None:
    try:
        token_data = jwt.decode(jwt=token,
                                key=settings.JWT_SECRET,
                                algorithms=[settings.JWT_ALGORITHM])
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
