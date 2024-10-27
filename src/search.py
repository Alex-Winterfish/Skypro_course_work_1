
from src.data_processing import get_data
file_path = '../data/operations.xlsx'


#search_str = input('Введите слово для поиска: ')


def user_search_discription(data, search_str) -> list:
    """Функция выполняет поиск во входном списке словарей опреаций по заданному слову"""
    output_list = list()  # переменная для накопления найденных транзакций
    import re
    data_dict = data.to_dict('index')
    for i in range(len(data_dict)):  # цикл для поиска транзакций
        search_pattern = re.search(f"{search_str}", data_dict.get(i).get("Описание"), flags=re.I)
        if search_pattern is not None:
            output_list.append(data_dict.get(i))
        else:
            continue
        if output_list == []:
            return "транзакции не найдены"
    else:
        return output_list


def user_search_phone_number(data) -> list:
    """Функция выполняет поиск во входном списке словарей опреаций по заданному слову"""

    import re
    output_list = list()  # переменная для накопления найденных транзакций

    data_dict = data.to_dict('index')
    for i in range(len(data_dict)):  # цикл для поиска транзакций
        search_pattern = re.search(r'\d \d{3,} \d{3,}-\d{2,}-\d{2,}', data_dict.get(i).get("Описание"), flags=re.I)
        if search_pattern is not None:
            output_list.append(data_dict.get(i))
        else:
            continue
    if output_list == []:
        return "транзакции не найдены"
    else:
        return output_list



if __name__ == '__main__':
    data = get_data(file_path)

    f = user_search_phone_number(data)

    print(f)