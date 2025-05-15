
def test_smoke(apid, datafix_read):

    smoked = datafix_read('smoke.html')

    assert apid(
        options=(
            'location:\n'
            '    mode: hidden\n'
            'ignore:\n'
            '    - _*\n'
        )
    ) == smoked

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


def test_imports():
    # import probe
    from mkdocs_apidescribed.probe import ENVIRON
    assert ENVIRON

    # import plugin
    from mkdocs_apidescribed.plugin import ApiDescribedPlugin
    assert ApiDescribedPlugin
