import sys
import io
from unittest.mock import patch
import runpy
import pytest
from app.main import fahrenheit_to_celsius


def test_fahrenheit_to_celsius_freezing():
    """32°F should be exactly 0°C."""
    assert fahrenheit_to_celsius(32.0) == pytest.approx(0.0)


def test_fahrenheit_to_celsius_boiling():
    """212°F should be exactly 100°C."""
    assert fahrenheit_to_celsius(212.0) == pytest.approx(100.0)


def test_fahrenheit_to_celsius_negative_same():
    """-40°F should equal -40°C."""
    assert fahrenheit_to_celsius(-40.0) == pytest.approx(-40.0)


def test_cli_with_argument():
    """CLI with a Fahrenheit argument prints the conversion."""
    test_args = ["main.py", "75"]
    with patch("sys.argv", test_args), \
         patch("app.main.flask_app.run") as mock_run, \
         patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        runpy.run_module("app.main", run_name="__main__", alter_sys=True)
        output = mock_stdout.getvalue()
        assert "75.0°F" in output
        assert "°C" in output
        mock_run.assert_not_called()


def test_cli_without_argument_starts_server():
    """Without arguments, the CLI starts the Flask admin server."""
    test_args = ["main.py"]
    with patch("sys.argv", test_args), \
         patch("app.main.flask_app.run") as mock_run, \
         patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
        runpy.run_module("app.main", run_name="__main__", alter_sys=True)
        output = mock_stdout.getvalue()
        assert "Starting Flask admin server" in output
        mock_run.assert_called_once()


def test_cli_invalid_argument():
    """Non-numeric Fahrenheit argument causes argparse to exit."""
    test_args = ["main.py", "abc"]
    with patch("sys.argv", test_args), \
         patch("sys.stderr", new_callable=io.StringIO):
        with pytest.raises(SystemExit):
            runpy.run_module("app.main", run_name="__main__", alter_sys=True)