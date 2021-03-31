import csv


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
    with open('.\\data\\recommends.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['sku','rec_sku','rank'])
        i = 0
        test_dict = {}
        for row in reader:
            if row['sku'] in test_dict.keys():
                test_dict[row['sku']].append([row['rec_sku'],row['rank']])
            else:
                test_dict.update({row['sku']:[[row['rec_sku'],row['rank']]]})
            i += 1
            if i > 1000000:
                break
        print(test_dict['WP260qJAo6'])


def test_csv_text():
    with open('.\\data\\recommends.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['sku','rec_sku','rank'])
        i = 0
        test_dict = {}
        for row in reader:
            if row['sku'] in test_dict.keys():
                test_dict[row['sku']].append([row['rec_sku'],row['rank']])
            else:
                test_dict.update({row['sku']:[[row['rec_sku'],row['rank']]]})
            i += 1
            if i > 1000000:
                break
        print(test_dict['WP260qJAo6'])

if __name__ == '__main__':
    # print(get_rec_sku_csv("WP260qJAo6"))
    test_csv()