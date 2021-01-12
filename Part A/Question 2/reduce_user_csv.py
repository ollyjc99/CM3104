import csv
import time
import random


def get_sample_businesses(n):
    time_start = time.perf_counter()
    business_list = []
    with open('business_small.csv', 'r') as r_file:
        with open('out/business_small.csv', 'w') as w_file:
            csv_reader = csv.reader(r_file, delimiter=',')
            headers = True
            for row in csv_reader:
                if headers:
                    headers = False
                else:
                    business_list.append(row[0])

            sample_list = random.sample(business_list, n)

    time_finish = time.perf_counter()
    print(f'Finished sampling businesses in {round(time_finish - time_start, 3)} second(s)')

    return sample_list


def reduce_businesses(sample_list):
    time_start = time.perf_counter()
    with open('business_small.csv', 'r') as r_file:
        with open('out/business_small.csv', 'w') as w_file:
            csv_reader = csv.reader(r_file, delimiter=',')
            csv_writer = csv.writer(w_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            headers = True
            for row in csv_reader:
                if headers:
                    headers = False
                    csv_writer.writerow(row)
                else:
                    if row[0] in sample_list:
                        csv_writer.writerow(row)

    time_finish = time.perf_counter()
    print(f'Finished reducing businesses in {round(time_finish - time_start, 3)} second(s)')


def reduce_categories(sample_list):
    time_start = time.perf_counter()
    with open('business_categories_small.csv', 'r') as r_file:
        with open('out/business_categories_small.csv', 'w') as w_file:
            csv_reader = csv.reader(r_file, delimiter=',')
            csv_writer = csv.writer(w_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            headers = True
            for row in csv_reader:
                if headers:
                    headers = False
                    csv_writer.writerow(row)
                else:
                    if row[0] in sample_list:
                        csv_writer.writerow(row)

    time_finish = time.perf_counter()
    print(f'Finished reducing business categories in {round(time_finish - time_start, 3)} second(s)')


def reduce_reviews(business_list):
    time_start = time.perf_counter()
    user_list = []
    with open('review_small.csv', 'r') as r_file:
        with open('out/review_small.csv', 'w') as w_file:
            csv_reader = csv.reader(r_file, delimiter=',')
            csv_writer = csv.writer(w_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            count = 0
            for row in csv_reader:
                if not count:
                    csv_writer.writerow(row)
                else:
                    if row[2] in business_list:
                        user_list.append(row[1])
                        csv_writer.writerow(row)

                count += 1

    time_finish = time.perf_counter()
    print(f'Finished reducing reviews in {round(time_finish - time_start, 3)} second(s)')
    return user_list


def reduce_users(user_list):
    time_start = time.perf_counter()
    with open('user_small.csv', 'r') as r_file:
        with open('out/user_small.csv', 'w') as w_file:
            csv_reader = csv.reader(r_file, delimiter=',')
            csv_writer = csv.writer(w_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            count = 0
            for row in csv_reader:
                if not count:
                    csv_writer.writerow(row)
                else:
                    if row[0] in user_list:
                        csv_writer.writerow(row)

                count += 1

    time_finish = time.perf_counter()
    print(f'Finished reducing users in {round(time_finish - time_start, 3)} second(s)')


def reduce_friendship(user_list):
    time_start = time.perf_counter()
    with open('user_friendship.csv', 'r') as r_file:
        with open('out/user_friendship.csv', 'w') as w_file:
            csv_reader = csv.reader(r_file, delimiter=',')
            csv_writer = csv.writer(w_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            count = 0
            for row in csv_reader:
                if not count:
                    csv_writer.writerow(row)
                else:
                    if row[0] in user_list and row[1] in user_list:
                        csv_writer.writerow(row)

                count += 1

    time_finish = time.perf_counter()
    print(f'Finished reducing user friendship in {round(time_finish - time_start, 3)} second(s)')


def main():
    number_of_businesses = 1000
    sample = get_sample_businesses(number_of_businesses)
    reduce_businesses(sample)
    reduce_categories(sample)
    user_list = reduce_reviews(sample)
    reduce_users(user_list)
    reduce_friendship(user_list)


if __name__ == '__main__':
    main()
