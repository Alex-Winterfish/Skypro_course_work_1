import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def amount_exchange() -> dict:
    """Функция получает курс валют от внешнего API"""

    currency_dict_1 = dict()
    currency_dict_2 = dict()
    with open('../user_settings.json') as f:
        data = json.load(f)

    user_currency = data.get('user_currencies')

    api = os.getenv("API_EXCHANGE_KEY")

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={user_currency[0]},{user_currency[1]}&base=RUB"

    payload = {}
    headers = {
        "apikey": api
    }
    try:
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.ConnectionError:  # обрабатываем ошибку подключенияя
        return "Connection Error. Please check your network connection"
    except requests.exceptions.HTTPError:  # обрабатываем ошибку HTTP запроса
        return "HTTP Error. Please check the URL"
    except (
        requests.exceptions.Timeout
    ):  # обрабатываем ошибку привышения времени подключения
        return "Request timed out. Please check your network connection"

    result = response.json().get('rates')

    currency_dict_1['currency'] = user_currency[0]
    currency_dict_2['currency'] = user_currency[1]
    currency_dict_1['rate'] = round(1 / result.get(user_currency[0]), 2)
    currency_dict_2['rate'] = round(1 / result.get(user_currency[1]), 2)

    exchange_list = [currency_dict_1,currency_dict_2]

    return exchange_list




def stock_value(user_stock:str) -> float:
    """"""
    api = os.getenv("API_MARKET_STOCK")

    stock_dict = dict()

    stock_dict['stock'] = user_stock

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={user_stock}&interval=60min&apikey={api}'

    try:
        response = requests.request(
                "GET", url, timeout=5)
    except requests.exceptions.ConnectionError:  # обрабатываем ошибку подключенияя
        return "Connection Error. Please check your network connection"
    except requests.exceptions.HTTPError:  # обрабатываем ошибку HTTP запроса
        return "HTTP Error. Please check the URL"
    except (requests.exceptions.Timeout):  # обрабатываем ошибку привышения времени подключения
        return "Request timed out. Please check your network connection"

    result = response.json().get("Time Series (60min)")

    for value in result.items():
        stock_dict['price'] = value[1].get('4. close')

    return stock_dict


def get_user_stock():
    with open('../user_settings.json') as f:
        data = json.load(f)

    user_stock = data.get('user_stocks')

    return user_stock





    stocks = get_user_stock()

    stock_list = list()
    stock_prices = dict()

    for stock in stocks:
        stock_data = stock_value(stock)
        stock_list.append(stock_data)

    stock_prices['stock_prices'] = stock_list


    print(stock_prices)
if __name__ == '__main__':

    print(amount_exchange())
