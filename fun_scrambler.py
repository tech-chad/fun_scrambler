# fun-scrambler
import argparse
import curses
import datetime
import random
import time

from typing import Optional
from typing import Sequence


CHAR_SET = [x for x in "ABCDEFGHIJKLMNOPQRTSTUVWXYZabcdefghijklmnopqrstuvwxyz 0123456789"]
CURSES_COLORS = {"green": curses.COLOR_GREEN, "red": curses.COLOR_RED,
                 "blue": curses.COLOR_BLUE, "cyan": curses.COLOR_CYAN,
                 "yellow": curses.COLOR_YELLOW, "magenta": curses.COLOR_MAGENTA,
                 "white": curses.COLOR_WHITE, "black": curses.COLOR_BLACK}
COLORS = ["red", "green", "blue", "cyan", "yellow", "magenta", "white"]
DELAY = {0: 0.02, 1:  0.04, 2: 0.05, 3: 0.06,
         4: 0.09, 5: 0.1, 6: 0.2, 7: 0.3, 8: 0.4, 9: 0.5}


def set_curses_color(fg_color: Optional[str] = "white", option: Optional[str] = "single"):
    if option == "single":
        color = CURSES_COLORS[fg_color]
        curses.init_pair(1, color, curses.COLOR_BLACK)
        curses.init_pair(2, color, curses.COLOR_BLACK)
        curses.init_pair(3, color, curses.COLOR_BLACK)
        curses.init_pair(4, color, curses.COLOR_BLACK)
        curses.init_pair(5, color, curses.COLOR_BLACK)
        curses.init_pair(6, color, curses.COLOR_BLACK)
        curses.init_pair(7, color, curses.COLOR_BLACK)
        curses.init_pair(8, color, curses.COLOR_BLACK)


def scrambler_loop(screen, args: argparse.Namespace):
    all_char_set = ["T"] if args.test_mode else CHAR_SET
    color = args.color
    delay = DELAY[args.delay]
    bold_all = args.bold_all
    bold = args.bold
    curses.curs_set(0)  # Set the cursor to off.
    screen.timeout(0)  # Turn blocking off for screen.getch().
    set_curses_color(color)
    if args.start_timer:
        time.sleep(args.start_timer)
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=args.run_timer)
    while True:

        size_y, size_x = screen.getmaxyx()
        for y in range(0, size_y - 1):
            for x in range(0, size_x - 1):
                if bold_all:
                    char_bold = curses.A_BOLD
                elif bold and random.randint(0, 10) <= 2:
                    char_bold = curses.A_BOLD
                else:
                    char_bold = 0
                random_color = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
                r = random.randint(0, 10)
                if r >= 6:
                    screen.addstr(y, x,
                                  random.choice(all_char_set),
                                  curses.color_pair(random_color) + char_bold)
        time.sleep(delay)
        if args.test_mode:
            screen.addstr(size_y - 1, 0, color)
        if args.run_timer and datetime.datetime.now() >= end_time:
            break
        ch = screen.getch()
        if ch in [81, 113]:
            break
        elif args.screen_saver and ch != -1:
            break
        elif ch == 66:  # B
            bold_all = not bold_all
        elif ch == 98:  # b
            bold = not bold
        elif ch == 114:  # r
            color = "red"
            set_curses_color(color)
        elif ch == 116:  # t
            color = "green"
            set_curses_color(color)
        elif ch == 121:  # y
            color = "blue"
            set_curses_color(color)
        elif ch == 117:  # u
            color = "yellow"
            set_curses_color(color)
        elif ch == 105:  # i
            color = "magenta"
            set_curses_color(color)
        elif ch == 111:  # o
            color = "cyan"
            set_curses_color(color)
        elif ch == 112:  # p
            color = "white"
            set_curses_color(color)
        elif ch in [48, 49, 50, 51, 52, 53, 54, 56, 57]:
            delay = DELAY[int(chr(ch))]
    screen.clear()
    screen.refresh()


def positive_int_zero_to_nine(value: str) -> int:
    """
    Used with argparse.
    Checks to see if value is positive int between 0 and 10.
    """
    try:
        int_value = int(value)
        if int_value < 0 or int_value >= 10:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive "
                                             f"int value 0 to 9")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int "
                                         f"value 0 to 9")


def argparse_color_type(value: str) -> str:
    lower_value = value.lower()
    if lower_value in COLORS:
        return lower_value
    else:
        raise argparse.ArgumentTypeError(f"{value} is not a valid color")


def positive_int(value: str) -> int:
    """
    Used by argparse.
    Checks to see if the value is positive.
    """
    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    else:
        if int_value <= 0:
            raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return int_value


def argument_parsing(agv: Optional[Sequence] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--color", type=argparse_color_type, default="white",
                        help="Set the character color.")
    parser.add_argument("-d", "--delay", type=positive_int_zero_to_nine,
                        default=5, help="Set the delay (Speed) 0-fast, 9-slow")
    parser.add_argument("-S", "--screen_saver", action="store_true",
                        help="Screen saver mode. Any key wll exit")
    parser.add_argument("-s", "--start_timer", type=positive_int, default=0,
                        help="Number of seconds to wait before starting.")
    parser.add_argument("-r", "--run_timer", type=positive_int, default=0,
                        help="Number of second to wait before quitting")
    parser.add_argument("-B", "--bold_all", action="store_true",
                        help="Bold all characters.")
    parser.add_argument("-b", "--bold", action="store_true",
                        help="Bold some of the characters")

    parser.add_argument("--test_mode", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args(agv)


def main():
    args = argument_parsing()
    curses.wrapper(scrambler_loop, args)


if __name__ == "__main__":
    exit(main())
