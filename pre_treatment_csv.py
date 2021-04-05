import csv
import os
import sys


def csv_counter(file_path):
    counter = 0
    with open(file_path, "r") as csv_file:
        for _ in csv_file:
            counter += 1
    return counter


class PreTreatmentCSV:
    def __init__(self, initial_csv_file_path, sorted_csv_file_path=".\\tmp\\sorted_csv.csv",
                 separated_csv_dir_path=".\\tmp\\separated_csv\\"):
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


if __name__ == '__main__':
    init_csv_path = ".\\tmp\\recommends.csv"
    sorted_csv_path = ".\\tmp\\new_recommends_1.csv"
    separated_csv_path = ".\\tmp\\separated csv\\"

    PreTreatmentCSV(init_csv_path, sorted_csv_path, separated_csv_path).start_treatment()
