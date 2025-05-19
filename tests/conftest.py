from textwrap import dedent, indent

import markdown
import pytest

from mkdocs_apidescribed.config import DEFAULT_CONFIG
from mkdocs_apidescribed.extension import makeExtension
from mkdocs_apidescribed.formatter import Formatter
from mkdocs_apidescribed.inspector import Symbol, SymbolType


@pytest.fixture
def apid():
    def apid_(
            *,
            before: str = 'before\n',
            after: str = 'after\n',
            target: str = 'mkdocs_apidescribed.probe',
            options: str = ''
    ):
        if options:
            options = indent(dedent(options), '    ')

        text = (
            f'{before}'
            f'::: apidescribed: {target}\n'
            f'{options}'
            f'{after}'
        )

        return markdown.markdown(text, extensions=[makeExtension()])
    return apid_


@pytest.fixture
def get_docstring_parsed(datafix_dir):
    def get_docstring_parsed_(fname: str):
        config = DEFAULT_CONFIG.copy()
        symbol = Symbol(
            depth=0,
            raw='',
            type=SymbolType.func,
            name='func',
            source='def func(): return True',
            docstr=(datafix_dir / fname).read_text(),
            path='pkg.mo.func',
            fpath='/pkg/mo.py',
            params=None,
            returns='returned',
            line_start=12,
            line_end=22,
        )
        return Formatter(symbol=symbol, config=config).docstr
    return get_docstring_parsed_
