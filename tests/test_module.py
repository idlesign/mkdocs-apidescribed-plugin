
import pytest

import markdown

from mkdocs_apidescribed.extension import makeExtension


def test_smoke(apid, datafix_read):

    smoked = datafix_read('smoke.html')

    out = apid(
        options=(
            'location:\n'
            '    mode: hidden\n'
            'ignore:\n'
            '    - _*\n'
        )
    )
    assert out == smoked

    # bogus config lead to default config
    assert apid(
        options=(
            '- a\n'
            'b:\n'
            '    c: d\n'
        )
    ) == smoked


def test_skip(apid):

    assert apid(options='skip: true\n') == '<p>before\nafter</p>'


def test_exception(apid):

    out = apid(
        target='somepackage.somemodule',
        options='debug: true\n'
    )
    assert '??? failure "Automated documentation error: ImportError"' in out
    assert 'Traceback (most recent call last):'


def test_error_describe(apid):

    out = apid(
        target="somepackage.somemodule",
        options="error: describe\n"
    )
    assert '??? failure "Automated documentation error: ImportError"' in out


def test_error_ignore(apid):

    assert apid(target="somepackage.somemodule", options="error: ignore\n") == '<p>before\nafter</p>'


def test_error_break(apid):

    with pytest.raises(ImportError):
        apid(target="somepackage.somemodule", options="error: break\n")


def test_global_config():

    text = "::: apidescribed: mkdocs_apidescribed.probe\n"

    out_default = markdown.markdown(text, extensions=[makeExtension()])
    out_global = markdown.markdown(text, extensions=[makeExtension(heading_base=4)])
    out_override = markdown.markdown(
        f"{text}    heading_base: 5\n",
        extensions=[makeExtension(heading_base=4)],
    )

    assert "<h2" in out_default
    assert "<h4" in out_global
    assert "<h5" in out_override


def test_imports():
    # import probe
    from mkdocs_apidescribed.probe import ENVIRON
    assert ENVIRON

    # import plugin
    from mkdocs_apidescribed.plugin import ApiDescribedPlugin
    assert ApiDescribedPlugin
