import re
from textwrap import indent, dedent
from traceback import format_exc
from typing import Any

import griffe
from mkdocs.plugins import get_plugin_logger

from .inspector import Symbol, SymbolType
from .parsers import DocstrParser, Block

log = get_plugin_logger(__name__)

RE_LINK = re.compile(
    r'https?://(www\.)?[A-z0-9@:%.\-_+~#=]{1,256}\.[A-z0-9()]{1,6}\b([A-z0-9()@:%\-_+.~#?&/=]*)'
)

# todo link to src in repo

class Formatter:

    category_titles = {
        SymbolType.attr: 'Attributes',
        SymbolType.func: 'Functions',
        SymbolType.cls: 'Classes',
        SymbolType.module: 'Modules',
    }

    @classmethod
    def format_error(cls, exc: Exception, *, instruction: list[str], debug: bool = False) -> str:

        def indent_raw(val: str) -> str:
            return f'    ```\n{indent(val, prefix="    ")}\n    ```\n'

        lines = [
            f'??? failure "Automated documentation error: {exc.__class__.__name__}"',
            '    **Configuration**',
            indent_raw("\n".join(instruction)),
            f'    **Error**',
            indent_raw(f'{exc}\n\n{format_exc() if debug else ""}'),
        ]

        return '\n'.join(lines)

    @classmethod
    def format_block_admonition(cls, block: Block) -> str:
        return f'!!! {block.marker}\n{cls.reindent(block)}'

    @classmethod
    def format_block_code(cls, block: Block) -> str:
        return f'```{block.value}\n' + dedent('\n'.join(block.addition)) + '\n```'

    @classmethod
    def format_block_version(cls, block: Block) -> str:
        return ''

    @classmethod
    def reindent(cls, src: Any) -> str:
        return indent(dedent(f'{src}'), '    ')

    def __init__(self, *, symbol: Symbol, config: dict):
        self.symbol = symbol
        self.config = config

        categorize = config['categorize']
        self.categorize = categorize

        heading_base = config['heading_base']
        self.heading_base = heading_base
        self.heading_level = heading_base + 1 if categorize else heading_base

        self.docstr = DocstrParser.parse(self.symbol.docstr, config=config, formatter=self)

    def signature_reconstruct_params(self) -> dict[str, tuple[str, str]]:
        docstring = self.docstr

        params = {}

        for param in self.symbol.params:
            param_name = param.name
            param_str = param_name
            param_note = docstring.params.get(param_str, '')

            default = param.default
            annotation = param.annotation

            match param.kind:
                case griffe.ParameterKind.var_positional:
                    param_str = f'*{param_str}'
                    default = False

                case griffe.ParameterKind.var_keyword:
                    param_str = f'**{param_str}'
                    default = False

            if annotation:
                if default:
                    annotation = f'{annotation} '
                param_str = f'{param_str}: {annotation}'

            if default:
                if annotation:
                    default = f' {default}'
                param_str = f'{param_str}={default}'

            params[param_name] = (f'{param_str},', param_note)

        return params

    def signature_build(self, params: dict) -> tuple[str, list[str]]:
        symbol = self.symbol
        reindent = self.reindent

        notes_counter = 0
        param_strings = []
        param_notes = []

        for param_str, param_note in params.values():
            postfix = ''

            if param_note:
                notes_counter += 1
                postfix = f' # ({notes_counter})!'  # add annotation index
                param_notes.append(f'{notes_counter}. {reindent(param_note)}\n')

            param_strings.append(f'{param_str}{postfix}')

        def get_signature() -> str:
            chunks = [
                '.' if symbol.is_class_member else '',
                f'{symbol.name}(',
                f'{joiner}{indented}',
                f'{joiner}{indented}'.join(param_strings).replace(',', ', ').rstrip(', '),
                f'{joiner})',
            ]

            if symbol.type == SymbolType.func and (returns := symbol.returns):
                chunks.extend(f' -> {returns}')

            return ''.join(chunks)

        indented = '    '
        joiner = '\n'

        oneline = not len(param_notes)

        if len(get_signature()) > 80:
            oneline = False

        if oneline:
            indented = ''
            joiner = ''

        return get_signature(), param_notes

    def handle_opt_location(self) -> str:
        symbol = self.symbol
        caption = ''

        if location := self.config['location']:

            match location['mode']:
                case 'module':
                    caption = f'{symbol.path}'.rpartition('.')[0]

                case 'file':
                    caption = f'{symbol.fpath}'

            if caption and location['line']:
                caption = f'{caption}:{symbol.line_start}'

        return caption

    def format_category(self) -> str:

        if self.categorize and (category := self.category_titles.get(self.symbol.type)):
            return f'{"#" * self.heading_base} {category}\n'

        return ''

    def format_signature(self) -> str:
        symbol = self.symbol
        param_notes = []

        def get_signature():
            return self.signature_build(self.signature_reconstruct_params())

        match symbol.type:
            case SymbolType.func | SymbolType.cls:
                signature, param_notes = get_signature()

            case SymbolType.attr:
                if symbol.is_property:
                    signature, param_notes = get_signature()

                else:
                    signature = (
                        ('.' if symbol.is_class_member else '') +
                        symbol.source
                    )

            case _:
                signature = ''

        if not signature:
            return ''

        caption = self.handle_opt_location()
        if caption:
            caption = f'title="{caption}"'

        lines = [
            f'\n``` py {caption}\n{signature}\n```\n',
            # param descriptions block
            *param_notes,
        ]

        return '\n'.join(lines)

    def format_description(self) -> str:
        docstring = self.docstr
        symbol = self.symbol
        icons = self.config['icons']

        text = docstring.text

        prefix = ''
        if symbol.type == SymbolType.cls:
            if bases := [f'[``{base.name}``](#{base.name.lower()})' for base in symbol.raw.bases]:
                prefix = f'{icons["clsbases"]} {" ".join(bases)}\n\n'

        text = f'{prefix}{text}\n'

        if raised := docstring.raises:
            raises = '\n\n'.join(
                f'{icons["raises"]} `{raised_key}` {raised_val}'
                for raised_key, raised_val in raised.items()
            )
            text = f'{text}\n{raises}\n'

        if returns := docstring.returns:
            returns = '\n\n'.join(
                f'{icons["returns"]} {returned}'
                for returned in returns
            )
            text = f'{text}\n{returns}\n'

        return text

    def format_title(self) -> str:
        symbol = self.symbol
        icons = self.config['icons']

        icon_before = icons.get(symbol.type.name, '')
        icons_after = []

        if symbol.is_inherited:
            icons_after.append(icons['inherited'])

        if symbol.is_property:
            icons_after.append(icons['property'])

        if symbol.is_classmethod:
            icons_after.append(icons['classmethod'])

        if symbol.is_staticmethod:
            icons_after.append(icons['staticmethod'])

        heading_marker = f'{"#" * (self.heading_level + symbol.depth)} '[:7]  # 7th level max
        title = f'{heading_marker}{icon_before} {symbol.name} {" ".join(icons_after)}\n'

        return title

    def indent(self, *, title: str, body: str) -> str:

        left = '<div style="margin-left:1.8em" markdown>'
        right = '</div>'

        depth = self.symbol.depth

        indented = (
            (left * depth) +
            title + (left + body + right) +
            (right * depth)
        )

        return indented

    def run(self) -> str:

        signature = self.format_signature()

        out = [
            signature,
            self.format_description(),
        ]

        out = '\n'.join(out)

        if signature:
            out = self.indent(title=self.format_title(), body=out)

        if out.strip():
            out = f'{out}\n----'

        if self.config['autolinks']:
            out = RE_LINK.sub(r'<\g<0>>', out)

        return out
