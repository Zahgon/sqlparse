#
# Copyright (C) 2009-2020 the sqlparse authors and contributors
# <see AUTHORS file>
#
# This module is part of python-sqlparse and is released under
# the BSD License: https://opensource.org/licenses/BSD-3-Clause

from sqlparse import sql, tokens as T
from sqlparse.utils import offset, indent


class AlignedIndentFilter:
    join_words = (r'((LEFT\s+|RIGHT\s+|FULL\s+)?'
                  r'(INNER\s+|OUTER\s+|STRAIGHT\s+)?|'
                  r'(CROSS\s+|NATURAL\s+)?)?JOIN\b')
    by_words = r'(GROUP|ORDER)\s+BY\b'
    split_words = ('FROM',
                   join_words, 'ON', by_words,
                   'WHERE', 'AND', 'OR',
                   'HAVING', 'LIMIT',
                   'UNION', 'VALUES',
                   'SET', 'BETWEEN', 'EXCEPT')

    def __init__(self, char=' ', n='\n'):
        self.n = n
        self.offset = 0
        self.indent = 0
        self.char = char
        self._max_kwd_len = len('select')

    def nl(self, offset=1):
        # offset = 1 represent a single space after SELECT
        pass

    def _process_statement(self, tlist):
        pass

    def _process_parenthesis(self, tlist):
        # if this isn't a subquery, don't re-indent
        pass

    def _process_identifierlist(self, tlist):
        # columns being selected
        pass

    def _process_case(self, tlist):
        pass

    def _next_token(self, tlist, idx=-1):
        pass

    def _split_kwds(self, tlist):
        pass

    def _process_default(self, tlist):
        pass

    def _process(self, tlist):
        func_name = f'_process_{type(tlist).__name__}'
        func = getattr(self, func_name.lower(), self._process_default)
        func(tlist)

    def process(self, stmt):
        self._process(stmt)
        return stmt
