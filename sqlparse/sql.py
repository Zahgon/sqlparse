#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

"""This module contains classes representing syntactical elements of SQL."""

import re

from sqlparse import tokens as T
from sqlparse.utils import imt, remove_quotes


class NameAliasMixin:
    """Implements get_real_name and get_alias."""

    def get_real_name(self):
        """Returns the real name (object name) of this identifier."""
        pass

    def get_alias(self):
        """Returns the alias for this identifier or ``None``."""
        pass


class Token:
    """Base class for all other classes in this module.

    It represents a single token and has two instance attributes:
    ``value`` is the unchanged value of the token and ``ttype`` is
    the type of the token.
    """

    __slots__ = ('value', 'ttype', 'parent', 'normalized', 'is_keyword',
                 'is_group', 'is_whitespace', 'is_newline')

    def __init__(self, ttype, value):
        value = str(value)
        self.value = value
        self.ttype = ttype
        self.parent = None
        self.is_group = False
        self.is_keyword = ttype in T.Keyword
        self.is_whitespace = self.ttype in T.Whitespace
        self.is_newline = self.ttype in T.Newline
        self.normalized = value.upper() if self.is_keyword else value

    def __str__(self):
        return self.value

    # Pending tokenlist __len__ bug fix
    # def __len__(self):
    #     return len(self.value)

    def __repr__(self):
        cls = self._get_repr_name()
        value = self._get_repr_value()

        q = '"' if value.startswith("'") and value.endswith("'") else "'"
        return "<{cls} {q}{value}{q} at 0x{id:2X}>".format(
            id=id(self), **locals())

    def _get_repr_name(self):
        pass

    def _get_repr_value(self):
        pass

    def flatten(self):
        """Resolve subgroups."""
        pass

    def match(self, ttype, values, regex=False):
        """Checks whether the token matches the given arguments.

        *ttype* is a token type as defined in `sqlparse.tokens`. If it does
        not match, ``False`` is returned.
        *values* is a list of possible values for this token. For match to be
        considered valid, the token value needs to be in this list. For tokens
        of type ``Keyword`` the comparison is case-insensitive. For
        convenience, a single value can be given passed as a string.
        If *regex* is ``True``, the given values are treated as regular
        expressions. Partial matches are allowed. Defaults to ``False``.
        """
        type_matched = self.ttype is ttype
        if not type_matched or values is None:
            return type_matched

        if isinstance(values, str):
            values = (values,)

        if regex:
            # TODO: Add test for regex with is_keyword = false
            flag = re.IGNORECASE if self.is_keyword else 0
            values = (re.compile(v, flag) for v in values)

            for pattern in values:
                if pattern.search(self.normalized):
                    return True
            return False

        if self.is_keyword:
            values = (v.upper() for v in values)

        return self.normalized in values

    def within(self, group_cls):
        """Returns ``True`` if this token is within *group_cls*.

        Use this method for example to check if an identifier is within
        a function: ``t.within(sql.Function)``.
        """
        pass

    def is_child_of(self, other):
        """Returns ``True`` if this token is a direct child of *other*."""
        pass

    def has_ancestor(self, other):
        """Returns ``True`` if *other* is in this tokens ancestry."""
        pass


