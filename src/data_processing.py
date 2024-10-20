import pathlib
from calendar import month

import pandas as pd
from datetime import datetime, date, time

file_path = '../data/operations.xlsx'
def get_data(filepath: str):
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




def date_split(data_frame, user_date = '09.03.2020', period='M'):
    '''Функция принимает дату от пользоватеял и необязательный аргумент - диапазон по дате'''
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
    "Принимает словарь с парми Категория:Сумма платежа, возврщает вормат json, где траты разбиты по категориям"
    output_data = dict

    processed_data = sorted(data.items(), key=lambda value: value[1], reverse=False)
    TEST_DICT = dict(processed_data)
    expenses_summ = sum(processed_data[i][1] for i in range(len(processed_data)) if processed_data[i][1]<0)*-1

    smaller_amount = sum(processed_data[i][1] for i in range(7,len(processed_data)) if processed_data[i][1]<0)*-1
    #здесь нужно отловить исключение out of range если список трат короче 7
    main_expenses = [{'category':processed_data[i][0],'amount':round(processed_data[i][1]*-1)} for i in range(7)] + [{'category':'Остальное', 'amount':round(smaller_amount)}]

    answer_dict = dict()
    expenses = dict()
    expenses['total_amount'] = round(expenses_summ)
    expenses['main'] = main_expenses

    processed_data = sorted(data.items(), key=lambda value: value[1], reverse=True)

    income_summ = sum(processed_data[i][1] for i in range(len(processed_data)) if processed_data[i][1]>0)

    income = [{'category':processed_data[i][0],'amount':round(processed_data[i][1])} for i in range(len(processed_data)) if processed_data[i][1]>0]
    answer_dict['exepenses'] = expenses
    answer_dict['income'] = income


    return answer_dict


if __name__ == "__main__":
    dataframe = get_data(file_path)
    data_sort_by = date_split(dataframe,period='M')
    pro_data = get_spending(data_sort_by)

    pro_data1 = sort_spending(pro_data)

    print(pro_data1)

