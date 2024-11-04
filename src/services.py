import json
import logging
import re

from src.utils import get_data

logger = logging.getLogger("utils")
handler = logging.FileHandler("../logs/services.log", "w")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

file_path = "../data/operations.xlsx"

data = get_data(file_path)


def user_search_discription(data, search_str) -> json:
    """Функция выполняет поиск во входном списке словарей опреаций по заданному слову"""
    data_dict = data.to_dict("index")
    output_list = list()  # переменная для накопления найденных транзакций
    logger.info(
        f"Функция {user_search_discription.__name__} производит поиск по запросу {search_str}"
    )
    for i in range(len(data_dict)):  # цикл для поиска транзакций
        search_pattern = re.search(
            f"{search_str}", data_dict.get(i).get("Описание"), flags=re.I
        )
        if search_pattern is not None:
            output_list.append(data_dict.get(i))
        else:
            continue
    if output_list == []:
        logger.error(
            f"{user_search_discription.__name__} не найдены транзакции по запросу {search_str}"
        )
        return "транзакции не найдены"
    else:
        logger.info(f"Функция {user_search_discription.__name__} формирует json ответ")
        json_data = json.dumps(output_list, ensure_ascii=False)
        logger.info(
            f"json ответ функции {user_search_discription.__name__}: {json_data}"
        )

        return json_data


def user_search_phone_number(data) -> json:
    """Функция выполняет поиск во входном списке словарей транзакций с номерами телофонов"""
    import json
    import re

    data_dict = data.to_dict("index")
    output_list = list()  # переменная для накопления найденных транзакций
    logger.info(
        f"{user_search_phone_number.__name__} производит поиск номеров телефонов"
    )
    for i in range(len(data_dict)):  # цикл для поиска транзакций
        search_pattern = re.search(
            r"\d \d{3,} \d{3,}-\d{2,}-\d{2,}",
            data_dict.get(i).get("Описание"),
            flags=re.I,
        )
        if search_pattern is not None:
            output_list.append(data_dict.get(i))
        else:
            continue
    if output_list == []:
        logger.error(
            f"{user_search_phone_number.__name__} не найдены транзакции с номерами телефонов"
        )
        return "транзакции не найдены"
    else:
        json_data = json.dumps(output_list, ensure_ascii=False)
        logger.info(
            f"json ответ функции {user_search_phone_number.__name__}: {json_data}"
        )
        return json_data


if __name__ == "__main__":
    data = get_data(file_path)

    data_dict = data.to_dict("index")

    # search = input('введите поиск:  ')

    f = user_search_phone_number(data_dict)

    def out_red(text):
        print("\033[34m{}".format(text))

    out_red(f)
