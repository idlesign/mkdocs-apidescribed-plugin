import re
from collections import defaultdict
from dataclasses import dataclass, field
from textwrap import dedent
from typing import TYPE_CHECKING

import griffe

if TYPE_CHECKING:
    from .formatter import Formatter


@dataclass
class Docstring:

    text: str = ''
    params: dict[str, str] = field(default_factory=dict)
    returns: list[str] = field(default_factory=list)
    raises: dict[str, str] =  field(default_factory=dict)


class Block:

    unmarked: str = '_unmarked'

    def __init__(self, marker: str = '', arg: str = '', value: str = ''):
        self.marker = marker or self.unmarked
        self.arg = arg.strip()
        self.value = value
        self.addition = []

    def __str__(self):
        prefix = f'{value}\n' if (value := self.value) else ''
        return prefix + '\n'.join(self.addition)

    @property
    def is_marked(self) -> bool:
        return self.marker != self.unmarked

    def contribute(self, val: str):
        self.addition.append(val)


class DocstrParser:
    alias: str = ''

    registry: dict[str, type['DocstrParser']] = {}

    @classmethod
    def parse(cls, docstr: griffe.Docstring | None, *, config: dict, formatter: 'Formatter') -> Docstring:

        value = getattr(docstr, 'value', None) or ''
        docstring = Docstring(text=f'{value}')

        if value:
            preferred_parser = config['format']

            parser = DocstrParser.registry.get(preferred_parser)
            parsers = [parser] if parser else DocstrParser.registry.values()

            for parser_cls in parsers:
                parser = parser_cls(value, config=config, formatter=formatter)

                if (result := parser.run()) and parser.markers_detected:
                    docstring = result
                    break

        return docstring

    def __init_subclass__(cls):
        alias = cls.alias
        registry = cls.registry

        assert alias
        assert alias not in registry

        super().__init_subclass__()

        registry[alias] = cls

    def __init__(self, src: str, *, config: dict, formatter: 'Formatter'):
        self.src = src
        self.config = config
        self.markers_detected = False
        self.formatter = formatter

    def run(self) -> Docstring | None:
        return self._parse(self.src)

    def postprocess(self, text: str) -> str:
        return text

    def _parse(self, value: str) -> Docstring | None:  # pragma: nocover
        return

    def to_dict(self, blocks: list[Block]) -> dict[str, str]:
        result = {
            block.arg: self.postprocess(f'{block}')
            for block in blocks
        }
        return result

    def to_list(self, blocks: list[Block]) -> list[str]:
        return [self.postprocess(f'{block}'.strip()) for block in blocks]


class SphinxParser(DocstrParser):
    alias: str = 'sphinx'

    re_markers = re.compile(
        r':(?P<marker>param|type|raises|return|rtype)'
        r'(?P<arg>[^:]*):\s*(?P<value>.*)'
    )

    re_directives = re.compile(
        r'\.\. (?P<marker>note|warning|code-block|versionadded|versionchanged|deprecated)'
        r'(?P<arg>[^:]*)::\s*(?P<value>.*)'
    )

    def postprocess(self, text: str) -> str:
        text = super().postprocess(text)
        formatter = self.formatter

        if (split := text.splitlines()) and len(split) > 1:
            # nested indented block (e.g. in param descriptions)
            # reindent with prefix from 2nd line
            line_two = split[1]
            prefix = ' ' * (len(line_two) - len(line_two.lstrip(' ')))
            text = dedent('\n'.join([
                f'{prefix}{split[0].lstrip()}',
                *split[1:]
            ]))

        _, processed = self.parse_blocks(
            pattern=self.re_directives,
            value=text,
        )

        lines = []

        for block in processed:
            if block.is_marked:
                match block.marker:
                    case 'versionadded' | 'versionchanged' | 'deprecated':
                        block = formatter.format_block_version(block)

                    case 'note' | 'warning':
                        block = formatter.format_block_admonition(block)

                    case 'code-block':
                        block = formatter.format_block_code(block)

            lines.append(f'{block}')

        return '\n'.join(lines)

    def parse_blocks(
            self,
            *,
            pattern: re.Pattern,
            value: str,
    ) -> tuple[dict[str, list[Block]], list[Block]]:

        blocks: dict[str, list[Block]] = defaultdict(list)
        block_last: Block | None = None
        marker_detected = False

        processed = []

        for line in value.splitlines():

            is_empty = len(line.strip()) == 0

            if block_last:
                if line.startswith(' ') or is_empty:
                    # must be a continuation of a block
                    block_last.contribute(line)
                    continue

                # previous block ended
                processed.append(block_last)
                block_last = None

            if matched := pattern.match(line):
                marker_detected = True
                marker = matched.group('marker')

                arg = matched.group('arg')
                val = matched.group('value')

                block = Block(marker, arg, val.strip())
                blocks[marker].append(block)
                block_last = block

            else:
                block = Block()
                block.contribute(line)
                blocks[Block.unmarked].append(block)
                processed.append(block)

        if block_last:
            # block in the last line
            processed.append(block_last)

        self.markers_detected = self.markers_detected or marker_detected

        return blocks, processed

    def _parse(self, value: str) -> Docstring | None:

        blocks, processed = self.parse_blocks(
            pattern=self.re_markers,
            value=value,
        )

        return Docstring(
            text=self.postprocess('\n'.join(map(str, blocks[Block.unmarked]))),
            params=self.to_dict(blocks['param']),
            returns=self.to_list(blocks['return']),
            raises=self.to_dict(blocks['raises']),
        )


class GoogleParser(DocstrParser):
    alias: str = 'google'


class NumpyParser(DocstrParser):
    alias: str = 'numpy'
