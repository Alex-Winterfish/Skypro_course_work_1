import pathlib
import pandas as pd
from collections import Counter
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

        return pd.DataFrame(output_list)
    except FileNotFoundError:
        return f"Файл по адресу {filepath} не найден"



def get_spending(data_frame)->list:
    """Функция принимает датафрейм с транзакциями и возврвщает json формат с категорями Основные: сортированны
    по убыванию. Первые 7 указанны, остальные собраны в категорию Остальные"""
    data_frame = data_frame.loc[:, ['Категория','Сумма платежа']] #в переменную data_frame вносим датафрем с двумя столбцами
    data_frame_list = data_frame.to_dict('tight', index=False)['data'] # создаем список с категориями и суммами платежей
    list_values = list()
    for i in range(len(data_frame_list)): # цикл для записи списка с категориями трат
        list_values.append(data_frame_list[i][0])
    category_list = list(set(list_values)) # переменная для записи категорий транзакций без повторений

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


if __name__ == "__main__":
    dataframe = get_data(file_path)

    print(get_spending(dataframe))