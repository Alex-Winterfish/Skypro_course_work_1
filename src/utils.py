import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests

file_path = "../data/operations.xlsx"

logger = logging.getLogger("utils")
handler = logging.FileHandler("../logs/utils.log", "w")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def amount_exchange() -> list:
    """Функция получает курс валют от внешнего API"""

    currency_dict_1 = dict()
    currency_dict_2 = dict()
    logger.info(
        f"Функция {amount_exchange.__name__} открывает файл с пользовательскими насторойками"
    )
    with open("../user_settings.json") as f:
        data = json.load(f)

    user_currency = data.get("user_currencies")

    api = os.getenv("API_EXCHANGE_KEY")

    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={user_currency[0]},{user_currency[1]}&base=RUB"

    payload = {}
    headers = {"apikey": api}
    try:
        logger.info(
            f"Функция {amount_exchange.__name__} производит запрос к внешенему API для получения курса валют"
        )
        response = requests.request(
            "GET", url, headers=headers, data=payload, timeout=5
        )
    except requests.exceptions.ConnectionError:  # обрабатываем ошибку подключенияя
        logger.error("Данные не получены, проверьте интернет соединение")
        return "Connection Error. Please check your network connection"
    except requests.exceptions.HTTPError:  # обрабатываем ошибку HTTP запроса
        logger.error("HTTP Error. Проверьте адрес страницы")
        return "HTTP Error. Please check the URL"
    except (
        requests.exceptions.Timeout
    ):  # обрабатываем ошибку превышения времени подключения
        logger.error("Превышения времени соединения")
        return "Request timed out. Please check your network connection"
    logger.info(f"{amount_exchange.__name__} получила данные от внешнего API")
    result = response.json().get("rates")

    currency_dict_1["currency"] = user_currency[0]
    currency_dict_2["currency"] = user_currency[1]
    currency_dict_1["rate"] = round(1 / result.get(user_currency[0]), 2)
    currency_dict_2["rate"] = round(1 / result.get(user_currency[1]), 2)

    exchange_list = [currency_dict_1, currency_dict_2]

    logger.info(f"{amount_exchange.__name__} возвращает\n {exchange_list}\n")
    return exchange_list


def stock_value(user_stock: str) -> float:
    """Функция запрашивает от внешнего API данные по акциям из пользовательских настоек"""
    api = os.getenv("API_MARKET_STOCK")

    stock_dict = dict()

    stock_dict["stock"] = user_stock

    url = (f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol"
           f"={user_stock}&interval=60min&apikey={api}")

    try:
        logger.info(
            f"Функция {stock_value.__name__} производит запрос к внешнему API "
            f"для получения данных о стоимости акции {user_stock}"
        )
        response = requests.request("GET", url, timeout=5)
    except requests.exceptions.ConnectionError:  # обрабатываем ошибку подключения
        logger.error("Данные не получены, проверьте интернет соединение")
        return "Connection Error. Please check your network connection"
    except requests.exceptions.HTTPError:  # обрабатываем ошибку HTTP запроса
        logger.error("HTTP Error. Проверьте адрес страницы")
        return "HTTP Error. Please check the URL"
    except (
        requests.exceptions.Timeout
    ):  # обрабатываем ошибку привышения времени подключения
        logger.error("Превышения времени соединения")
        return "Request timed out. Please check your network connection"

    result = response.json().get("Time Series (60min)")

    for value in result.items():
        stock_dict["price"] = value[1].get("4. close")
    logger.info(f"{stock_value.__name__} возвращает \n {stock_dict}\n")
    return stock_dict


def get_user_stock():
    """Функция перебирает акции из настроек пользователя, для их передаче в функцию stock_value()"""
    logger.info(
        f"{get_user_stock.__name__} открывает файл с пользовательскими настройками"
    )
    with open("../user_settings.json") as f:
        data = json.load(f)

    user_stock = data.get("user_stocks")
    logger.info(f"{get_user_stock.__name__} возвращает \n {user_stock}\n")
    return user_stock


