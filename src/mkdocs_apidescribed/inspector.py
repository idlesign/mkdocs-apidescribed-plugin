from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from fnmatch import fnmatch
from typing import Any

import griffe
from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)


class SymbolType(Enum):
    attr = 1
    func = 2
    cls = 3
    module = 4


@dataclass
class Symbol:

    depth: int
    raw: Any
    type: SymbolType
    name: str
    source: str
    docstr: griffe.Docstring
    path: str
    fpath: str
    params: griffe.Parameters | None
    returns: str
    line_start: int = None
    line_end: int = None

    @property
    def is_property(self) -> bool:
        return 'property' in self.raw.labels

    @property
    def is_inherited(self) -> bool:
        return self.raw.inherited

    @property
    def is_class_member(self) -> bool:
        return self.raw.parent.is_class

    @property
    def is_classmethod(self) -> bool:
        return 'classmethod' in self.raw.labels

    @property
    def is_staticmethod(self) -> bool:
        return 'staticmethod' in self.raw.labels


def simplify_args(symb: griffe.Object, parameters: griffe.Parameters):
    # drop self, cls
    if symb.is_class or symb.parent.is_class:
        if parameters._params:
            parameters = deepcopy(parameters)
            # Exceptions can have no params
            parameters._params.pop(0)
    return parameters


def get_symbol(
    obj: griffe.Object,
    *,
    types: list[str] = None,
    undocumented: bool = False,
    ignore: list[str] = None,
    only: set[str] = None,
    inherited: bool = True,
    depth: int = 0,
) -> tuple[Symbol, list[Symbol]] | None:

    symbol_type = 0
    symbols_sub = []
    types = types or []

    params = getattr(obj, 'parameters', [])
    returns = getattr(obj, 'returns', None)

    if obj.is_attribute:
        symbol_type = SymbolType.attr

    elif obj.is_module:
        symbol_type = SymbolType.module

    elif obj.is_function:
        symbol_type = SymbolType.func
        params = simplify_args(obj, params)

    elif obj.is_class:
        symbol_type = SymbolType.cls
        params = simplify_args(obj, params)

        symbols_sub = get_symbols(
            obj,
            types=types,
            undocumented=undocumented,
            ignore=ignore,
            only=only,
            inherited=inherited,
            depth=depth + 1
        )

    if not symbol_type:
        log.error(f'Unsupported symbol type: {obj}. Skipped.')
        return

    symbol = Symbol(
        depth=depth,
        raw=obj,
        type=symbol_type,
        name=obj.name,
        source=obj.source,
        docstr=obj.docstring,
        path=obj.path,
        fpath=f'{obj.relative_package_filepath}',
        params=params,
        returns=returns,
        line_start=obj.lineno,
        line_end=obj.endlineno,
    )
    return symbol, symbols_sub


def get_symbols(
    container: griffe.Object,
    *,
    types: list[str],
    undocumented: bool = False,
    ignore: list[str] = None,
    only: set[str] = None,
    inherited: bool = True,
    depth: int = 0,
) -> list[Symbol]:

    symbols = []
    ignore = ignore or []
    only = only or set()

    for key in types:

        for _, symbol_raw in sorted(getattr(container, key).items(), key=lambda item: item[0]):

            if not depth and symbol_raw.is_alias:
                # hide imported from other modules
                # but preserve class members inherited from base
                continue

            name = symbol_raw.name

            docstring = symbol_raw.docstring
            skip = False

            if not inherited and symbol_raw.inherited:
                continue

            if docstring is None and not undocumented:
                continue

            if only:
                skip = name not in only

            else:
                for rule in ignore:
                    if fnmatch(name, rule):
                        skip = True
                        break

            if skip:
                continue

            symbol, symbols_sub = get_symbol(
                symbol_raw,
                types=types,
                undocumented=undocumented,
                ignore=ignore,
                only=only,
                inherited=inherited,
                depth=depth,
            )

            if symbol:
                symbols.append(symbol)

            if symbols_sub:
                symbols.extend(symbols_sub)
                # symbols_sub.clear()

    return symbols


def inspect(
        target: str,
        *,
        types: list[str],
        undocumented: bool = False,
        ignore: list[str],
        only: list[str],
        inherited: bool,
) -> tuple[Symbol, list[Symbol]]:

    log.info(f'Getting API information for: {target} ...')
    obj = griffe.load(target)

    root, _ = get_symbol(obj)
    symbols = get_symbols(
        obj,
        types=types,
        undocumented=undocumented,
        ignore=ignore,
        only=set(only),
        inherited=inherited,
    )

    return root, symbols
