import csv
import os


def get_rec_sku_csv(sku: str, rank=None) -> list:
    """
    main function to check csv using csv
    :param sku:
    :param rank:
    :return:
    """
    if not rank:
        rank: float = 0.0
    with open('.\\data\\recommends.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        result = []
        for row in reader:
            cur_row = row[0].split(',')
            if sku == cur_row[0]:
                rec_rank = float(cur_row[2])
                if rec_rank >= float(rank):
                    result.append(cur_row[1])
            # print(row[0].split(',')[0])
        return result


def test_csv_dict():
    with open('.\\tmp\\recommends.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['sku', 'rec_sku', 'rank'])
        i = 0
        test_dict = {}
        for row in reader:
            if row['sku'] in test_dict.keys():
                test_dict[row['sku']].append([row['rec_sku'], row['rank']])
            else:
                test_dict.update({row['sku']: [[row['rec_sku'], row['rank']]]})
            i += 1
            if i > 1000000:
                break
        print(test_dict['WP260qJAo6'])


def test_csv_text():
    with open('.\\tmp\\recommends.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        test_dict = {}
        for row in reader:
            cur_row = row[0].split(',')
            if cur_row[0] in test_dict.keys():
                test_dict[cur_row[0]].append([cur_row[1], cur_row[2]])
            else:
                test_dict.update({cur_row[0]: [[cur_row[1], cur_row[2]]]})
            # i += 1
            # if i > 1000000:
            #     break
        print(test_dict['WP260qJAo6'])


def get_data_from_csv(filename, criterion1, criterion2):
    with open(filename) as csvfile:
        datareader = csv.reader(csvfile)
        yield next(datareader)  # yield the header row
        count = 0
        print(1)
        for row in datareader:
            if row[0] == criterion1:
                if float(row[2]) >= float(criterion2):
                    yield row[1]


def getdata(filename, criterion1, criterion2):
    # for criterion in criteria:
    for row in get_data_from_csv(filename, criterion1, criterion2):
        yield row


def _get_reader(input_filename, csv_reader, encoding, delimiter):
    """Get the reader instance. This will either open the file, or
    return the csv_reader supplied by the caller.
    """
    if csv_reader:
        return csv_reader

    with open(input_filename, newline='', encoding=encoding) as input_fp:
        return csv.reader(input_fp, delimiter=delimiter)


def two_reader_one_writer():
    with open('.\\tmp\\recommends.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        i = 0
        test_dict = {}
        for row in reader:
            cur_row = row[0].split(',')
            if os.path.isfile(f".\\tmp\\abc_split\\{cur_row[0][0].lower()}.csv") is True:
                with open(f".\\tmp\\abc_split\\{cur_row[0][0].lower()}.csv", 'a', newline='') as csvfile_2:
                    writer = csv.writer(csvfile_2, delimiter=' ', quotechar='|')
                    writer.writerow([cur_row[0], cur_row[1], cur_row[2]])
                    csvfile_2.close()
            else:
                with open(f".\\tmp\\abc_split\\else.csv", 'a', newline='') as csvfile_2:
                    writer = csv.writer(csvfile_2, delimiter=' ', quotechar='|')
                    writer.writerow([cur_row[0], cur_row[1], cur_row[2]])
                    csvfile_2.close()
            i += 1
            print(i)


def create_csv():
    for i in 'abccdefghijklmnopqrstuvwxyz1234567890':
        if os.path.isfile(f".\\tmp\\abc_split\\{i}.csv") is False:
            j = open(f'.\\tmp\\abc_split\\{i}.csv', 'w')
            j.close()
    if os.path.isfile(f".\\tmp\\abc_split\\else.csv") is False:
        j = open(f'.\\tmp\\abc_split\\else.csv', 'w')
        j.close()


if __name__ == '__main__':
    # print(get_rec_sku_csv("WP260qJAo6"))
    # test_csv_text()
    print("Start")
    # two_reader_one_writer()
    create_csv()
    two_reader_one_writer()
    # print(get_data_from_csv('.\\tmp\\recommends.csv', "WP260qJAo6"))
    # for row in getdata('.\\tmp\\recommends.csv', "WP260qJAo6", '0.9'):
    #     print(row)
    print("End")
