import pytest

import fun_scrambler


@pytest.mark.parametrize("test_value, expected", [
    ([], False), (["--test_mode"], True)
])
def test_argument_parser_test_mode(test_value, expected):
    result = fun_scrambler.argument_parsing(test_value)
    assert result.test_mode == expected
