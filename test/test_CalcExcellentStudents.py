# -*- coding: utf-8 -*-
import pytest
from src.Types import DataType
from src.CalcExcellentStudents import CalcExcellentStudents


class TestCalcExcellentStudents:

    @pytest.fixture()
    def input_data(self) -> tuple[DataType, list[str]]:
        data: DataType = {
            "Абрамов Петр Сергеевич": [
                ("математика", 90), ("физика", 100)
            ],
            "Петров Игорь Владимирович": [
                ("математика", 61), ("литература", 97)
            ],
            "Сидорова Анна Сергеевна": [
                ("математика", 95), ("химия", 91), ("история", 99)
            ],
            "Козлов Дмитрий Андреевич": [
                ("математика", 89), ("химия", 100)
            ],
        }
        excellent = ["Абрамов Петр Сергеевич", "Сидорова Анна Сергеевна"]
        return data, excellent

    def test_init(self, input_data: tuple[DataType, list[str]]) -> None:
        assert CalcExcellentStudents(input_data[0]).data == input_data[0]

    def test_calc(self, input_data: tuple[DataType, list[str]]) -> None:
        assert CalcExcellentStudents(input_data[0]).calc() == 2

    def test_get_excellent_students(
            self, input_data: tuple[DataType, list[str]]) -> None:
        result = CalcExcellentStudents(input_data[0]).get_excellent_students()
        assert result == input_data[1]

    def test_empty_data(self) -> None:
        assert CalcExcellentStudents({}).calc() == 0

    def test_no_excellent_students(self) -> None:
        data: DataType = {"Иванов Иван": [("химия", 89), ("физика", 30)]}
        assert CalcExcellentStudents(data).calc() == 0

    def test_student_without_subjects_is_not_excellent(self) -> None:
        assert CalcExcellentStudents({"Иванов Иван": []}).calc() == 0

    @pytest.mark.parametrize("scores, expected", [
        ([90], True),
        ([89], False),
        ([100, 90, 95], True),
        ([100, 89, 95], False),
        ([0], False),
    ])
    def test_is_excellent_boundaries(self, scores: list[int],
                                     expected: bool) -> None:
        subjects = [(f"предмет {i}", s) for i, s in enumerate(scores)]
        assert CalcExcellentStudents.is_excellent(subjects) is expected
