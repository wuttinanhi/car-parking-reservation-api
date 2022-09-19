"""
    bcrypt wrapper module
"""


import os

import bcrypt


class BcryptService:
    __salt_round = os.getenv("BCRYPT_SALT") or 10
    __salt = bcrypt.gensalt(rounds=__salt_round)

    @staticmethod
    def hash(value: str):
        return bcrypt.hashpw(value.encode("utf-8"), BcryptService.__salt)

    @staticmethod
    def validate(value: str, hash: str):
        if isinstance(value, str):
            value = value.encode("utf-8")
        if isinstance(hash, str):
            hash = hash.encode("utf-8")
        return bcrypt.checkpw(value, hash)
