import csv
import os
import sys
import time


def time_counter(function):
    def wrapper(value):
        start_time = time.perf_counter()
        function(value)
        end_time = time.perf_counter()
        print(f"Время выполнения функции {function.__name__} составляет {end_time - start_time}")

    return wrapper


# Обычный подсчёт элементов в csv O(n)
def csv_counter(file_path):
    counter = 0
    with open(file_path, "r") as csv_file:
        for _ in csv_file:
            counter += 1
    print(counter)


class PreTreatmentCSV:
    def __init__(self, initial_csv_file_path, sorted_csv_file_path, separated_csv_dir_path):
        self.initial_csv_file_path = os.path.abspath(initial_csv_file_path)
        self.sorted_csv_file_path = os.path.abspath(sorted_csv_file_path)
        self.separated_csv_dir_path = os.path.abspath(separated_csv_dir_path)
        self.__check_env()

    def start_treatment(self):
        self.__create_dict_from_csv()
        self.__csv_separator()

    def __check_env(self):
        sorted_csv_dir_path = "\\".join(self.sorted_csv_file_path.split("\\")[0:-1])

        if os.path.isfile(self.initial_csv_file_path) is False:
            raise FileExistsError("The initial file does not exist")

        if os.path.isdir(sorted_csv_dir_path) is False:
            os.mkdir(sorted_csv_dir_path)

        if os.path.isdir(self.separated_csv_dir_path) is False:
            os.mkdir(self.separated_csv_dir_path)

    # Сбор всей csv'ки в словарь. Ключом являются товары, а значением - список строк вида "rate-связанный_товар".
    @time_counter
    def __create_dict_from_csv(self):
        csv_large_dict = {}

        with open(self.initial_csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row[0] in csv_large_dict:
                    csv_large_dict[row[0]].append(f"{row[2]} {row[1]}")
                elif row[0] not in csv_large_dict:
                    csv_large_dict[row[0]] = [f"{row[2]} {row[1]}"]

        dict_keys_list = list(csv_large_dict.keys())
        dict_keys_list.sort()

        if os.path.isfile(self.sorted_csv_file_path) is False:
            f = open(self.sorted_csv_file_path, "w")
            f.close()

        with open(self.sorted_csv_file_path, mode="w", newline='') as new_csv_file:
            for key in dict_keys_list:
                csv_large_dict[key] = list(dict.fromkeys(csv_large_dict[key]))
                csv_large_dict[key].sort()

                csv_writer = csv.writer(new_csv_file, delimiter=',')

                # Мне откровенно не нравится идея с временным списком, но другой пока что у меня нет
                tmp_list = [key]

                for value in csv_large_dict[key]:
                    tmp_list.append(value.split()[1])
                    tmp_list.append(value.split()[0])

                csv_writer.writerow(tmp_list)

    @time_counter
    def __csv_separator(self):
        with open(self.sorted_csv_file_path, "r", encoding="utf_8_sig") as csv_file:
            new_file_name = ""
            new_csv_file = ""
            for csv_row in csv_file.readlines():
                if csv_row[0].upper() != new_file_name:
                    if new_csv_file and new_csv_file.closed is False:
                        new_csv_file.close()

                    new_file_name = csv_row[0].upper()
                    new_file_path = f"{self.separated_csv_dir_path}\\{new_file_name}.csv"

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

    PreTreatmentCSV(init_csv_path, sorted_csv_path, separated_csv_path).start_treatment()

    print("-" * 150)
