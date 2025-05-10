import re

from markdown import Extension
from markdown.preprocessors import Preprocessor
from mkdocs.plugins import get_plugin_logger

from .config import get_config
from .formatter import Formatter
from .inspector import inspect

log = get_plugin_logger(__name__)


class ApidescribedProcessor(Preprocessor):

    RE_START = re.compile(r'^::: apidescribed:(.*)')

    cls_fmt = Formatter

    @classmethod
    def process_instruction(cls, *, target: str, config: dict) -> list[str]:
        cls_fmt = cls.cls_fmt
        out = []
        last_type = ''

        root, symbols = inspect(
            target,
            types=config['types'],
            ignore=config['ignore'],
            only=config['only'],
            inherited=config['inherited'],
        )
        formatter = cls_fmt(symbol=root, config=config)

        if prolog := formatter.run():
            out.append(prolog)

        for symbol in symbols:
            formatter = cls_fmt(symbol=symbol, config=config)

            if symbol.depth == 0:
                if last_type != symbol.type.name and (categorized := formatter.format_category()):
                    out.append(categorized)

                last_type = symbol.type.name

            formatted = formatter.run()
            out.append(formatted)

        return out

    def run(self, lines: list[str]) -> list[str]:
        out = []

        re_start = self.RE_START
        process_instruction = self.process_instruction
        instruction = []

        for line in lines:

            to_add = [line]

            if matched := re_start.search(line):
                instruction.append(matched[1].strip())
                to_add = []

            elif instruction:
                if line.startswith('    '):
                    # new option for instruction
                    instruction.append(line)
                    to_add = []
                else:
                    # end of an instruction options block
                    debug = False

                    try:
                        target = instruction[0]
                        config = get_config('\n'.join(instruction[1:]))

                        skip = config['skip']
                        debug = config['debug']

                        if skip:
                            log.debug(f'Skipped instruction for: {target}')

                        else:
                            to_add = process_instruction(target=target, config=config)

                    except Exception as e:

                        to_add = [Formatter.format_error(e, instruction=instruction, debug=debug)]
                        log.exception('Automated API documentation error')

                    finally:
                        instruction.clear()

            out.extend(to_add)

        return out


class ApiDescribedExtension(Extension):

    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(ApidescribedProcessor(md.parser), "apidescribed", 110)


def makeExtension(**kwargs):
    return ApiDescribedExtension(**kwargs)
