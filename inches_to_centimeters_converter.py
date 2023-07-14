# coding: utf-8


import sys
from typing import Union


class __PrintEffects:
    pass


class __KeyboardEffects:
    pass


class __TerminalEffects:
    pass


class __SysEffects:
    pass


_INCHES_TO_CENTIMETERS_FACTOR = 2.54
_CENTIMETERS_TO_INCHES_FACTOR = 0.394

_VOCAB = {
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


def _print_result(unit: str, res: float) -> __PrintEffects:
    print(f"Converted to {unit.lower()}:\n> {res}")


def _print_invalid_input_error() -> __PrintEffects:
    print(f"\n{_VOCAB['INVALID_INPUT']}\n")


def _value_prompt_str(unit: str) -> str:
    return f"{unit}:\n> "


def _sanitize_user_input(user_input: str) -> str:
    return user_input.strip().lower()


def _is_number(unknown_value) -> bool:
    try:
        float(unknown_value)
        return True
    except ValueError:
        return False


def _terminate(msg: str = "") -> Union[__PrintEffects, __SysEffects]:
    print(msg)
    exit(0)


def _input_handling_keyboard_interrupt_wrapper(input_msg: str) -> Union[str, __PrintEffects, __KeyboardEffects]:
    try:
        user_input = input(input_msg)
        return user_input
    except (KeyboardInterrupt, EOFError):
        _terminate(f"\n{_VOCAB['QUIT_MSG']}")


def _inches_to_centimeters_prompt() -> Union[float, __PrintEffects, __KeyboardEffects]:
    user_input = _input_handling_keyboard_interrupt_wrapper(
        _value_prompt_str(_VOCAB["INCHES"])
    )
    user_input = _sanitize_user_input(user_input)
    if not _is_number(user_input):
        _print_invalid_input_error()
        return _inches_to_centimeters_prompt()
    else:
        res = round(float(user_input) * _INCHES_TO_CENTIMETERS_FACTOR, 3)
        return res


def _centimeters_to_inches_prompt() -> Union[float, __PrintEffects, __KeyboardEffects]:
    user_input = _input_handling_keyboard_interrupt_wrapper(
        _value_prompt_str(_VOCAB["CENTIMETERS"])
    )
    user_input = _sanitize_user_input(user_input)
    if not _is_number(user_input):
        _print_invalid_input_error()
        return _centimeters_to_inches_prompt()
    else:
        res = round(float(user_input) * _CENTIMETERS_TO_INCHES_FACTOR, 3)
        return res


def _pause() -> Union[__PrintEffects, __KeyboardEffects, __TerminalEffects, __SysEffects]:
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
            _terminate(f"\n{_VOCAB['QUIT_MSG']}")
        finally:
            if not sys.stdin.closed:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def _prompt_loop() -> Union[__PrintEffects, __KeyboardEffects, __TerminalEffects, __SysEffects]:
    QUIT_CHOICE = "c"

    while True:
        print(_VOCAB["CONVERSION_PROMPT_MSG"])
        print(*_VOCAB["OPTIONS"], sep="\n")
        user_input = _input_handling_keyboard_interrupt_wrapper("> ")
        user_input = _sanitize_user_input(user_input)
        res = 0
        if user_input == "a":
            res = _inches_to_centimeters_prompt()
            _print_result(_VOCAB["CENTIMETERS"], res)
        elif user_input == "b":
            res = _centimeters_to_inches_prompt()
            _print_result(_VOCAB["INCHES"], res)
        elif user_input == QUIT_CHOICE:
            print(_VOCAB["QUIT_MSG"])
            break
        else:
            _print_invalid_input_error()
            continue

        if user_input != QUIT_CHOICE:
            _pause()
            print()


def run() -> Union[__PrintEffects, __KeyboardEffects, __TerminalEffects, __SysEffects]:
    print(_VOCAB["WELCOME_MSG"])
    _prompt_loop()


if __name__ == "__main__":
    run()
