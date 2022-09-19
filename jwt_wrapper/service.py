"""
    jwt wrapper module
"""


import os
from datetime import datetime, timedelta, timezone

import jwt


class JwtService:
    __jwt_secret = os.getenv("BCRYPT_SALT") or "dev-secret"

    def encode(value: any, duration: int):
        value["iat"] = datetime.now(tz=timezone.utc)
        value["exp"] = value["iat"] + timedelta(seconds=duration)
        return jwt.encode(value, JwtService.__jwt_secret, "HS256")

    def validate(value: str):
        try:
            jwt.decode(value, JwtService.__jwt_secret, algorithms=["HS256"])
            return True
        except:
            return False

    def decode(value: str):
        return jwt.decode(value, JwtService.__jwt_secret, algorithms=["HS256"])
