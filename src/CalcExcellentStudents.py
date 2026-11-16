# -*- coding: utf-8 -*-
from Types import DataType


class CalcExcellentStudents:
    """Подсчет студентов-отличников: баллы по всем предметам >= 90."""

    MIN_SCORE: int = 90

    def __init__(self, data: DataType) -> None:
        self.data: DataType = data

    @classmethod
    def is_excellent(cls, subjects: list[tuple[str, int]]) -> bool:
        # Студент без оценок отличником не считается
        return len(subjects) > 0 and \
            all(score >= cls.MIN_SCORE for _, score in subjects)

    def get_excellent_students(self) -> list[str]:
        return [name for name, subjects in self.data.items()
                if self.is_excellent(subjects)]

    def calc(self) -> int:
        return len(self.get_excellent_students())
