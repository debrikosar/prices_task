import argparse
import csv
import os


def generate_unique_items_list(stream_reader):
    items_id_list = []

    next(stream_reader)
    for line in stream_reader:
        if not line[0] in items_id_list:
            items_id_list.append(line[0])

    return items_id_list


def count_unique_items(stream_reader):
    return len(generate_unique_items_list(stream_reader))


def generate_unique_shops_list(stream_reader):
    shop_id_list = []

    next(stream_reader)
    for line in stream_reader:
        if not line[1] in shop_id_list:
            shop_id_list.append(line[1])

    return shop_id_list


def count_unique_shops(stream_reader):
    return len(generate_unique_shops_list(stream_reader))


def generate_user_statistic(stream_reader):
    user_statistic = {}

    next(stream_reader)
    for line in stream_reader:
        if not line[3] in user_statistic.keys():
            user_statistic[line[3]] = 1
        else:
            user_statistic[line[3]] += 1

    return user_statistic


def find_highest_activity_user(stream_reader):
    user_statistic = generate_user_statistic(stream_reader)
    highest_activity_user = ("None", 0)

    for user in user_statistic.items():
        if user[1] > highest_activity_user[1]:
            highest_activity_user = user

    return highest_activity_user[0]


def generate_empty_unique_shop_items_list(stream_reader):
    return {shop_key: [] for shop_key in generate_unique_shops_list(stream_reader)}


def generate_unique_shop_items_list(stream_reader, empty_unique_shop_items):
    unique_shop_items = empty_unique_shop_items

    next(stream_reader)
    for line in stream_reader:
        if not line[0] in empty_unique_shop_items[line[1]]:
            unique_shop_items[line[1]].append(line[0])

    return unique_shop_items


def generate_empty_average_prices_list(stream_reader):
    empty_average_prices_list = {item_key: [] for item_key in generate_unique_items_list(stream_reader)}

    return empty_average_prices_list


def generate_average_prices_list(stream_reader, empty_average_prices_list):
    average_prices_list = empty_average_prices_list

    next(stream_reader)
    for line in stream_reader:
        average_prices_list[line[0]].append(line[2])

    for item in average_prices_list.items():
        average_prices_list[item[0]] = sum([float(i) for i in average_prices_list[item[0]]]) \
                                       / len(average_prices_list[item[0]])

    return average_prices_list


def search_for_boundary_prices(stream_reader):
    max_price_item = ()
    min_price_item = ()

    next(stream_reader)
    for line in stream_reader:
        if not max_price_item:
            max_price_item = line
        else:
            if line[2] > max_price_item[2]:
                max_price_item = line

        if not min_price_item:
            min_price_item = line
        else:
            if line[2] < min_price_item[2]:
                min_price_item = line

    min_price_item = (min_price_item[0], min_price_item[1], min_price_item[2])
    max_price_item = (max_price_item[0], max_price_item[1], max_price_item[2])

    return min_price_item, max_price_item


def command_line_input():
    parser = argparse.ArgumentParser(description='Reports management')
    parser.add_argument('data_address', action='store')
    result = parser.parse_args()

    if not os.path.isfile(result.data_address):
        print("Incorrect Data Address")
    else:
        filename = os.path.splitext(os.path.basename(result.data_address))[0]
        with open(result.data_address, newline='') as csv_file:
            stream_reader = csv.reader(csv_file)

            unique_items_number = count_unique_items(stream_reader)
            csv_file.seek(0)

            unique_shops_number = count_unique_shops(stream_reader)
            csv_file.seek(0)

            highest_activity_user = find_highest_activity_user(stream_reader)
            csv_file.seek(0)

            empty_unique_shop_items = generate_empty_unique_shop_items_list(stream_reader)
            csv_file.seek(0)

            unique_shop_items = generate_unique_shop_items_list(stream_reader, empty_unique_shop_items)
            csv_file.seek(0)

            empty_average_prices = generate_empty_average_prices_list(stream_reader)
            csv_file.seek(0)

            average_prices = generate_average_prices_list(stream_reader, empty_average_prices)
            csv_file.seek(0)

            boundary_prices = search_for_boundary_prices(stream_reader)
            csv_file.seek(0)

    with open(filename + '_general_statistic.csv', 'w', newline='') as file:
        prices_stream_writer = csv.writer(file)

        prices_stream_writer.writerow(["Unique products: ", unique_items_number])
        prices_stream_writer.writerow(["Unique shops: ", unique_shops_number])
        prices_stream_writer.writerow(["User with highest activity: ", highest_activity_user])
        prices_stream_writer.writerow(["The cheapest product: ", boundary_prices[0][0],
                                       " with price: ", boundary_prices[0][2],
                                       " from store: ", boundary_prices[0][1]])
        prices_stream_writer.writerow(["The most expensive product: ", boundary_prices[1][0],
                                       " with price: ", boundary_prices[1][2],
                                       " from store: ", boundary_prices[1][1]])

    with open(filename + '_stores_statistic.csv', 'w', newline='') as file:
        stores_stream_writer = csv.writer(file)

        stores_stream_writer.writerow(["Shop ID", "Unique items ID"])

        for line in unique_shop_items.items():
            stores_stream_writer.writerow([line[0], len(line[1])])

    with open(filename + '_items_statistic.csv', 'w', newline='') as file:
        items_stream_writer = csv.writer(file)

        items_stream_writer.writerow(["Item ID", "Item average price"])

        for line in average_prices.items():
            items_stream_writer.writerow([line[0], line[1]])


if __name__ == "__main__":
    command_line_input()