class TokenList(Token):
    """A group of tokens.

    It has an additional instance attribute ``tokens`` which holds a
    list of child-tokens.
    """

    __slots__ = 'tokens'

    def __init__(self, tokens=None):
        self.tokens = tokens or []
        [setattr(token, 'parent', self) for token in self.tokens]
        super().__init__(None, str(self))
        self.is_group = True

    def __str__(self):
        return ''.join(token.value for token in self.flatten())

    # weird bug
    # def __len__(self):
    #     return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)

    def __getitem__(self, item):
        return self.tokens[item]

    def _get_repr_name(self):
        pass

    def _pprint_tree(self, max_depth=None, depth=0, f=None, _pre=''):
        """Pretty-print the object tree."""
        pass

    def get_token_at_offset(self, offset):
        """Returns the token that is on position offset."""
        pass

    def flatten(self):
        """Generator yielding ungrouped tokens.

        This method is recursively called for all child tokens.
        """
        pass

    def get_sublists(self):
        for token in self.tokens:
            if token.is_group:
                yield token

    @property
    def _groupable_tokens(self):
        pass

    def _token_matching(self, funcs, start=0, end=None, reverse=False):
        """next token that match functions"""
        if start is None:
            return None

        if not isinstance(funcs, (list, tuple)):
            funcs = (funcs,)

        if reverse:
            assert end is None
            indexes = range(start - 2, -1, -1)
        else:
            if end is None:
                end = len(self.tokens)
            indexes = range(start, end)
        for idx in indexes:
            token = self.tokens[idx]
            for func in funcs:
                if func(token):
                    return idx, token
        return None, None

    def token_first(self, skip_ws=True, skip_cm=False):
        """Returns the first child token.

        If *skip_ws* is ``True`` (the default), whitespace
        tokens are ignored.

        if *skip_cm* is ``True`` (default: ``False``), comments are
        ignored too.
        """
        pass

    def token_next_by(self, i=None, m=None, t=None, idx=-1, end=None):
        idx += 1
        return self._token_matching(lambda tk: imt(tk, i, m, t), idx, end)

    def token_not_matching(self, funcs, idx):
        pass

    def token_matching(self, funcs, idx):
        pass

    def token_prev(self, idx, skip_ws=True, skip_cm=False):
        """Returns the previous token relative to *idx*.

        If *skip_ws* is ``True`` (the default) whitespace tokens are ignored.
        If *skip_cm* is ``True`` comments are ignored.
        ``None`` is returned if there's no previous token.
        """
        return self.token_next(idx, skip_ws, skip_cm, _reverse=True)

    # TODO: May need to re-add default value to idx
    def token_next(self, idx, skip_ws=True, skip_cm=False, _reverse=False):
        """Returns the next token relative to *idx*.

        If *skip_ws* is ``True`` (the default) whitespace tokens are ignored.
        If *skip_cm* is ``True`` comments are ignored.
        ``None`` is returned if there's no next token.
        """
        if idx is None:
            return None, None
        idx += 1  # alot of code usage current pre-compensates for this

        def matcher(tk):
            pass
        return self._token_matching(matcher, idx, reverse=_reverse)

    def token_index(self, token, start=0):
        """Return list index of token."""
        start = start if isinstance(start, int) else self.token_index(start)
        return start + self.tokens[start:].index(token)

    def group_tokens(self, grp_cls, start, end, include_end=True,
                     extend=False):
        """Replace tokens by an instance of *grp_cls*."""
        pass

    def insert_before(self, where, token):
        """Inserts *token* before *where*."""
        if not isinstance(where, int):
            where = self.token_index(where)
        token.parent = self
        self.tokens.insert(where, token)

    def insert_after(self, where, token, skip_ws=True):
        """Inserts *token* after *where*."""
        if not isinstance(where, int):
            where = self.token_index(where)
        nidx, next_ = self.token_next(where, skip_ws=skip_ws)
        token.parent = self
        if next_ is None:
            self.tokens.append(token)
        else:
            self.tokens.insert(nidx, token)

    def has_alias(self):
        """Returns ``True`` if an alias is present."""
        pass

    def get_alias(self):
        """Returns the alias for this identifier or ``None``."""
        pass

    def get_name(self):
        """Returns the name of this identifier.

        This is either it's alias or it's real name. The returned valued can
        be considered as the name under which the object corresponding to
        this identifier is known within the current statement.
        """
        pass

    def get_real_name(self):
        """Returns the real name (object name) of this identifier."""
        pass

    def get_parent_name(self):
        """Return name of the parent object if any.

        A parent object is identified by the first occurring dot.
        """
        pass

    def _get_first_name(self, idx=None, reverse=False, keywords=False,
                        real_name=False):
        """Returns the name of the first token with a name"""
        pass


class Statement(TokenList):
    """Represents a SQL statement."""

    def get_type(self):
        """Returns the type of a statement.

        The returned value is a string holding an upper-cased reprint of
        the first DML or DDL keyword. If the first token in this group
        isn't a DML or DDL keyword "UNKNOWN" is returned.

        Whitespaces and comments at the beginning of the statement
        are ignored.
        """
        pass