def get_data(filepath: str) -> pd.DataFrame:
    """Функция принимает путь к файлу xls и возвращает Data Frame с транзакциями"""

    try:
        logger.info(
            f"{get_data.__name__} переводит данные из {filepath} в список словарей"
        )
        transaction_data_xls = pd.read_excel(filepath).to_dict(
            "index"
        )  # читаем файл excel и переводим в словарь
        output_list = list()  # список для накопления транзакций
        for (
            values
        ) in (
            transaction_data_xls.values()
        ):  # цикл для добавления словарй с транзакциями в список
            output_list.append(values)
        logger.info(f"{get_data.__name__} переводит список транзакций в DataFrame")
        dataframe = pd.DataFrame(output_list)
        logger.info(f"{get_data.__name__} возвращает\n {dataframe}\n")
        return dataframe
    except FileNotFoundError:
        logger.error(f"файл по адресу {filepath} не найден\n")
        return f"Файл по адресу {filepath} не найден"


def date_split(data_frame, user_date, period="M"):
    """Функция принимает дату от пользователя и необязательный аргумент - диапазон по дате
    Возвращает дата фрейм с транзакциями в заданном временном диапазоне"""
    logger.info(f"Функция {date_split.__name__} начинает выполнение")
    user_date = datetime.strptime(user_date, "%d.%m.%Y")
    if period == "M":  # устанавливаем период за месяц даты пользователя
        logger.info("Период для получения транзакций - месяц")
        period_date = datetime(user_date.year, user_date.month, 1)
    elif period == "W":  # устанавливаем период за неделю даты пользователя
        logger.info("Период для получения транзакций - неделя")
        day_period = 7 - user_date.weekday()
        period_date = datetime(user_date.year, user_date.month, day_period)
    elif period == "Y":  # устанаваливаем предел за год даты пользователя
        logger.info("Период для получения транзакций - год")
        period_date = datetime(user_date.year, 1, 1)
    elif period == "ALL":  # все транзакции до даты пользователя
        logger.info("Выводятся все транзакции до дата пользователя")
        period_date = datetime.strptime(
            data_frame.loc[:, "Дата операции"][len(data_frame) - 3][0:10], "%d.%m.%Y"
        )

    i = 0
    while (
        datetime.strptime(data_frame.loc[:, "Дата операции"][i][0:10], "%d.%m.%Y")
        > user_date
    ):
        i += 1
    j = 0
    while (
        datetime.strptime(data_frame.loc[:, "Дата операции"][j][0:10], "%d.%m.%Y")
        >= period_date
    ):
        j += 1
    logger.info(f"{date_split.__name__} возвращает\n {data_frame.loc[i:j]}\n")
    return data_frame.iloc[i:j]


def get_spending(data_frame) -> list:
    """Функция принимает датафрейм с транзакциями и возврвщает словарь с
    парами ключ-значене - Категория:Сумма орперации"""
    logger.info(
        f"{get_spending.__name__} формирует DataFrame с данными по Категориям и Суммам операций"
    )
    data_frame = data_frame.loc[
        :, ["Категория", "Сумма операции"]
    ]  # в переменную data_frame вносим датафрем с двумя столбцами
    data_frame_list = data_frame.to_dict("tight", index=False)[
        "data"
    ]  # создаем список с категориями и суммами платежей
    list_values = list()
    logger.info(
        f"{get_spending.__name__} формирует список с существующими в DataFrame операциях"
    )
    for i in range(len(data_frame_list)):  # цикл для записи списка с категориями трат
        if (
            data_frame_list[i][0] not in list_values
        ):  # в этом цикле отсекаем повторяющиеся категории
            list_values.append(data_frame_list[i][0])
    category_list = (
        list_values  # переменная для записи категорий транзакций без повторений
    )
    return_df = dict()
    summ = 0  # переменная для накопления сумм транзакций

    logger.info(f"{get_spending.__name__} выполняет сложение сумм операций в кетегории")

    for j in range(len(category_list)):  # цикл для перебора существующих транзакций
        for i in range(
            len(data_frame_list)
        ):  # в этом цикле мы перебираем элементы для нахождения
            # совпадения по категориям в итерации j
            if (
                data_frame_list[i][0] == category_list[j]
            ):  # проверяем категории в датафрейме на совпадение с
                # категорией в итерации j
                summ += data_frame_list[i][1]  # накапливаем сумму
            else:
                continue
        return_df[category_list[j]] = summ
    logger.info(
        f"{get_spending.__name__} выводит суммы операций по категориям \n{return_df}\n"
    )
    return return_df


