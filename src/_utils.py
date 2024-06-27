from random import choice as choice_char
from string import ascii_letters, digits

DEFAULT_CHARS = ascii_letters + digits


def generate_string(length: int = 16):
    return "".join(choice_char(DEFAULT_CHARS) for _ in range(length))

