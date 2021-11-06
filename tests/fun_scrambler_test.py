import pytest

from hecate import Runner


def run_fun_scrambler(*args):
    options = [a for a in args]
    return ["python3", "fun_scrambler.py"] + options


def test_fun_scrambler_test_mode():
    with Runner(*run_fun_scrambler("--test_mode")) as h:
        h.await_text("T")


def test_fun_scrambler_no_test_mode():
    with Runner(*run_fun_scrambler()) as h:
        h.await_text("A", timeout=4)
        h.await_text("y", timeout=4)


@pytest.mark.parametrize("test_key", ["q", "Q"])
def test_fun_scrambler_quit(test_key):
    with Runner(*run_fun_scrambler("--test_mode")) as h:
        h.await_text("T")
        h.write(test_key)
        h.press("Enter")
        h.await_exit()


@pytest.mark.parametrize("test_value", [
    "red", "blue", "green", "yellow", "cyan", "magenta", "white"
])
def test_fun_scrambler_cli_set_color(test_value):
    with Runner(*run_fun_scrambler("--test_mode", "-c", test_value)) as h:
        h.await_text("T")
        h.await_text(test_value)


@pytest.mark.parametrize("test_key, expected", [
    ("r", "red"), ("t", "green"), ("y", "blue"), ("u", "yellow"),
    ("i", "magenta"), ("o", "cyan"), ("p", "white")
])
def test_fun_scrambler_running_set_color(test_key, expected):
    with Runner(*run_fun_scrambler("--test_mode")) as h:
        h.await_text("T")
        h.write(test_key)
        h.await_text(expected)


def test_run_scrambler_running_set_colors_again():
    with Runner(*run_fun_scrambler("--test_mode", "--color", "red")) as h:
        h.await_text("T")
        h.await_text("red")
        h.write("u")
        h.await_text("yellow")
        h.write("o")
        h.await_text("cyan")
        h.write("t")
        h.await_text("green")
        h.write("i")
        h.await_text("magenta")
        h.write("r")
        h.await_text("red")
        h.write("p")
        h.await_text("white")
