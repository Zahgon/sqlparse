#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

from sqlparse import sql, tokens as T
from sqlparse.utils import offset, indent


class ReindentFilter:
    def __init__(self, width=2, char=' ', wrap_after=0, n='\n',
                 comma_first=False, indent_after_first=False,
                 indent_columns=False, compact=False):
        self.n = n
        self.width = width
        self.char = char
        self.indent = 1 if indent_after_first else 0
        self.offset = 0
        self.wrap_after = wrap_after
        self.comma_first = comma_first
        self.indent_columns = indent_columns
        self.compact = compact
        self._curr_stmt = None
        self._last_stmt = None
        self._last_func = None

    def _flatten_up_to_token(self, token):
        """Yields all tokens up to token but excluding current."""
        pass

    @property
    def leading_ws(self):
        pass

    def _get_offset(self, token):
        pass

    def nl(self, offset=0):
        pass

    def _next_token(self, tlist, idx=-1):
        pass

    def _split_kwds(self, tlist):
        pass

    def _split_statements(self, tlist):
        pass

    def _process(self, tlist):
        func_name = f'_process_{type(tlist).__name__}'
        func = getattr(self, func_name.lower(), self._process_default)
        func(tlist)

    def _process_where(self, tlist):
        pass

    def _process_parenthesis(self, tlist):
        pass

    def _process_function(self, tlist):
        pass

    def _process_identifierlist(self, tlist):
        pass

    def _process_case(self, tlist):
        pass

    def _process_values(self, tlist):
        pass

    def _process_default(self, tlist, stmts=True):
        pass

    def process(self, stmt):
        self._curr_stmt = stmt
        self._process(stmt)

        if self._last_stmt is not None:
            nl = '\n' if str(self._last_stmt).endswith('\n') else '\n\n'
            stmt.tokens.insert(0, sql.Token(T.Whitespace, nl))

        self._last_stmt = stmt
        return stmt
