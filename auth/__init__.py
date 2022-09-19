"""
    auth module
"""

from auth.blueprint import blueprint as auth_blueprint
from auth.decorator import login_required
from auth.function import GetUser

__all__ = [auth_blueprint, login_required, GetUser]
