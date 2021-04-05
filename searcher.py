import os
import bisect


# Пока что работает через жопу.
def custom_bisect(input_list, value):
    debug_counter = 0
    right_border = len(input_list) - 1
    left_border = 0
    left_to_right_range = right_border - left_border
    middle_of_list = left_to_right_range // 2 + left_border
    while left_to_right_range > 1:
        # debug_counter += 1
        # print(debug_counter)
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


def find_some_row(searching_value, input_folder, desired_rank=None):
    input_folder = os.path.abspath(input_folder)

    if os.path.isfile(f"{input_folder}\\{searching_value[0].upper()}.csv") is False:
        return ["The necessary file does not exist"]

    if desired_rank is not None:
        try:
            desired_rank = float(desired_rank)
        except ValueError:
            desired_rank = None  # Вероятно тутъ нужно намеакть API, что что-то пошло не так

    with open(f"{input_folder}\\{searching_value[0].upper()}.csv", encoding="utf_8_sig") as csv_file:
        # csv_reader = csv.reader(csv_file)
        for row in csv_file.readlines():
            row = row.split(',')
            if row[0] == searching_value:
                if desired_rank is None:
                    return row[1::2]

                # Можно и так, но особого профита нет, т.к. приходится вытаскивать ранги.
                # test_tuple = tuple([float(value) for value in row[2::2]])
                # c = bisect.bisect_left(test_tuple, desired_rank)
                # return row[c * 2 + 1::2]

                # Попытка реализации собственной бисекции. Пока не оч удачная.
                # test_idx = custom_bisect(row, desired_rank)
                # return row[test_idx - 1::2]

                for idx in range(len(row)):  # Думаю, что для "безопасности" тут лучше перебрать каждый элемент.
                    try:
                        rank = float(row[idx])
                    except ValueError:
                        continue
                    if rank >= desired_rank:
                        return row[idx - 1::2]
        return ["Search failed"]
