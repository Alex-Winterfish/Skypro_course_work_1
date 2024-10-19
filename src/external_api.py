import os

import requests
from dotenv import load_dotenv

load_dotenv()


def amount_exchange() -> float:
    """"""
    api = os.getenv("API_EXCHANGE_KEY")
    exchenge_dict = dict()
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD,EUR&base=RUB"

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
    exchenge_dict['USD'] = round(1/result.get('USD'), 2)
    exchenge_dict['EUR'] = round(1 / result.get('EUR'), 2)

    status_code = response.status_code
    return exchenge_dict

    api_result = {'USD': 1.087424, 'EUR': 1}

if __name__ == '__main__':

    print(amount_exchange())
