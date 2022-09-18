"""
    bcrypt wrapper module
"""


import os

import bcrypt


class BcryptWrapper:
    __salt_round = os.getenv("BCRYPT_SALT") or 10
    __salt = bcrypt.gensalt(rounds=__salt_round)

    @staticmethod
    def hash(value: str):
        return bcrypt.hashpw(value.encode("utf-8"), BcryptWrapper.__salt)

    @staticmethod
    def validate(value: str, hash: str):
        return bcrypt.checkpw(value.encode("utf-8"), hash)
