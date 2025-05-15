from textwrap import dedent, indent

import markdown
import pytest

from mkdocs_apidescribed.extension import makeExtension


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
