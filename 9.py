
# Задание task_03_04_09.
#
# Выполнил: Фамилия И.О.
# Группа: !!!



import json


class NoSuchFieldError(Exception):
    def __init__(self, message):
        super().__init__(message)


class IllegalArgumentError(ValueError):
    pass


def load_players(filename):
    """Загрузить данные о хоккеистах из json-файла 'filename'.

    Параметры:
        - filename (str): имя файла.

    Результат:
        - list of dict.

    Для каждого хоккеиста в результат необходимо добавить ключи:
        - "год_рождения", содержащий год из поля "дата_рождения";
        - "ИМТ", содержащий значение индекса массы тела
                (I = масса_в_кг / рост_в_м ** 2);
        - "ИМТ_категория", содержащий значение на основании ключа "ИМТ":
            "Выраженный дефицит массы тела" - 16 и менее;
            "Недостаточная масса тела" - 16—18,5;
            "Норма" - 18,5—24,99;
            "Избыточная масса тела" - 25—30;
            "Ожирение первой степени" - 30—35;
            "Ожирение второй степени" - 35—40;
            "Ожирение третьей степени" - 40 и более.

    Пример одного игрока с добавленными ключами:
       {
          "год":2016,
          "страна":"RUS",
          "номер":22,
          "фамилия":"Зайцев",
          "имя":"Никита",
          "амплуа":"Защитник",
          "рука":"Правая",
          "дата_рождения":"1991-10-29",
          "клуб":"ЦСКА",
          "возраст":24.5065023956194,
          "рост":189,
          "вес":89,
          "год_рождения": 1991,
          "ИМТ": 24.915315920606925,
          "ИМТ_категория": "Норма"
       }

    Функция не обрабатывает исключения."""
    # 1. Загрузить файл
    with open(filename, 'r', encoding = 'utf-8') as f:
        players = json.load(f)

    # 2. Добавить ключи
    for player in players:
        brth = player.get('дата_рождения')
        if brth and len(brth) >= 4:
            player['год_рождения'] = int(brth[:4])
        else:
            player['год_рождения'] = None

        h = player.get('рост')
        w = player.get('вес')
        if h and w and h > 0 and w > 0:
            h_m = h / 100.0
            imt = w / (h_m ** 2)
            player['ИМТ'] = round(imt, 2)
            if imt <= 16:
                cat = "Выраженный дефицит массы тела"
            elif imt < 18.5:
                cat = "Недостаточная масса тела"
            elif imt < 25:
                cat = "Норма"
            elif imt < 30:
                cat = "Избыточная масса тела"
            elif imt < 35:
                cat = "Ожирение первой степени"
            elif imt < 40:
                cat = "Ожирение второй степени"
            else:
                cat = "Ожирение третьей степени"
            player["ИМТ_категория"] = cat
        else:
            player["ИМТ"] = None
            player["ИМТ_категория"] = None

    return players


def group_by(players, field):
    """Вернуть данные, сгруппированные по полю 'field' (по значению).

    Параметры:
        - players (list of dict): структура данных формата 'load_players()';
        - field (string): поле для группировки
                         ("имя", "амплуа", "рука", "год_рождения",
                          "клуб", "клуб_страна", "ИМТ_категория").

    Результат:
        - dict. Формат (на примере поля "амплуа"):
                {"Защитник": 2, "Нападающий": 3, "Вратарь": 1}

    Исключения:
        - если поле 'field' отсутствует в структуре игрока, возбуждается
          исключения NoSuchFieldError с сообщением
          "Нет данных для игрока по полю '...'".
    """
    res = {}

    for player in players:
        value = player.get(field)
        if value is None:
            continue
        res[value] = res.get(value, 0) + 1
    if not res:
        raise NoSuchFieldError(f"Нет данных для игрока по полю '{field}'")

    return res


def save_group_data(filename, group_data, headers):
    """Сохранить данные 'group_data' в csv-файл 'filename'
    с заголовками 'headers'.

    Параметры:
        - filename (str): имя файла;
        - group_data (dict): структура данных формата 'group_by()';
        - headers (list): заголовки в csv-файле (2 значения).

    'group_data' должен быть записан в файл по убыванию значений, но по
    возрастанию ключей при их равенстве:

    Имя,Количество
    Иван,5
    Борис,3
    Михаил,3
    Кирилл,2
    ...

    Исключения:
        - IllegalArgumentError: 'headers' не список или
                                не содержит ровно 2 элемента.
    """
    if not isinstance(headers, list) or len(headers) != 2:
        raise IllegalArgumentError("headers должен быть списком из 2 элементов")

    items = list(group_data.items())
    items.sort(key=lambda x: (-x[1], x[0]))

    with open(filename, 'w', encoding='utf-8', newline='') as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(headers)
        for key, count in items:
            writer.writerow([key, count])


if __name__ == "__main__":
    try:
        filename = "p.json"   # или input()
        save_filename = "output.csv"

        # filename = input("Введите имя файла: ")
        filename = "p.json"

        # save_filename = input("Введите имя файла: ")
        save_filename = "output.csv"

        players = load_players(filename)
        # print(players)

        group_data = group_by(players, field="имя")
        # group_data = group_by(players, field="амплуа")
        # group_data = group_by(players, field="рука")
        # group_data = group_by(players, field="год_рождения")
        # group_data = group_by(players, field="клуб")
        # group_data = group_by(players, field="ИМТ_категория")

        save_group_data(save_filename, group_data, headers=["Имя", "Количество"])
        # save_group_data(save_filename, group_data, headers=["амплуа", "Количество"])
        # save_group_data(save_filename, group_data, headers=["рука", "Количество"])
        # save_group_data(save_filename, group_data, headers=["год_рождения", "Количество"])
        # save_group_data(save_filename, group_data, headers=["клуб", "Количество"])
        # save_group_data(save_filename, group_data, headers=["ИМТ_категория", "Количество"])

        print("Группировка успешно сохранена в", save_filename)
    except FileNotFoundError as e:
        print("Файл не найден:", e)
    except json.JSONDecodeError as e:
        print("Ошибка в JSON-файле:", e)
    except (NoSuchFieldError, IllegalArgumentError) as e:
        print("Ошибка:", e)
    except Exception as e:
        print("Непредвиденная ошибка:", e)