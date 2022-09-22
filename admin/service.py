"""
    admin service
"""

import os


class AdminService:
    @staticmethod
    def is_valid_admin_key(key: str):
        return key == os.getenv("ADMIN_KEY")