class Identifier(NameAliasMixin, TokenList):
    """Represents an identifier.

    Identifiers may have aliases or typecasts.
    """

    def is_wildcard(self):
        """Return ``True`` if this identifier contains a wildcard."""
        pass

    def get_typecast(self):
        """Returns the typecast or ``None`` of this object as a string."""
        pass

    def get_ordering(self):
        """Returns the ordering or ``None`` as uppercase string."""
        pass

    def get_array_indices(self):
        """Returns an iterator of index token lists"""
        pass


class IdentifierList(TokenList):
    """A list of :class:`~sqlparse.sql.Identifier`\'s."""

    def get_identifiers(self):
        """Returns the identifiers.

        Whitespaces and punctuations are not included in this generator.
        """
        pass


class TypedLiteral(TokenList):
    """A typed literal, such as "date '2001-09-28'" or "interval '2 hours'"."""
    M_OPEN = [(T.Name.Builtin, None), (T.Keyword, "TIMESTAMP")]
    M_CLOSE = T.String.Single, None
    M_EXTEND = T.Keyword, ("DAY", "HOUR", "MINUTE", "MONTH", "SECOND", "YEAR")


class Parenthesis(TokenList):
    """Tokens between parenthesis."""
    M_OPEN = T.Punctuation, '('
    M_CLOSE = T.Punctuation, ')'

    @property
    def _groupable_tokens(self):
        pass


class SquareBrackets(TokenList):
    """Tokens between square brackets"""
    M_OPEN = T.Punctuation, '['
    M_CLOSE = T.Punctuation, ']'

    @property
    def _groupable_tokens(self):
        pass


class Assignment(TokenList):
    """An assignment like 'var := val;'"""


class If(TokenList):
    """An 'if' clause with possible 'else if' or 'else' parts."""
    M_OPEN = T.Keyword, 'IF'
    M_CLOSE = T.Keyword, 'END IF'


class For(TokenList):
    """A 'FOR' loop."""
    M_OPEN = T.Keyword, ('FOR', 'FOREACH')
    M_CLOSE = T.Keyword, 'END LOOP'


class Comparison(TokenList):
    """A comparison used for example in WHERE clauses."""

    @property
    def left(self):
        pass

    @property
    def right(self):
        pass


class Comment(TokenList):
    """A comment."""

    def is_multiline(self):
        pass


class Where(TokenList):
    """A WHERE clause."""
    M_OPEN = T.Keyword, 'WHERE'
    M_CLOSE = T.Keyword, (
        'ORDER BY', 'GROUP BY', 'LIMIT', 'UNION', 'UNION ALL', 'EXCEPT',
        'INTERSECT', 'HAVING', 'RETURNING', 'INTO')


class Over(TokenList):
    """An OVER clause."""
    M_OPEN = T.Keyword, 'OVER'


class Having(TokenList):
    """A HAVING clause."""
    M_OPEN = T.Keyword, 'HAVING'
    M_CLOSE = T.Keyword, ('ORDER BY', 'LIMIT')


class Case(TokenList):
    """A CASE statement with one or more WHEN and possibly an ELSE part."""
    M_OPEN = T.Keyword, 'CASE'
    M_CLOSE = T.Keyword, 'END'

    def get_cases(self, skip_ws=False):
        """Returns a list of 2-tuples (condition, value).

        If an ELSE exists condition is None.
        """
        pass


class Function(NameAliasMixin, TokenList):
    """A function or procedure call."""

    def get_parameters(self):
        """Return a list of parameters."""
        pass

    def get_window(self):
        """Return the window if it exists."""
        pass


class Begin(TokenList):
    """A BEGIN/END block."""
    M_OPEN = T.Keyword, 'BEGIN'
    M_CLOSE = T.Keyword, 'END'


class Operation(TokenList):
    """Grouping of operations"""


class Values(TokenList):
    """Grouping of values"""


class Command(TokenList):
    """Grouping of CLI commands."""
