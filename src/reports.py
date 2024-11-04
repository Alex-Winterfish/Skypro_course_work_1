import json
import logging
import re
from datetime import datetime
from typing import Optional

import pandas as pd

logger = logging.getLogger("utils")
handler = logging.FileHandler("../logs/reports.log", "w")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log(filename: str):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            # обработка исключений
            try:
                result = func(*args, *kwargs)
                with open(f"{filename}", "a") as file:
                    file.write(
                        f"\nФункция {func.__name__}: результат выполнения:{result}"
                    )
                print(f"Функция {func.__name__}: результат выполнения:{result}")
                # условие для вывода в консоль
            except Exception as e:
                # условие для записи ошибки в файл
                if filename != None:

                    with open(f"{filename}", "a") as file:
                        file.write(
                            f"\nФункция {func.__name__}: ошибка:{e}, входные данные {*args, *kwargs}"
                        )
                    print(
                        f"Функция {func.__name__}: ошибка: {e}, входные данные {*args, *kwargs}"
                    )
                # условие для вывода ошибки в консоль
                else:
                    print(
                        f"Функция {func.__name__}: ошибка: {e}, входные данные {*args, *kwargs}"
                    )

        return wrapper

    return my_decorator


def log_simple(func):
    def wrapper(*args, **kwargs):
        # обработка исключений
        try:
            result = func(*args, *kwargs)
            # условие для записи в файл
            with open("../logs/simple_log.log", "a") as file:
                file.write(f"\nФункция {func.__name__}: результат выполнения:{result}")
                print("Функция {func.__name__}: результат выполнения:{result}")
            # условие для вывода в консоль
        except Exception as e:
            # условие для записи ошибки в файл

            with open("../logs/simple_log.log", "a") as file:
                file.write(
                    f"\nФункция {func.__name__}: ошибка: {e}, входные данные {*args, *kwargs}"
                )
                print(
                    f"Функция {func.__name__}: ошибка: {e}, входные данные {*args, *kwargs}"
                )

    return wrapper


def spending_by_category(
    data_frame: pd.DataFrame, search_str: str, date: Optional[str] = None
) -> json:

    if date is not None:
        logger.info(f"Передана дата от пользователя: {date}")
        date_proc = datetime.strptime(date, "%d.%m.%Y")

    else:
        logger.info(
            f"Дата от пользователя не передана. Для отчета взята текущая дата {datetime.today().strftime('%d.%m.%Y')}"
        )
        date_proc = datetime.today()

    if date_proc.month - 3 > 0:
        period_month = date_proc.month - 3
        period_year = date_proc.year
    else:
        period_month = 9 + date_proc.month
        period_year = date_proc.year - 1

    i = 0
    while (
        datetime.strptime(data_frame.loc[:, "Дата операции"][i][0:10], "%d.%m.%Y")
        > date_proc
    ):
        i += 1
    j = 0
    while datetime.strptime(
        data_frame.loc[:, "Дата операции"][j][0:10], "%d.%m.%Y"
    ) >= datetime(period_year, period_month, date_proc.day):
        j += 1
    logger.info(
        f"Произведена выборка в период с {date_proc.day}.{period_month}.{period_year} "
        f"по {date_proc.strftime('%d.%m.%Y')}"
    )
    data_by_category = data_frame.iloc[i:j]

    data_dict = data_by_category.to_dict("index")

    output_list = list()
    logger.info(f"Производим поиск по вводу от пользователя: {search_str}")
    for k in range(i, j):  # цикл для поиска транзакций
        if type(data_dict.get(k).get("Категория")) == str:
            search_pattern = re.search(
                f"{search_str}", data_dict.get(k).get("Категория"), flags=re.I
            )
            if search_pattern is not None:
                output_list.append(data_dict.get(k))
            else:
                continue
            if output_list == []:
                logger.exception(f"Транзакции по запросу {search_str} не найдены")
                return "транзакции не найдены"

    logger.info(f"Выводим json ответ по запросу {search_str}")
    json_data = json.dumps(output_list, ensure_ascii=False)
    logger.info(f"Вывод функции {json_data}")

    return json_data
