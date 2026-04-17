#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

from sqlparse import sql
from sqlparse import tokens as T
from sqlparse.exceptions import SQLParseError
from sqlparse.utils import recurse, imt

# Maximum recursion depth for grouping operations to prevent DoS attacks
# Set to None to disable limit (not recommended for untrusted input)
MAX_GROUPING_DEPTH = 100

# Maximum number of tokens to process in one grouping operation to prevent
# DoS attacks.
# Set to None to disable limit (not recommended for untrusted input)
MAX_GROUPING_TOKENS = 10000

T_NUMERICAL = (T.Number, T.Number.Integer, T.Number.Float)
T_STRING = (T.String, T.String.Single, T.String.Symbol)
T_NAME = (T.Name, T.Name.Placeholder)


def _group_matching(tlist, cls, depth=0):
    """Groups Tokens that have beginning and end."""
    pass


def group_brackets(tlist):
    pass


def group_parenthesis(tlist):
    pass


def group_case(tlist):
    pass


def group_if(tlist):
    pass


def group_for(tlist):
    pass


def group_begin(tlist):
    pass


def group_typecasts(tlist):
    pass


def group_tzcasts(tlist):
    pass


def group_typed_literal(tlist):
    # definitely not complete, see e.g.:
    # https://docs.microsoft.com/en-us/sql/odbc/reference/appendixes/interval-literal-syntax
    # https://docs.microsoft.com/en-us/sql/odbc/reference/appendixes/interval-literals
    # https://www.postgresql.org/docs/9.1/datatype-datetime.html
    # https://www.postgresql.org/docs/9.1/functions-datetime.html
    pass


def group_period(tlist):
    pass


def group_as(tlist):
    pass


def group_assignment(tlist):
    pass


def group_comparison(tlist):
    pass


@recurse(sql.Identifier)
def group_identifier(tlist):
    pass


@recurse(sql.Over)
def group_over(tlist):
    pass


def group_arrays(tlist):
    pass


def group_operator(tlist):
    pass


def group_identifier_list(tlist):
    pass


@recurse(sql.Comment)
def group_comments(tlist):
    pass


@recurse(sql.Where)
def group_where(tlist):
    pass


@recurse()
def group_aliased(tlist):
    pass


@recurse(sql.Function)
def group_functions(tlist):
    pass


@recurse(sql.Identifier)
def group_order(tlist):
    """Group together Identifier and Asc/Desc token"""
    pass


@recurse()
def align_comments(tlist):
    pass


def group_values(tlist):
    pass


def group(stmt):
    for func in [
        group_comments,

        # _group_matching
        group_brackets,
        group_parenthesis,
        group_case,
        group_if,
        group_for,
        group_begin,

        group_over,
        group_functions,
        group_where,
        group_period,
        group_arrays,
        group_identifier,
        group_order,
        group_typecasts,
        group_tzcasts,
        group_typed_literal,
        group_operator,
        group_comparison,
        group_as,
        group_aliased,
        group_assignment,

        align_comments,
        group_identifier_list,
        group_values,
    ]:
        func(stmt)
    return stmt


def _group(tlist, cls, match,
           valid_prev=lambda t: True,
           valid_next=lambda t: True,
           post=None,
           extend=True,
           recurse=True,
           depth=0
           ):
    """Groups together tokens that are joined by a middle token. i.e. x < y"""
    pass
