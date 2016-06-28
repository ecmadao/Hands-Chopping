#!usr/bin/env python
"""message utils

make colorful text
print error message

Fore # BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back # BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style # DIM, NORMAL, BRIGHT, RESET_ALL
"""

from colorama import Fore


def colorful_text(text, color=Fore.RESET):
    return color + text + Fore.RESET


def error_message(message='Ops, there are some error...'):
    print(colorful_text(message, Fore.RED))
