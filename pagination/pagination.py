"""
    pagination class wrapper
"""

from enum import Enum
from typing import TypeVar

from database.database import db_session
from flask import Request
from marshmallow import Schema, fields, validate
from sqlalchemy import column, desc, text
from sqlalchemy.orm.query import Query
from util.validate_request import validate_object, validate_request
from werkzeug.exceptions import BadRequest


class PaginationSortOptions(Enum):
    ASC = "ASC"
    DESC = "DESC"

    def __str__(self):
        return str(self.value)


T = TypeVar("T")


class PaginationOptions(Schema):
    page = fields.Integer(required=True, validate=validate.Range(min=1))
    limit = fields.Integer(required=True, validate=validate.Range(min=1, max=100))
    sort = fields.Integer(required=True, validate=validate.Range(min=0, max=1))
    order_by = fields.String(required=True, validate=validate.Length(min=1, max=50))
    search = fields.String(
        required=False, validate=validate.Length(min=0, max=50), default=""
    )

    @classmethod
    def from_dict(cls, d: dict, schem: T) -> T:
        template = cls if cls is None else schem
        vobj = validate_object(template, d)
        return vobj


def int_to_sort(i: int):
    if i == 0:
        return PaginationSortOptions.ASC
    if i == 1:
        return PaginationSortOptions.DESC
    raise BadRequest(f"Invalid pagination sort integer: {i}")


def create_order_by(model, key: str, sort: PaginationSortOptions):
    if hasattr(model, key):
        result = model.__dict__.get(key)
        if sort == PaginationSortOptions.DESC:
            result = desc(result)
        return result
    raise BadRequest(f"Invalid order by key!: {key}")


def create_pagination_options_from_schema(data):
    options = PaginationOptions()
    options.page = int(data.page)
    options.limit = int(data.limit)
    options.order_by = data.order_by

    if hasattr(data, "search"):
        options.search = data.search
    else:
        options.search = ""

    if int(data.sort) == 1:
        options.sort = PaginationSortOptions.DESC
    else:
        options.sort = PaginationSortOptions.ASC

    return options


def create_pagination_options_from_dict(data):
    options = PaginationOptions()
    options.page = int(data["page"])
    options.limit = int(data["limit"])
    options.order_by = data["order_by"]

    if hasattr(data, "search"):
        options.search = data["search"]
    else:
        options.search = ""

    if int(data["sort"]) == 1:
        options.sort = PaginationSortOptions.DESC
    else:
        options.sort = PaginationSortOptions.ASC

    return options


def create_pagination_options_from_request(request: Request):
    data = validate_request(PaginationOptions, request, "GET")
    options = create_pagination_options_from_schema(data)
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
        self._model = model
        self._query = query

    def set_options(self, opt: PaginationOptions):
        self._page = int(opt.page) - 1
        self._limit = int(opt.limit)
        self._offset = self._page * self._limit
        self._order_by = opt.order_by
        self._sort = opt.sort

        if hasattr(opt, "search"):
            self._search = opt.search
        else:
            self._search = ""

        if type(self._sort) == int or type(self._sort) == str:
            to_int = int(self._sort)
            self._sort = int_to_sort(to_int)
        elif isinstance(self._sort, PaginationSortOptions):
            self._sort = self._sort
        else:
            raise BadRequest(f"Invalid pagination sorting option!: {self._sort}")

    def result(self):
        return (
            self._query.order_by(
                create_order_by(self._model, self._order_by, self._sort)
            )
            .offset(self._offset)
            .limit(self._limit)
            .all()
        )


class PaginationRaw(Pagination):
    def __init__(self, raw_query: str) -> None:
        self._query = raw_query

    def result(self):
        statement = self._query
        statement = statement.replace(":sort", str(self._sort))
        statement = statement.replace(":order_by", str(self._order_by))

        params = {
            "limit": int(self._limit),
            "offset": int(self._offset),
            "order_by": column(self._order_by),
            "sort": str(self._sort),
            "search": str(f"%{self._search}%"),
        }

        exec = db_session.execute(text(statement), params)

        result = exec.all()
        return result
