
def test_parser_sphinx(get_docstring_parsed):
    docstr = get_docstring_parsed('docstr_sphinx_1.txt')

    assert docstr.raises == {'KeyError': 'If something other happens', 'ValueError': 'If something happens'}
    assert docstr.returns == ['This is returned', 'This is also returned']
    assert '!!! note\n    Some note here.' in docstr.text
    assert '```bash\ncd ~\ntouch this/\n```' in docstr.text
    assert docstr.params == {
        'a': 'comment for a\n\n',
        'another': 'text for another\n', 'args': 'info for args',
        'b': 'hint for b\nSeveral lines.\n\n!!! warning\n    Some warning\n\nAnother line.',
        'kwargs': 'description for kwargs'}


def test_parser_google(get_docstring_parsed):
    docstr = get_docstring_parsed('docstr_google_1.txt')

    assert docstr.raises == {'AttributeError': 'Can raise\n    this in some cases.', 'ValueError': 'If something.\n'}
    assert docstr.returns == ['True if successful, False otherwise.\n    Even more text for return description.']
    assert docstr.params == {
        '**kwargs': 'Keyword parameters\n', 'e': 'Param e\n', 'q': 'Param q\n',
        'w': 'Param w\n    Description continued.'}
