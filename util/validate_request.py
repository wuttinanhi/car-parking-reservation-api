"""
    function for validate request json
"""

from collections import namedtuple
from typing import TypeVar

from flask import Request
from marshmallow import ValidationError

T = TypeVar('T')


def ValidateRequest(schema: T, request: Request) -> T:
    template = schema()
    dict = request.get_json()
    err = template.validate(dict)
    if err:
        raise ValidationError(err)
    return namedtuple(schema.__class__.__name__, dict.keys())(*dict.values())
