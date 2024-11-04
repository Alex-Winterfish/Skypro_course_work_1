import json

from src.services import user_search_discription, user_search_phone_number
from src.utils import get_data


def test_search_discription_1(test_search_str_1, test_file_path):
    """Функция проверяет правильность поиска по заданному слову"""
    data_frame = get_data(test_file_path)
    data = user_search_discription(data_frame, test_search_str_1)
    assert len(json.loads(data)) == 350
    assert json.loads(data)[0].get("Описание") == "Перевод Кредитная карта. ТП 10.2 RUR"


def test_search_discription_2(test_search_str_2, test_file_path):
    """Функция проверяет правильность поиска по заданному слову"""
    data_frame = get_data(test_file_path)
    data = user_search_discription(data_frame, test_search_str_2)
    assert len(json.loads(data)) == 152
    assert json.loads(data)[0].get("Описание") == "Пополнение через Газпромбанк"


def test_search_discription_3(test_search_str_3, test_file_path):
    """Функция проверяет правильность поиска если ключевого слова нет"""
    data_frame = get_data(test_file_path)
    data = user_search_discription(data_frame, test_search_str_3)
    assert data == "транзакции не найдены"


def test_search_phome_nomber(test_file_path):
    """Функция проверяет правильность поиска транзакций с номерами телефонов"""
    data_frame = get_data(test_file_path)
    data = user_search_phone_number(data_frame)
    assert len(json.loads(data)) == 25
    assert json.loads(data)[0].get("Описание") == "Тинькофф Мобайл +7 995 555-55-55"
