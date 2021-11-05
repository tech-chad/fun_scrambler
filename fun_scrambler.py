# fun-scrambler
import argparse
import curses
import random
import time

from typing import Optional
from typing import Sequence


char_set = [x for x in "ABCDEFGHIJKLMNOPQRTSTUVWXYZabcdefghijklmnopqrstuvwxyz 0123456789"]
curses_color = {"green": curses.COLOR_GREEN, "red": curses.COLOR_RED,
                "blue": curses.COLOR_BLUE, "cyan": curses.COLOR_CYAN,
                "yellow": curses.COLOR_YELLOW, "magenta": curses.COLOR_MAGENTA,
                "white": curses.COLOR_WHITE, "black": curses.COLOR_BLACK}


def set_curses_color(fg_color: Optional[str] = "white", option: Optional[str] = "single"):
    if option == "single":
        color = curses_color[fg_color]
        curses.init_pair(1, color, curses.COLOR_BLACK)
        curses.init_pair(2, color, curses.COLOR_BLACK)
        curses.init_pair(3, color, curses.COLOR_BLACK)
        curses.init_pair(4, color, curses.COLOR_BLACK)
        curses.init_pair(5, color, curses.COLOR_BLACK)
        curses.init_pair(6, color, curses.COLOR_BLACK)
        curses.init_pair(7, color, curses.COLOR_BLACK)
        curses.init_pair(8, color, curses.COLOR_BLACK)


def scrambler_loop(screen, args):
    all_char_set = ["T"] if args.test_mode else char_set
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().

    set_curses_color("magenta")

    while True:

        size_y, size_x = screen.getmaxyx()
        for y in range(0, size_y - 1):
            for x in range(0, size_x - 1):
                random_color = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
                r = random.randint(0, 10)
                if r >= 6:
                    screen.addstr(y, x,
                                  random.choice(all_char_set),
                                  curses.color_pair(random_color))
        time.sleep(0.1)

        ch = screen.getch()
        if ch in [81, 113]:
            break

    screen.clear()
    screen.refresh()


def argument_parsing(agv: Optional[Sequence] = None):
    parser = argparse.ArgumentParser()

    parser.add_argument("--test_mode", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args(agv)


def main():
    args = argument_parsing()
    curses.wrapper(scrambler_loop, args)


if __name__ == "__main__":
    exit(main())
