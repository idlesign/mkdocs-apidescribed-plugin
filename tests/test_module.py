
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
