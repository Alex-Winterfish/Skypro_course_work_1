import json

import pandas as pd
from datetime import datetime

from src.external_api import amount_exchange, stock_value, get_user_stock

file_path = '../data/operations.xlsx'
def get_data(filepath: str)->pd.DataFrame:
    """Функция принимает путь к файлу xls и возвращает список словарей с транзакциями"""

    try:
        transaction_data_xls = pd.read_excel(filepath).to_dict(
            "index"
        )  # читаем файл excel и переводим в словарь
        output_list = list()
        for (
            values
        ) in (
            transaction_data_xls.values()
        ):  # цикл для добавления словарй с транзакциями в список
            output_list.append(values)

        dataframe = pd.DataFrame(output_list)

        return dataframe
    except FileNotFoundError:
        return f"Файл по адресу {filepath} не найден"




def date_split(data_frame, user_date, period='M'):
    '''Функция принимает дату от пользоватеял и необязательный аргумент - диапазон по дате
    Возвращает дата фрейм с транзакциями в заданном временном диапазоне'''
    user_date = datetime.strptime(user_date, '%d.%m.%Y')
    if period=='M': #устанавливаем период за месяц даты пользователя
        period_date = datetime(user_date.year,user_date.month,1)
    elif period == 'W': #устанавливаем период за неделю даты пользователя
        day_period = 7 - user_date.weekday()
        period_date = datetime(user_date.year,user_date.month,day_period)
    elif period == 'Y':  #устанаваливаем предел за год даты пользователя
        period_date = datetime(user_date.year,1,1)
    elif period == 'ALL': # все транзакции до даты пользователя
        period_date = datetime.strptime(data_frame.loc[:,'Дата операции'][len(data_frame)-3][0:10], '%d.%m.%Y')

    i=0
    while datetime.strptime(data_frame.loc[:,'Дата операции'][i][0:10], '%d.%m.%Y') > user_date:
        i+=1
    j=0
    while  datetime.strptime(data_frame.loc[:,'Дата операции'][j][0:10], '%d.%m.%Y') >= period_date:
        j+=1
    return data_frame.iloc[i:j]






def get_spending(data_frame)->list:
    """Функция принимает датафрейм с транзакциями и возврвщает словарь с
     парами ключ-значене - Категория:Сумма орперации"""
    data_frame = data_frame.loc[:, ['Категория','Сумма операции']] #в переменную data_frame вносим датафрем с двумя столбцами
    data_frame_list = data_frame.to_dict('tight', index=False)['data'] # создаем список с категориями и суммами платежей
    list_values = list()
    for i in range(len(data_frame_list)): # цикл для записи списка с категориями трат
        if data_frame_list[i][0] not in list_values: # в этом цикле отсекаем повторяющиеся категории
            list_values.append(data_frame_list[i][0])
    category_list = list_values  # переменная для записи категорий транзакций без повторений
    return_df = dict()
    summ = 0 # переменная для накопления сумм транзакций

    for j in range(len(category_list)): # цикл для перебора существующих транзакций
        for i in range(len(data_frame_list)): # в этом цикле мы перебираем элементы для нахождения
            # совпадения по категориям в итерации j
            if data_frame_list[i][0] == category_list[j]: # проверяем категории в датафрейме на совпадение с
                # категорией в итерации j
                summ += data_frame_list[i][1] # накапливаем сумму
            else:
                continue
        return_df[category_list[j]] = summ

    return return_df




def sort_spending(data:dict):
    "Принимает словарь с парми Категория:Сумма платежа, возвращает json, где траты разбиты по категориям"
    output_data = dict

    processed_data = sorted(data.items(), key=lambda value: value[1], reverse=False)

    expenses_summ = sum(processed_data[i][1] for i in range(len(processed_data)) if processed_data[i][1]<0)*-1

    expenses_list = [processed_data[i] for i in range(len(processed_data)) if processed_data[i][1]<0] #определяем список с расходами

    if len(expenses_list) > 7: #проверяем длину списка расходов

        smaller_amount = sum(expenses_list[i][1] for i in range(7,len(expenses_list)))*-1
        main_expenses = [{'category':expenses_list[i][0],'amount':round(expenses_list[i][1]*-1)} for i in range(7)] + [{'category':'Остальное', 'amount':round(smaller_amount)}]

    else:
        main_expenses = [{'category': expenses_list[i][0], 'amount': round(expenses_list[i][1] * -1)} for i in
                         range(len(expenses_list))] + [{'category': 'Остальное', 'amount': 0}]

    answer_dict = dict()
    expenses = dict()
    income = dict()
    cash = dict()
    transfers = dict()


    expenses['total_amount'] = round(expenses_summ)
    expenses['main'] = main_expenses

    income_summ = sum(processed_data[i][1] for i in range(len(processed_data)) if processed_data[i][1]>0)

    main_income = [{'category':processed_data[i][0],'amount':round(processed_data[i][1])} for i in range(len(processed_data)) if processed_data[i][1]>0]
    main_income = main_income[::-1]

    income['total_amount'] = income_summ
    income['main'] = main_income

    cash['category'] = 'Наличные'
    cash['amount'] = round(data.get('Наличные', 0))

    transfers['category'] = 'Переводы'
    transfers['amount'] = round(data.get('Переводы', 0))


    answer_dict['expenses'] = expenses
    answer_dict['transfers_and_cash'] = [cash, transfers]
    answer_dict['income'] = income
    currency_rate = amount_exchange()
    answer_dict['currency_rate'] = currency_rate

    stocks = get_user_stock()

    stock_list = list()

    for stock in stocks:
        stock_data = stock_value(stock)
        stock_list.append(stock_data)

    answer_dict['stock_prices'] = stock_list

    json_answer = json.dumps(answer_dict, ensure_ascii=False)


    return json_answer




if __name__ == "__main__":
    dataframe = get_data(file_path)
    data_sort_by = date_split(dataframe, '20.03.2018',period='ALL')
    pro_data = get_spending(data_sort_by)

    pro_data1 = sort_spending(pro_data)

    print(pro_data1)