def sort_spending(data: dict):
    "Принимает словарь с парми Категория:Сумма платежа, возвращает json, где траты разбиты по категориям"
    logger.info(
        f"{sort_spending.__name__} сортирует входной словарь по суммам операций по возрастанию"
    )
    processed_data = sorted(data.items(), key=lambda value: value[1], reverse=False)

    logger.info(f"{sort_spending.__name__} формирует общую сумму расходов")
    expenses_summ = (
        sum(
            processed_data[i][1]
            for i in range(len(processed_data))
            if processed_data[i][1] < 0
        )
        * -1
    )

    logger.info(f"{sort_spending.__name__} формирует список с расходами")
    expenses_list = [
        processed_data[i]
        for i in range(len(processed_data))
        if processed_data[i][1] < 0
    ]  # определяем список с расходами

    logger.info(f"{sort_spending.__name__} формирует список с основными расходами")
    if len(expenses_list) > 7:  # проверяем длину списка расходов

        smaller_amount = (
            sum(expenses_list[i][1] for i in range(7, len(expenses_list))) * -1
        )
        main_expenses = [
            {"category": expenses_list[i][0], "amount": round(expenses_list[i][1] * -1)}
            for i in range(7)
        ] + [{"category": "Остальное", "amount": round(smaller_amount)}]

    else:
        main_expenses = [
            {"category": expenses_list[i][0], "amount": round(expenses_list[i][1] * -1)}
            for i in range(len(expenses_list))
        ] + [{"category": "Остальное", "amount": 0}]

    answer_dict = dict()  # словарь для накопления результата работы функции
    expenses = dict()  # словарь для накопления расходов
    income = dict()  # словарь для накопления поступлений
    cash = dict()  # словарь для накопления суммы наличный
    transfers = dict()  # словарь для накопления суммы переводов

    logger.info("sort_spending формирует общую сумму расходов")
    expenses["total_amount"] = round(expenses_summ)
    expenses["main"] = main_expenses

    income_summ = sum(
        processed_data[i][1]
        for i in range(len(processed_data))
        if processed_data[i][1] > 0
    )

    logger.info(f"{sort_spending.__name__} формирует словарь с основными поступлениями")
    main_income = [
        {"category": processed_data[i][0], "amount": round(processed_data[i][1])}
        for i in range(len(processed_data))
        if processed_data[i][1] > 0
    ]
    main_income = main_income[::-1]

    income["total_amount"] = income_summ
    income["main"] = main_income

    logger.info(f"{sort_spending.__name__} формирует словарь с суммой наличный")
    cash["category"] = "Наличные"
    cash["amount"] = round(data.get("Наличные", 0))

    logger.info(f"{sort_spending.__name__} формирует словарь с суммой переводов")
    transfers["category"] = "Переводы"
    transfers["amount"] = round(data.get("Переводы", 0))

    logger.info(
        f"{sort_spending.__name__} формирует словарь c транзакциями пользователя"
    )
    answer_dict["expenses"] = expenses
    answer_dict["transfers_and_cash"] = [cash, transfers]
    answer_dict["income"] = income
    currency_rate = amount_exchange()
    answer_dict["currency_rate"] = currency_rate
    logger.info(f"Функция get_user_stock получает акции из настроек пользователя")
    stocks = get_user_stock()

    stock_list = list()  # список для накопления акций из настоек пользователя

    logger.info(f"{sort_spending.__name__} получает стоимость акций")
    for stock in stocks:
        stock_data = stock_value(stock)
        stock_list.append(stock_data)

    logger.info(
        f"{sort_spending.__name__} добавляет словарь со стоимостями акций в общий словарь"
    )
    answer_dict["stock_prices"] = stock_list

    json_answer = json.dumps(answer_dict, ensure_ascii=False)

    logger.info(f"{sort_spending.__name__} возвращает {json_answer}")
    return json_answer


if __name__ == "__main__":
    dataframe = get_data(file_path)
    data_sort_by = date_split(dataframe, "20.03.2018", period="ALL")
    pro_data = get_spending(data_sort_by)

    pro_data1 = sort_spending(pro_data)

    print(pro_data1)
