import csv
import os
import time

CSV_PATH = ".\\tmp\\recommends.csv"
NEW_CSV_PATH = ".\\tmp\\new_recomends.csv"


def time_counter(function):
    def wrapper():
        start_time = time.perf_counter()
        function()
        end_time = time.perf_counter()
        print(f"Время выполнения функции {function.__name__} составляет {end_time - start_time}")
    return wrapper


# Сбор всей csv'ки в словарь. Ключом являются товары, а значением - список строк вида "rate-связанный_товар".
@time_counter
def create_dict_from_csv():
    large_dict = {}

    with open(CSV_PATH, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] in large_dict:
                large_dict[row[0]].append(f"{row[2]} {row[1]}")
            elif row[0] not in large_dict:
                large_dict[row[0]] = [f"{row[2]} {row[1]}"]

    dict_keys_list = list(large_dict.keys())
    dict_keys_list.sort()

    if os.path.isfile(NEW_CSV_PATH) is False:
        f = open(NEW_CSV_PATH, "w")
        f.close()

    with open(NEW_CSV_PATH, mode="w", newline='') as new_csv_file:
        for key in dict_keys_list:
            large_dict[key] = list(dict.fromkeys(large_dict[key]))
            large_dict[key].sort()

            csv_writer = csv.writer(new_csv_file, delimiter=',')

            # Мне откровенно не нравится идея с временным списком, но другой пока что у меня нет
            tmp_list = [key]

            for value in large_dict[key]:
                tmp_list.append(value.split()[1])
                tmp_list.append(value.split()[0])

            csv_writer.writerow(tmp_list)
    print(dict_keys_list[0])
    print(large_dict[dict_keys_list[0]])
    print(len(dict_keys_list))


# Обычный подсчёт элементов в csv O(n)
# @time_counter
def csv_counter(file_path):
    counter = 0
    with open(file_path, "r") as csv_file:
        for row in csv_file:
            counter += 1
    print(counter)


if __name__ == '__main__':
    print("-" * 150)
    # create_dict_from_csv()
    csv_counter(NEW_CSV_PATH)
    print("-" * 150)
