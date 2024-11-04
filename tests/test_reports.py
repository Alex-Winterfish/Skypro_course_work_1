import json
from datetime import datetime

from src.reports import log, log_simple, spending_by_category
from src.utils import get_data


def test_spending_by_category(test_file_path, test_search_str_1):
    """Функция проверяет правильность поиска категории в период 3 месяца"""
    data_frame = get_data(test_file_path)
    data = spending_by_category(data_frame, test_search_str_1, "20.06.2020")
    # Дата начало выборки
    date_start = datetime.strptime(
        json.loads(data)[0].get("Дата операции"), "%d.%m.%Y %H:%M:%S"
    )
    # Дата окончания выборки
    date_end = datetime.strptime(
        json.loads(data)[-1].get("Дата операции"), "%d.%m.%Y %H:%M:%S"
    )
    assert date_start.month - date_end.month == 3
    # Создаем список с булевыми значениями для проверки соответствия ключевому слову
    assert all(data.get("Категория") == "Переводы" for data in json.loads(data)) == True


def test_my_division_1(capsys):
    # функция проверяет вывод в консоль при положительных аргументах
    @log("../tests/test.log")
    def my_division(x, y):
        return x / y

    my_division(4, 0)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Функция my_division: ошибка: division by zero, входные данные (4, 0)\n"
    )


def test_my_division_2(capsys):
    # функция проверяет вывод в консоль ошибки при делении на ноль
    @log_simple
    def my_division(x, y):
        return x / y

    my_division(4, 0)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "Функция my_division: ошибка: division by zero, входные данные (4, 0)\n"
    )
