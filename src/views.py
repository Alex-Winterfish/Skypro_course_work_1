import json

from src.utils import date_split, get_data, get_spending, sort_spending

path_to_data_file = "../data/operations.xlsx"


def user_date():
    """фцнкция для определения даты от пользователя"""
    day = input("Введите дату для выборки \n день: ")
    month = input("месяц: ")
    year = input("  год: ")
    return f"{day}.{month}.{year}"


def user_period():
    """Функция для определения периода выборки"""
    period = input(
        "Введите период для выборки \n"
        " M - месяц \n W - неделя \n Y - год "
        "\n ALL - все данные до пользовательской даты \n Период: "
    )
    return period.upper()


def main(data: json):

    data = json.loads(data)

    accum_value = list()

    for values in data.values():
        accum_value.append(values)

    main_spending = accum_value[0].get("main")

    transfer_and_cash = accum_value[1]

    currency_list = accum_value[3]

    stock_list = accum_value[4]

    print("\nОсновные")
    for spending in main_spending:
        print(spending.get("amount"), end=" ")
        print(spending.get("category"))

    print("\nПереводы и наличные")
    for transfers in transfer_and_cash:
        print(transfers.get("amount"), end=" ")
        print(transfers.get("category"))

    print("\nКурсы валют")
    for user_currency in currency_list:
        print(user_currency.get("currency"), end=" ")
        print(user_currency.get("rate"))

    print("\nСтоимость акций из S&P 500")
    for stock in stock_list:
        print(stock.get("stock"), end=" ")
        print(stock.get("price"))


if __name__ == "__main__":

    data_frame = get_data(path_to_data_file)

    date = user_date()

    period = user_period()

    split_data = date_split(
        data_frame, date, period=period
    )  # получаем дата фрейм по пользовательской дате

    sort_data = get_spending(
        split_data
    )  # формируем словарь с ключ-парой Категория:Сумма операции

    json_answer = sort_spending(sort_data)

    main(json_answer)
