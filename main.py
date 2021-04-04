import csv
import os
import time

CSV_PATH = ".\\tmp\\recommends.csv"
NEW_CSV_PATH = ".\\tmp\\new_recomends.csv"


def time_counter(function):
    def wrapper(value, value_2):
        start_time: float = time.perf_counter()
        function(value, value_2)
        end_time: float = time.perf_counter()
        print(f"Время выполнения функции {function.__name__} составляет {end_time - start_time}")

    return wrapper


# Сбор всей csv'ки в словарь. Ключом являются товары, а значением - список строк вида "rate-связанный_товар".
# @time_counter
def create_dict_from_csv() -> None:
    large_dict = {}

    with open(CSV_PATH, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] in large_dict:
                large_dict[row[0]].append(f"{row[2]} {row[1]}")
            elif row[0] not in large_dict:
                large_dict[row[0]] = [f"{row[2]} {row[1]}"]

    dict_keys_list: list[str] = list(large_dict.keys())
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
            tmp_list: list[str] = [key]

            for value in large_dict[key]:
                tmp_list.append(value.split()[1])
                tmp_list.append(value.split()[0])

            csv_writer.writerow(tmp_list)


# Обычный подсчёт элементов в csv O(n)
# @time_counter
def csv_counter(file_path) -> None:
    counter = 0
    with open(file_path, "r") as csv_file:
        for row in csv_file:
            counter += 1
    print(counter)


@time_counter
def csv_separator() -> None:
    with open(NEW_CSV_PATH, "r", encoding="utf_8_sig") as csv_file:
        first_line_in_csv = csv_file.readline()

        # TODO: DRY! Вынести всё в отдельную функцию
        new_file_name = first_line_in_csv[0].upper()
        new_file_path = f".\\tmp\\test\\{new_file_name}.csv"

        # TODO: Заменить else на elif
        if os.path.isfile(new_file_path) is False:
            new_csv_file = open(new_file_path, "w", newline='')
        else:
            new_csv_file = open(new_file_path, "a", newline='')

        csv_writer = csv.writer(new_csv_file, delimiter=',')

        write_row = first_line_in_csv.split(",")
        write_row[-1] = write_row[-1][:-1]

        csv_writer.writerow(write_row)

        for csv_row in csv_file.readlines():
            if csv_row[0].upper() != new_file_name:
                if new_csv_file.closed is False:
                    new_csv_file.close()

                new_file_name = csv_row[0].upper()
                new_file_path = f".\\tmp\\test\\{new_file_name}.csv"

                if os.path.isfile(new_file_path) is False:
                    new_csv_file = open(new_file_path, "w", newline='')
                else:
                    new_csv_file = open(new_file_path, "a", newline='')

                csv_writer = csv.writer(new_csv_file, delimiter=',')

            write_row = csv_row.split(",")
            write_row[-1] = write_row[-1][:-1]

            csv_writer.writerow(write_row)

        new_csv_file.close()


@time_counter
def find_some_row(searching_value: str, desired_rank = None):
    if os.path.isfile(f".\\tmp\\test\\{searching_value[0].upper()}.csv") is False:
        print("АХТУНГ!")
        return None

    if desired_rank is not None:
        try:
            desired_rank = float(desired_rank)
        except ValueError:
            desired_rank = None  # Вероятно тутъ нужно намеакть API, что что-то пошло не так

    with open(f".\\tmp\\test\\{searching_value[0].upper()}.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == searching_value:
                for idx in range(2, len(row), 2):
                    if desired_rank is None:
                        print(row[idx - 1::2])
                        break
                    elif desired_rank is not None:
                        try:
                            rank = float(row[idx])
                        except:
                            continue

                        if rank >= desired_rank:
                            print(row[idx - 1::2])
                            break
                print(row)
                break


if __name__ == '__main__':
    print("-" * 150)
    # create_dict_from_csv()
    # csv_counter(NEW_CSV_PATH)
    find_some_row("plEWbqhEVb", 0.71)
    # csv_separator()
    print("-" * 150)
