# coding: utf-8

import sys
import tty
import termios

INCHES_TO_CENTIMETERS_FACTOR = 2.54
CENTIMETERS_TO_INCHES_FACTOR = 0.394

VOCAB = {
    "WELCOME_MSG": "Hello world!\n",
    "CONVERSION_PROMPT_MSG": "Please, choose a conversion option:",
    "INVALID_INPUT": "Invalid input!",
    "CENTIMETERS": "Centimeters",
    "INCHES": "Inches",
    "OPTIONS": [
        "'A' ->\tConvert inches to centimeters,",
        "'B' ->\tConvert centimeters to inches,",
        "'C' ->\tQuit",
    ],
    "QUIT_MSG": "Goodbye!",
}


def input_handling_keyboard_interrupt_wrapper(input_msg: str) -> str:
    try:
        user_input = input(input_msg)
        return user_input
    except (KeyboardInterrupt, EOFError):
        print(f"\n{VOCAB['QUIT_MSG']}")
        exit(0)


def pause():
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def display_result(unit: str, res: float):
    print(f"Converted to {unit.lower()}:\n> {res}")


def value_prompt(unit: str):
    return f"{unit}:\n> "


def sanitize_user_input(user_input: str) -> str:
    return user_input.strip().lower()


def is_number(unknown_value) -> bool:
    try:
        float(unknown_value)
        return True
    except ValueError:
        return False


def inches_to_centimeters() -> float:
    user_input = input_handling_keyboard_interrupt_wrapper(
        value_prompt(VOCAB["INCHES"])
    )
    user_input = sanitize_user_input(user_input)
    if not is_number(user_input):
        print(f"\n{VOCAB['INVALID_INPUT']}")
        return inches_to_centimeters()
    else:
        res = round(float(user_input) * INCHES_TO_CENTIMETERS_FACTOR, 3)
        return res


def centimeters_to_inches() -> float:
    user_input = input_handling_keyboard_interrupt_wrapper(
        value_prompt(VOCAB["CENTIMETERS"])
    )
    user_input = sanitize_user_input(user_input)
    if not is_number(user_input):
        print(f"\n{VOCAB['INVALID_INPUT']}")
        return centimeters_to_inches()
    else:
        res = round(float(user_input) * CENTIMETERS_TO_INCHES_FACTOR, 3)
        return res


def prompt():
    QUIT_CHOICE = "c"

    while True:
        print(VOCAB["CONVERSION_PROMPT_MSG"])
        print(*VOCAB["OPTIONS"], sep="\n")
        user_input = input_handling_keyboard_interrupt_wrapper("> ")
        user_input = sanitize_user_input(user_input)
        res = 0
        if user_input == "a":
            res = inches_to_centimeters()
            display_result(VOCAB["CENTIMETERS"], res)
        elif user_input == "b":
            res = centimeters_to_inches()
            display_result(VOCAB["INCHES"], res)
        elif user_input == QUIT_CHOICE:
            print(VOCAB["QUIT_MSG"])
            break
        else:
            print(f"\n{VOCAB['INVALID_INPUT']}")
            prompt()

        if user_input != QUIT_CHOICE:
            pause()
            print()


def runtime():
    print(VOCAB["WELCOME_MSG"])
    prompt()


if __name__ == "__main__":
    runtime()
