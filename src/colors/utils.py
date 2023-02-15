"""
This module is part of the 'we-love-colors' package,
which is released under MIT license.
"""

import re
from typing import Callable, List, Union

RGB_REGEX = re.compile(
    r"""
    # leading 'rgb' & opening bracket (optional)
    (?:rgb\()?
    # red
    (?P<red>[0-9]|1[0-9]|2[0-4][0-9]|25[0-5])*
    # whitespace(s) & comma
    (?:\s*),(?:\s*)
    # green
    (?P<green>[0-9]|1[0-9]|2[0-4]|25[0-5])*
    # whitespace(s) & comma
    (?:\s*),(?:\s*)
    # blue
    (?P<blue>[0-9]|1[0-9]|2[0-4]|25[0-5])*
    # closing bracket (optional)
    \)?
    """,
    re.VERBOSE,
)


def natural_sort(unsorted: List[dict], key: str = "code") -> None:
    """
    Applies a natural sort order to dictionaries inside a given list

    See https://stackoverflow.com/a/8940266

    :param unsorted: list List of dictionaries to be sorted
    :param key: Key to sort by
    :return: None
    """

    def normalize_input(text: str) -> Union[int, str]:
        """
        :param text: str
        :return: int | str
        """

        return int(text) if text.isdigit() else text

    def get_alphanum_key(func: Callable) -> Callable:
        """
        :param func: typing.Callable
        :return: typing.Callable
        """

        return lambda s: [normalize_input(c) for c in re.split("([0-9]+)", func(s))]

    sort_key = get_alphanum_key(lambda x: x[key])
    unsorted.sort(key=sort_key)


def rgb2hex(rgb_values: Union[List[Union[int, str]], str]) -> str:
    """
    Converts RGB values to HEX colors

    See https://stackoverflow.com/a/3380739

    :param rgb_values: list | str RGB values
    :return: str HEX color
    :raises: ValueError Invalid input string
    """

    if isinstance(rgb_values, str):
        # Check whether string actually contains RGB values
        matches = RGB_REGEX.match(rgb_values)

        # If input string is invalid ..
        if matches is None:
            # .. report back
            raise ValueError(f'Invalid RGB string: "{rgb_values}"')

        # Store matches
        rgb_values = [
            matches.group("red"),
            matches.group("green"),
            matches.group("blue"),
        ]

    # Unpack RGB values
    red, green, blue = [int(rgb) for rgb in rgb_values]

    # Convert to HEX & uppercase
    return f"#{red:02x}{green:02x}{blue:02x}".upper()


def hex2rgb(hexa: str) -> str:
    """
    Converts HEX color to RGB values

    See https://stackoverflow.com/a/29643643

    :param hexa: str HEX color
    :return: str RGB values
    """

    return ",".join([str(int(hexa.lstrip("#")[i : i + 2], 16)) for i in (0, 2, 4)])
