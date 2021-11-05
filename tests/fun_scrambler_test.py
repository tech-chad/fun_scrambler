import pytest

from hecate import Runner


def run_fun_scrambler(*args):
    options = [a for a in args]
    return ["python3", "fun_scrambler.py"] + options


def test_fun_scrambler_test_mode():
    with Runner(*run_fun_scrambler("--test_mode")) as h:
        h.await_text("T")


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_fun_scrambler_quit(test_key):
    with Runner(*run_fun_scrambler("--test_mode")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()