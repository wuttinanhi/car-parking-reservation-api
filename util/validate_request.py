"""
    function for validate request json
"""


from collections import namedtuple
from typing import Any, Dict, TypeVar

from flask import Request
from marshmallow import ValidationError

T = TypeVar("T")


def ValidateRequest(schema: T, request: Request, method="POST") -> T:
    # create schema object
    template = schema()

    # parse request
    dict: Dict[Any, Any]
    if method == "GET":
        dict = request.args.to_dict()
    else:
        dict = request.get_json()

    # validate dict
    err = template.validate(dict)
    if err:
        raise ValidationError(err)

    # fill object with data from dict
    return namedtuple(schema.__class__.__name__, dict.keys())(*dict.values())
