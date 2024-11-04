import pytest


@pytest.fixture
def test_user_stock():
    """фикстура для тестирования получения цены акций"""
    return "IBM"


@pytest.fixture
def test_file_path():
    """Фикстура пути к файлу"""
    return "../data/operations.xlsx"


@pytest.fixture
def test_broke_file_path():
    """Фикстура передает несуществующий путь к файлу"""
    return "..daa/operations.xlsx"


@pytest.fixture
def user_date():
    """Фикстура передает дату"""
    return "12.06.2021"


@pytest.fixture
def test_input_user_date():
    return ["20", "06", "2020"]


@pytest.fixture
def json_test():
    return (
        '{"expenses": {"total_amount": 184375, "main": [{"category": "Переводы", '
        '"amount": 31761}, {"category": "Различные товары", "amount": 15013}, '
        '{"category": "Аптеки", "amount": 14974}, {"category": "Рестораны", "amount": '
        '14775}, {"category": "Частные услуги", "amount": 14525}, {"category": "Ж/д '
        'билеты", "amount": 14325}, {"category": "Пополнения", "amount": 13913}, '
        '{"category": "Остальное", "amount": 65089}]}, "transfers_and_cash": '
        '[{"category": "Наличные", "amount": 0}, {"category": "Переводы", "amount": '
        '-31761}], "income": {"total_amount": 0, "main": []}, "currency_rate": '
        '[{"currency": "USD", "rate": 0.01}, {"currency": "EUR", "rate": 0.01}], '
        '"stock_prices": [{"price": "206.2300", "stock": "IBM"}]}'
    )


@pytest.fixture
def test_search_str_1():
    return "Перевод"


@pytest.fixture
def test_search_str_2():
    return "банк"


@pytest.fixture
def test_search_str_3():
    return "kjghjghj"
