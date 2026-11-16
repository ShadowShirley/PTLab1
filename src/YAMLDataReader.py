# -*- coding: utf-8 -*-
import yaml

from Types import DataType
from DataReader import DataReader


class YAMLDataReader(DataReader):
    """Чтение данных о студентах из YAML-файла вида:

    - Иванов Иван Иванович:
        математика: 67
        литература: 100
    - Петров Петр Петрович:
        химия: 87
    """

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            content = yaml.safe_load(file)
        if content is None:
            return self.students
        if not isinstance(content, list):
            raise ValueError("YAML root must be a list of students")
        for item in content:
            if not isinstance(item, dict):
                raise ValueError(f"Invalid student record: {item!r}")
            for name, subjects in item.items():
                self.students[str(name).strip()] = \
                    self._parse_subjects(subjects)
        return self.students

    @staticmethod
    def _parse_subjects(subjects) -> list[tuple[str, int]]:
        if subjects is None:
            return []
        if not isinstance(subjects, dict):
            raise ValueError(f"Invalid subjects record: {subjects!r}")
        return [(str(subj).strip(), int(score))
                for subj, score in subjects.items()]
