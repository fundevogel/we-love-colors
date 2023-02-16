"""
This module is part of the 'farben' package,
which is released under MIT license.
"""

from click.testing import CliRunner

from farben import cli


def test_cli():
    """
    Tests CLI interface
    """

    # Setup
    # (1) CLI runner
    runner = CliRunner()

    # Run function
    result = runner.invoke(cli, ["-p", "invalid"])

    # Assert result
    assert result.exit_code == 2
