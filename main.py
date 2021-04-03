import csv
import time
import json


def time_counter(function):
    def wrapper(search=None):
        start_time = time.perf_counter()
        function(search)
        end_time = time.perf_counter()
        print(f"Время выполнения функции {function.__name__} составляет {end_time - start_time}")

    return wrapper


# Линейный поиск O(n)
@time_counter
def open_csv_without_list(searching_value=None):
    # counter = 0
    with open(".\\tmp\\recommends.csv", newline='') as csv_file:
        reader = csv.reader(csv_file)
        # for row in reader:
        #     counter += 1
        #     print(row)
        #     if counter > 10:
        #         break

        if searching_value is not None:
            [print(row) for row in reader if searching_value == row[0]]


# В общем-то такая петрушка, но работа с raw-текстом
@time_counter
def open_csv_like_raw_text(searching_value=None):
    with open(".\\tmp\\recommends.csv", 'r', encoding="utf_8_sig") as csv_file:
        data = csv_file.readlines()
        print(data[0])


# Немного помучил yield
def yield_test(searching_value=None):
    with open(".\\tmp\\recommends.csv", "r", encoding="utf_8_sig") as csv_file:
        # reader = csv.reader(csv_file)
        # yield next(reader)
        for row in csv_file.readline():
            if row[0] == searching_value:
                yield row


# Аналогично
def test_yield_search_time(searching_value=None):
    for row in yield_test(searching_value):
        print(row)


# Сбор всей csv'ки в словарь. Ключём являются товары, а значением - множество строк вида "связанный_товар-rate".
@time_counter
def create_dick_from_csv(whats_search=None):
    test_dict = {}
    with open(".\\tmp\\recommends.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] in test_dict:
                test_dict[row[0]].add(f"{row[1]}_{row[2]}")
            elif row[0] not in test_dict:
                test_dict[row[0]] = {f"{row[1]}_{row[2]}"}
    return test_dict


# Остаток от экспериментов с json (не надо так делать :D). Json создавал с помощью функции create_dick_from_csv.
# Для этого добавляем json.dump, а set меняем на list (меняем скобочки в elif и add -> append)
@time_counter
def search_in_json(whats_search):
    with open(".\\tmp\\test_json.json", "r") as test_json:
        jdata = json.load(test_json)
        print(len(jdata.keys()))


# Обычный подсчёт элементов в csv O(n)
@time_counter
def csv_counter(whats_search=None):
    counter = 0
    with open(".\\tmp\\recommends.csv", "r") as csv_file:
        for row in csv_file:
            counter += 1
    print(counter)


if __name__ == '__main__':
    print("-" * 150)
    csv_counter("1")
    print("-" * 150)
