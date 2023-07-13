# coding: utf-8

import sys

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


def terminate(msg: str = ''):
    print(msg)
    exit(0)


def input_handling_keyboard_interrupt_wrapper(input_msg: str) -> str:
    try:
        user_input = input(input_msg)
        return user_input
    except (KeyboardInterrupt, EOFError):
        terminate(f"\n{VOCAB['QUIT_MSG']}")


def pause():
    if sys.platform.startswith("win"):
        import msvcrt

        msvcrt.getch()
    else:
        import termios
        import tty

        old_settings = termios.tcgetattr(sys.stdin)
        try:
            sys.stdin.flush()
            tty.setcbreak(sys.stdin.fileno())
            new_settings = termios.tcgetattr(sys.stdin)
            new_settings[3] = new_settings[3] & ~termios.ICANON
            termios.tcsetattr(sys.stdin, termios.TCSANOW, new_settings)
            input()
        except:
            terminate(f"\n{VOCAB['QUIT_MSG']}")
        finally:
            if not sys.stdin.closed:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def display_result(unit: str, res: float):
    print(f"Converted to {unit.lower()}:\n> {res}")


def print_invalid_input_error():
    print(f"\n{VOCAB['INVALID_INPUT']}\n")


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
        print_invalid_input_error()
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
        print_invalid_input_error()
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
            print_invalid_input_error()
            continue

        if user_input != QUIT_CHOICE:
            pause()
            print()


def runtime():
    print(VOCAB["WELCOME_MSG"])
    prompt()


if __name__ == "__main__":
    runtime()
