import pytest

import fun_scrambler


@pytest.mark.parametrize("test_value, expected", [
    ([], False), (["--test_mode"], True)
])
def test_argument_parser_test_mode(test_value, expected):
    result = fun_scrambler.argument_parsing(test_value)
    assert result.test_mode == expected


@pytest.mark.parametrize("test_value, expected",[
    (["-c", "red"], "red"), (["--color", "Yellow"], "yellow"),
    (["-c", "GREEN"], "green")
])
def test_argument_parser_color(test_value, expected):
    result = fun_scrambler.argument_parsing(test_value)
    assert result.color == expected


@pytest.mark.parametrize("test_value, expected", [
    ([], 5), (["-d", "5"], 5), (["--delay", "1"], 1),
    (["--delay", "3"], 3)
])
def test_argument_parser_delay(test_value, expected):
    result = fun_scrambler.argument_parsing(test_value)
    assert result.delay == expected


@pytest.mark.parametrize("test_value, expected", [
    ("red", "red"), ("Green", "green"), ("BLUE", "blue")
])
def test_argparse_color_type_valid(test_value, expected):
    result = fun_scrambler.argparse_color_type(test_value)
    assert result == expected


@pytest.mark.parametrize("test_value", [
    "orange", "blue10", "2321239", "*blue", "rrrrrrrrrr"
])
def test_argparse_color_time_invalid(test_value):
    with pytest.raises(fun_scrambler.argparse.ArgumentTypeError):
        fun_scrambler.argparse_color_type(test_value)


@pytest.mark.parametrize("test_value, expected", [
    ("0", 0), ("1", 1), ("2", 2), ("3", 3), ("4", 4),
    ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9),
])
def test_positive_int_zero_to_nine(test_value, expected):
    result = fun_scrambler.positive_int_zero_to_nine(test_value)
    assert result == expected


@pytest.mark.parametrize("test_value", [
    "30", "gh0", "1p", "1%", "2-5", "ben"
])
def test_positive_int_zero_to_nine_invalid(test_value):
    with pytest.raises(fun_scrambler.argparse.ArgumentTypeError):
        fun_scrambler.positive_int_zero_to_nine(test_value)
