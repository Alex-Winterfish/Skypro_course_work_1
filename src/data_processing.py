import pathlib
file_path = pathlib.Path('../data/operations.xlsx')
def excel_processing(filepath: str) -> list:
    """Функция принимает путь к файлу xls и возвращает список словарей с транзакциями"""
    import pandas as pd

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

        return output_list
    except FileNotFoundError:
        return f"Файл по адресу {filepath} не найден"



if __name__ == "__main__":

    print(excel_processing(file_path))