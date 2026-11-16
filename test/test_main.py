# -*- coding: utf-8 -*-
import sys

import pytest

from src.main import get_path_from_arguments, get_reader, main
from src.TextDataReader import TextDataReader
from src.YAMLDataReader import YAMLDataReader


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(
        correct_arguments_string: tuple[list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(
        noncorrect_arguments_string: list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])
    assert e.type == SystemExit


@pytest.mark.parametrize("path, reader_class", [
    ("data/data.txt", TextDataReader),
    ("data/data.yaml", YAMLDataReader),
    ("data/data.yml", YAMLDataReader),
    ("DATA.YAML", YAMLDataReader),
])
def test_get_reader(path: str, reader_class: type) -> None:
    # src.X и X — разные объекты модулей из-за PYTHONPATH=./:./src,
    # поэтому сравниваем имена классов.
    assert type(get_reader(path)).__name__ == reader_class.__name__


def test_get_reader_unsupported_format() -> None:
    with pytest.raises(ValueError):
        get_reader("data/data.csv")


def test_main_with_yaml(tmpdir, monkeypatch, capsys) -> None:
    p = tmpdir.join("students.yaml")
    p.write_text("- Иванов Иван:\n    химия: 80\n    физика: 90\n",
                 encoding='utf-8')
    monkeypatch.setattr(sys, "argv", ["main.py", "-p", str(p)])
    main()
    out = capsys.readouterr().out
    assert "Иванов Иван" in out
    assert "85.0" in out
    assert "Number of excellent students:  0" in out
