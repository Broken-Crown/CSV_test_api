import csv
import time

CSV_PATH = ".\\tmp\\recommends.csv"


def time_counter(function):
    def wrapper():
        start_time = time.perf_counter()
        function()
        end_time = time.perf_counter()
        print(f"Время выполнения функции {function.__name__} составляет {end_time - start_time}")
    return wrapper


# Сбор всей csv'ки в словарь. Ключом являются товары, а значением - множество строк вида "связанный_товар-rate".
@time_counter
def create_dict_from_csv():
    large_dict = {}
    with open(CSV_PATH, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] in large_dict:
                large_dict[row[0]].append(f"{row[2]}_{row[1]}")
            elif row[0] not in large_dict:
                large_dict[row[0]] = [f"{row[2]}_{row[1]}"]
    dict_keys_list = list(large_dict.keys())
    dict_keys_list.sort()
    for key, value in large_dict.items():
        # large_dict[key] = list(dict.fromkeys(value))  # Это такой интересный способ удалить дубликаты.
        value.sort()
    print(dict_keys_list[0])
    print(large_dict[dict_keys_list[0]])
    print(len(dict_keys_list))


# Обычный подсчёт элементов в csv O(n)
@time_counter
def csv_counter():
    counter = 0
    with open(CSV_PATH, "r") as csv_file:
        for row in csv_file:
            counter += 1
    print(counter)


if __name__ == '__main__':
    print("-" * 150)
    create_dict_from_csv()
    print("-" * 150)
