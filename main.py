import csv
import os
import time


def time_counter(function):
    def wrapper(value, value_2):
        start_time = time.perf_counter()
        function(value, value_2)
        end_time = time.perf_counter()
        print(f"Время выполнения функции {function.__name__} составляет {end_time - start_time}")
    return wrapper

# Сбор всей csv'ки в словарь. Ключом являются товары, а значением - список строк вида "rate-связанный_товар".
@time_counter
def create_dict_from_csv(initial_csv_path, output_csv_path):
    large_dict = {}

    if os.path.isfile(initial_csv_path) is False:
        raise FileExistsError("Initial *.csv-file not found")

    with open(initial_csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[0] in large_dict:
                large_dict[row[0]].append(f"{row[2]} {row[1]}")
            elif row[0] not in large_dict:
                large_dict[row[0]] = [f"{row[2]} {row[1]}"]

    dict_keys_list = list(large_dict.keys())
    dict_keys_list.sort()

    if os.path.isfile(output_csv_path) is False:
        f = open(output_csv_path, "w")
        f.close()

    with open(output_csv_path, mode="w", newline='') as new_csv_file:
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


# Обычный подсчёт элементов в csv O(n)
# @time_counter
def csv_counter(file_path) -> None:
    counter = 0
    with open(file_path, "r") as csv_file:
        for row in csv_file:
            counter += 1
    print(counter)


@time_counter
def csv_separator(input_csv_path, output_csv_path) -> None:
    if os.path.isdir(output_csv_path) is False:
        os.mkdir(output_csv_path)

    with open(input_csv_path, "r", encoding="utf_8_sig") as csv_file:
        first_line_in_csv = csv_file.readline()

        # TODO: Да, я тут нарушил DRY потому что мысля пёрла.
        new_file_name = first_line_in_csv[0].upper()
        if "\\" in output_csv_path[-1]:
            output_csv_path = output_csv_path[:-1]
        new_file_path = f"{output_csv_path}\\{new_file_name}.csv"

        # TODO: Заменить else на elif
        if os.path.isfile(new_file_path) is False:
            new_csv_file = open(new_file_path, "w", newline='')
        elif os.path.isfile(new_file_path) is True:
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
                new_file_path = f"{output_csv_path}\\{new_file_name}.csv"

                if os.path.isfile(new_file_path) is False:
                    new_csv_file = open(new_file_path, "w", newline='')
                else:
                    new_csv_file = open(new_file_path, "a", newline='')

                csv_writer = csv.writer(new_csv_file, delimiter=',')

            write_row = csv_row.split(",")
            write_row[-1] = write_row[-1][:-1]

            csv_writer.writerow(write_row)

        new_csv_file.close()


# @time_counter
# Пока что работает через жопу.
def custom_bisect(input_list, value):
    debug_counter = 0
    right_border = len(input_list) - 1
    left_border = 0
    left_to_right_range = right_border - left_border
    middle_of_list = left_to_right_range // 2 + left_border
    while left_to_right_range > 1:
        debug_counter += 1
        print(debug_counter)
        try:
            checking_value = float(input_list[middle_of_list])
        except ValueError:
            middle_of_list += 1
            checking_value = float(input_list[middle_of_list])

        if checking_value < value:
            left_border = middle_of_list
        elif checking_value > value:
            right_border = middle_of_list
        elif checking_value == value:
            return middle_of_list

        left_to_right_range = right_border - left_border
        middle_of_list = left_to_right_range // 2 + left_border
    else:
        if right_border == len(input_list) - 1:
            return right_border
        elif left_border == 0:
            return left_border
        return middle_of_list + 1


# @time_counter
def find_some_row(searching_value, input_folder, desired_rank=None):
    if "\\" in input_folder[-1]:
        input_folder = input_folder[:-1]

    if os.path.isfile(f"{input_folder}\\{searching_value[0].upper()}.csv") is False:
        print("АХТУНГ!")
        return None

    if desired_rank is not None:
        try:
            desired_rank = float(desired_rank)
        except ValueError:
            desired_rank = None  # Вероятно тутъ нужно намеакть API, что что-то пошло не так

    with open(f"{input_folder}\\{searching_value[0].upper()}.csv", newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0] == searching_value:
                if desired_rank is None:
                    print(row[1::2])
                    break

                # Можно и так, но особого профита нет, т.к. приходится вытаскивать ранги
                # test_tuple = tuple([float(value) for value in row[2::2]])
                # c = bisect.bisect_right(test_tuple, desired_rank)
                # print(row[c * 2 + 1::2])

                test_idx = custom_bisect(row, desired_rank)
                print(row[test_idx - 1::2])

                # for idx in range(2, len(row), 2):  # Думаю, что для "безопасности" тут лучше перебрать каждый элемент
                #     try:
                #         rank = float(row[idx])
                #     except ValueError:
                #         continue
                #     if rank >= desired_rank:
                #         print(row[idx - 1::2])
                #         break
                print(row)
                break


if __name__ == '__main__':
    print("-" * 150)

    init_csv_path = ".\\tmp\\recommends.csv"
    sorted_csv_path = ".\\tmp\\new_recommends_1.csv"
    separated_csv_path = f".\\tmp\\separated csv\\"

    create_dict_from_csv(init_csv_path, sorted_csv_path)
    csv_separator(sorted_csv_path, separated_csv_path)
    # csv_counter(NEW_CSV_PATH)
    # find_some_row("plEWbqhEVb", 0.5)
    # csv_separator()
    # a = ["11", "22", "33", "44", "55", "66"]
    # c = custom_bisect(a, 33.001)
    # print(c)
    print("-" * 150)
