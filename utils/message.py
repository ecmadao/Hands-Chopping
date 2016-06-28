from colorama import Fore


def colorful_text(text, color=Fore.RESET):
    return color + text + Fore.RESET


def error_message(message='Ops, there are some error...'):
    print(colorful_text(message, Fore.RED))

