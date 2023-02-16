"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from pytest import raises

from farben.utils import RGB_REGEX, hex2rgb, rgb2hex


def test_color_regex() -> None:
    """
    Tests 'RGB_REGEX'
    """

    # Setup
    expected = {
        "red": "0",
        "green": "0",
        "blue": "0",
    }

    # Assert results
    assert RGB_REGEX.match("0,0,0").groupdict() == expected
    assert RGB_REGEX.match("rgb(0,0,0)").groupdict() == expected
    assert RGB_REGEX.match(" 0  ,0,   0    ").groupdict() == expected
    assert RGB_REGEX.match("rgb( 0  ,0,   0   )").groupdict() == expected


def test_hex2rgb() -> None:
    """
    Tests 'hex2rgb()'
    """

    # Assert results
    assert hex2rgb("000000") == "0,0,0"
    assert hex2rgb("#000000") == "0,0,0"


def test_hex2rgb_invalid() -> None:
    """
    Tests 'hex2rgb()' (invalid input)
    """

    # Assert exception
    with raises(ValueError):
        # Run function
        hex2rgb("invalid")


def test_rgb2hex() -> None:
    """
    Tests 'rgb2hex()'
    """

    # Assert results
    assert rgb2hex([0, 0, 0]) == "#000000"
    assert rgb2hex(["0", "0", "0"]) == "#000000"
    assert rgb2hex("0,0,0") == "#000000"
    assert rgb2hex(" 0  ,0,   0   ") == "#000000"
    assert rgb2hex("rgb(0,0,0)") == "#000000"
    assert rgb2hex("rgb( 0  ,0,   0   )") == "#000000"


def test_rgb2hex_invalid() -> None:
    """
    Tests 'rgb2hex()' (invalid input)
    """

    # Assert exception
    with raises(ValueError):
        # Run function
        rgb2hex("invalid")
