"""
    pagination class wrapper
"""

from enum import Enum

from flask import Request
from marshmallow import Schema, fields, validate
from sqlalchemy import desc
from sqlalchemy.orm.query import Query
from util.validate_request import ValidateRequest
from werkzeug.exceptions import BadRequest


class PaginationSortOptions(Enum):
    ASC = "ASC"
    DESC = "DESC"

    def __str__(self):
        return str(self.value)


def create_order_by(model, key: str, sort: PaginationSortOptions):
    if hasattr(model, key):
        result = model.__dict__.get(key)
        if sort == PaginationSortOptions.DESC:
            result = desc(result)
        return result
    raise BadRequest(f"Invalid order by key!: {key}")


class PaginationOptions(Schema):
    page = fields.Integer(required=True, validate=validate.Range(min=1))
    limit = fields.Integer(required=True, validate=validate.Range(min=1, max=100))
    sort = fields.Integer(required=True, validate=validate.Range(min=0, max=1))
    order_by = fields.String(required=True)


def create_pagination_options_from_request(request: Request):
    data = ValidateRequest(PaginationOptions, request, "GET")

    options = PaginationOptions()
    options.page = int(data.page)
    options.limit = int(data.limit)
    options.order_by = data.order_by

    if int(data.sort) == 1:
        options.sort = PaginationSortOptions.DESC
    else:
        options.sort = PaginationSortOptions.ASC

    return options


def create_pagination_options(
    page=1, limit=10, sort=PaginationSortOptions.ASC, order_by="id"
):
    options = PaginationOptions()
    options.page = page
    options.limit = limit
    options.sort = sort
    options.order_by = order_by
    return options


class Pagination:
    def __init__(self, model, query: Query) -> None:
        self.__model = model
        self.__query = query

    def set_options(self, opt: PaginationOptions):
        self.__page = opt.page - 1
        self.__limit = opt.limit
        self.__offset = self.__page * self.__limit
        self.__order_by = opt.order_by
        if (
            opt.sort == PaginationSortOptions.ASC
            or opt.sort == PaginationSortOptions.DESC
        ):
            self.__sort = opt.sort
        else:
            raise BadRequest(f"Invalid pagination sorting option!: {opt.sort}")

    def result(self):
        return (
            self.__query.order_by(
                create_order_by(self.__model, self.__order_by, self.__sort)
            )
            .offset(self.__offset)
            .limit(self.__limit)
            .all()
        )
