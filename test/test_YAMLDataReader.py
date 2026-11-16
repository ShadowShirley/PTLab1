# -*- coding: utf-8 -*-
import pytest
from src.Types import DataType
from src.DataReader import DataReader
from src.YAMLDataReader import YAMLDataReader


class TestYAMLDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = "- Иванов Константин Дмитриевич:\n" + \
               "    математика: 91\n" + \
               "    химия: 100\n" + \
               "- Петров Петр Семенович:\n" + \
               "    русский язык: 87\n" + \
               "    литература: 78\n"
        data = {
            "Иванов Константин Дмитриевич": [
                ("математика", 91), ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }
        return text, data

    @staticmethod
    def write(tmpdir, text: str) -> str:
        p = tmpdir.join("my_data.yaml")
        p.write_text(text, encoding='utf-8')
        return str(p)

    def test_is_data_reader(self) -> None:
        bases = [cls.__name__ for cls in type(YAMLDataReader()).__mro__]
        assert DataReader.__name__ in bases

    def test_read(self, file_and_data_content: tuple[str, DataType],
                  tmpdir) -> None:
        path = self.write(tmpdir, file_and_data_content[0])
        assert YAMLDataReader().read(path) == file_and_data_content[1]

    def test_read_keeps_subject_order(
            self, file_and_data_content: tuple[str, DataType],
            tmpdir) -> None:
        path = self.write(tmpdir, file_and_data_content[0])
        result = YAMLDataReader().read(path)
        subjects = [s for s, _ in result["Иванов Константин Дмитриевич"]]
        assert subjects == ["математика", "химия"]

    def test_read_empty_file(self, tmpdir) -> None:
        path = self.write(tmpdir, "")
        assert YAMLDataReader().read(path) == {}

    def test_read_student_without_subjects(self, tmpdir) -> None:
        path = self.write(tmpdir, "- Иванов Иван Иванович:\n")
        assert YAMLDataReader().read(path) == {"Иванов Иван Иванович": []}

    def test_read_string_scores_are_converted(self, tmpdir) -> None:
        path = self.write(tmpdir, "- Иванов Иван:\n    химия: '85'\n")
        assert YAMLDataReader().read(path) == {"Иванов Иван": [("химия", 85)]}

    def test_root_not_list_raises(self, tmpdir) -> None:
        path = self.write(tmpdir, "Иванов Иван:\n  химия: 85\n")
        with pytest.raises(ValueError):
            YAMLDataReader().read(path)

    def test_student_record_not_dict_raises(self, tmpdir) -> None:
        path = self.write(tmpdir, "- Иванов Иван\n")
        with pytest.raises(ValueError):
            YAMLDataReader().read(path)

    def test_subjects_not_dict_raises(self, tmpdir) -> None:
        path = self.write(tmpdir, "- Иванов Иван:\n    - химия\n")
        with pytest.raises(ValueError):
            YAMLDataReader().read(path)

    def test_non_numeric_score_raises(self, tmpdir) -> None:
        path = self.write(tmpdir, "- Иванов Иван:\n    химия: отлично\n")
        with pytest.raises(ValueError):
            YAMLDataReader().read(path)

    def test_missing_file_raises(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            YAMLDataReader().read(str(tmpdir.join("absent.yaml")))
