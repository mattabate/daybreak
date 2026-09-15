import re
import shlex
from pathlib import Path

import pytest

from daybreak.cli import main

README = Path(__file__).resolve().parent.parent / "README.md"


def run(capsys, argv):
    assert main(argv) == 0
    return capsys.readouterr().out


def test_readme_console_blocks_are_real_output(capsys):
    blocks = re.findall(r"```console\n(.*?)```", README.read_text(), re.S)
    assert blocks
    for block in blocks:
        command, *expected = block.splitlines()
        assert command.startswith("$ daybreak"), command
        out = run(capsys, shlex.split(command[2:])[1:])
        assert out.rstrip("\n") == "\n".join(expected).rstrip("\n"), command


def test_default_is_the_week(capsys):
    assert run(capsys, []) == run(capsys, ["5", "2"])


def test_legacy_output(capsys):
    out = run(capsys, ["5", "2", "--legacy", "--times"])
    assert out.startswith("First passage 5 days\nSecond passage 2 days\nWays to split:\n\n")
    assert "Chunks: 9\nStep size for Poem 1: 13 hours 20 minutes\n" in out
    assert "Step size for Poem 2: 1 hour 46 minutes 40 seconds\n" in out
    assert "times ['12:00:00 AM', '01:20:00 PM', '02:40:00 AM'," in out


def test_no_split(capsys):
    assert run(capsys, ["3", "3"]) == "no split works for 3 days and 3 days (up to 9999 steps)\n"


@pytest.mark.parametrize("argv", [["5"], ["5", "2", "1"], ["0", "2"], ["5", "2", "--max-steps", "0"]])
def test_bad_arguments_exit_2(argv):
    with pytest.raises(SystemExit) as exc:
        main(argv)
    assert exc.value.code == 2
