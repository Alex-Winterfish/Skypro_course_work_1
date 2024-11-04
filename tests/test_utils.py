from unittest.mock import patch

import pandas as pd

from src.utils import (amount_exchange, date_split, file_path, get_data,
                       get_spending, get_user_stock, sort_spending,
                       stock_value)


@patch("requests.request")
def test_amount_exchange_request(mock_get):
    """Функция проверяет запроса курса валют к внешнему API"""
    import os

    api = os.getenv("API_EXCHANGE_KEY")
    mock_get.return_value.json.return_value = {
        "base": "RUB",
        "date": "2022-04-14",
        "rates": {"USD": 100, "EUR": 100},
        "success": "true",
        "timestamp": 1519296206,
    }
    assert amount_exchange() == [
        {"currency": "USD", "rate": 0.01},
        {"currency": "EUR", "rate": 0.01},
    ]
    mock_get.assert_called_once_with(
        "GET",
        "https://api.apilayer.com/exchangerates_data/latest?symbols=USD,EUR&base=RUB",
        headers={"apikey": api},
        data={},
        timeout=5,
    )


@patch("requests.request")
def test_stock_value(mock_get, test_user_stock):
    """Функция проверяет запроса цены акции к внешнему API"""
    import os

    api = os.getenv("API_MARKET_STOCK")
    mock_get.return_value.json.return_value = {
        "Meta Data": {
            "1. Information": "Intraday (5min) open, high, low, close prices and volume",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-10-31 19:55:00",
            "4. Interval": "5min",
            "5. Output Size": "Compact",
            "6. Time Zone": "US/Eastern",
        },
        "Time Series (60min)": {
            "2024-10-31 19:55:00": {
                "1. open": "206.6999",
                "2. high": "206.7000",
                "3. low": "206.2300",
                "4. close": "206.2300",
                "5. volume": "132",
            }
        },
    }
    assert stock_value(test_user_stock) == {"price": "206.2300", "stock": "IBM"}
    mock_get.assert_called_once_with(
        "GET",
        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
        f"{test_user_stock}&interval=60min&apikey={api}",
        timeout=5,
    )


def test_get_user_stock():
    """Функция проверяет получение акций из настроек пользователя"""
    assert get_user_stock() == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_get_data(test_file_path):
    """Функция проверяет вывод результата в виде дата фрейма соответствующего размера"""
    data = get_data(file_path)
    assert data is not None
    assert type(data) is pd.DataFrame
    assert data.shape == (6705, 15)


def test_get_data_broke_path(test_broke_file_path):
    """Функция проверяет вывод ошибки пути к файлу"""
    data = get_data(test_broke_file_path)
    assert data is not str
    assert type(data) is not pd.DataFrame
    assert data == "Файл по адресу ..daa/operations.xlsx не найден"


def test_date_split_week(user_date):
    """Функция проверяет формирование дата фрейм в период в неделю"""
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "W")
    assert data is not None
    assert type(data) is pd.DataFrame
    assert data.shape == (67, 15)


def test_date_split_month(user_date):
    """Функция проверяет формирование дата фрейм в период в месяц"""
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "M")
    assert data is not None
    assert type(data) is pd.DataFrame
    assert data.shape == (68, 15)


def test_date_split_year(user_date):
    """Функция проверяет формирование дата фрейм в период в год"""
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "Y")
    assert data is not None
    assert type(data) is pd.DataFrame
    assert data.shape == (835, 15)


def test_date_split_all(user_date):
    """Функция проверяет формирование дата фрейм в период в год"""
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "ALL")
    assert data is not None
    assert type(data) is pd.DataFrame
    assert data.shape == (5664, 15)


def test_get_spending(user_date):
    """Функция проверяет сортировку данный по категориям"""
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "M")
    data_s = get_spending(data)
    assert data_s is not None
    assert type(data_s) is dict
    assert data_s == {
        "Аптеки": -14973.519999999999,
        "Бонусы": -8913.419999999998,
        "Ж/д билеты": -14324.519999999999,
        "Одежда и обувь": -9649.919999999998,
        "Переводы": -31761.42,
        "Пополнения": -13913.419999999998,
        "Различные товары": -15013.419999999998,
        "Рестораны": -14774.519999999999,
        "Связь": -9051.189999999999,
        "Супермаркеты": -4018.1899999999996,
        "Транспорт": -10991.919999999998,
        "Турагентства": -13913.419999999998,
        "Фастфуд": -8551.189999999999,
        "Частные услуги": -14524.519999999999,
    }


@patch("src.utils.stock_values")
@patch("src.utils.get_user_stock")
@patch("src.utils.amount_exchange")
def test_sort_spending(mock_exchange, mock_stock, mock_stock_values, user_date):
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "M")
    data_s = get_spending(data)
    mock_exchange.return_value = [
        {"currency": "USD", "rate": 0.01},
        {"currency": "EUR", "rate": 0.01},
    ]
    mock_stock.return_value = ["IBM"]
    mock_stock_values.return_value = {"price": "206.2300", "stock": "IBM"}
    data_sort = sort_spending(data_s)
    assert data_sort is not None
    assert type(data_sort) is str
    assert data_sort == ""


@patch("src.utils.stock_value")
@patch("src.utils.get_user_stock")
@patch("src.utils.amount_exchange")
def test_sort_spending1(
    mock_amount_exchange, mock_get_user_stock, mock_stock_value, user_date
):
    """Функция проверяет формирование итогового отчета"""
    data_f = get_data("../data/operations.xlsx")
    data = date_split(data_f, user_date, "M")
    data_s = get_spending(data)
    mock_amount_exchange.return_value = [
        {"currency": "USD", "rate": 0.01},
        {"currency": "EUR", "rate": 0.01},
    ]
    mock_get_user_stock.return_value = ["IBM"]
    mock_stock_value.return_value = {"price": "206.2300", "stock": "IBM"}
    data_sort = sort_spending(data_s)
    assert data_sort is not None
    assert type(data_sort) is str
    assert data_sort == (
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
