"""
    function for validate request json
"""


from collections import namedtuple
from typing import Any, Dict, TypeVar

from flask import Request
from marshmallow import Schema, ValidationError

T = TypeVar("T")


def validate_object(schema: T, dict: Any) -> T:
    template: Schema = schema()
    err = template.validate(dict)
    if err:
        raise ValidationError(err)
    result = namedtuple(template.__class__.__name__, dict.keys())(*dict.values())
    return result


def validate_request(schema: T, request: Request, method="POST") -> T:
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
