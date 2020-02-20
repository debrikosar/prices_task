import argparse
import csv
import os
import time
import calculations


def generate_general_statistic(data, filename):
    item_id_index = 0
    store_id_index = 1
    price_index = 2


    with open('Data_Output/' + filename + '_general_statistic.csv', 'w', newline='') as file:
        prices_stream_writer = csv.writer(file)

        boundary_prices =  calculations.search_for_boundary_prices(data)
        min_price_item = boundary_prices[0]
        max_price_item = boundary_prices[1]

        prices_stream_writer.writerow(["Unique products: ",  calculations.count_unique_items(data)])
        prices_stream_writer.writerow(["Unique shops: ",  calculations.count_unique_shops(data)])
        prices_stream_writer.writerow(["User with highest activity: ",  calculations.find_highest_activity_user(data)])
        prices_stream_writer.writerow(["The cheapest product: ", min_price_item[item_id_index],
                                       " with price: ", min_price_item[price_index],
                                       " from store: ", min_price_item[store_id_index]])
        prices_stream_writer.writerow(["The most expensive product: ", max_price_item[item_id_index],
                                       " with price: ", max_price_item[price_index],
                                       " from store: ", max_price_item[store_id_index]])


def generate_stores_statistic(data, filename):
    shop_id_index = 0
    items_id_index = 1

    with open('Data_Output/' + filename + '_stores_statistic.csv', 'w', newline='') as file:
        stores_stream_writer = csv.writer(file)

        stores_stream_writer.writerow(["Shop ID", "Unique items ID"])

        for line in  calculations.generate_unique_shop_items_list(data).items():
            stores_stream_writer.writerow([line[shop_id_index], len(line[items_id_index])])


def generate_items_statistic(data, filename):
    item_id_index = 0
    price_index = 1

    with open('Data_Output/' + filename + '_items_statistic.csv', 'w', newline='') as file:
        items_stream_writer = csv.writer(file)

        items_stream_writer.writerow(["Item ID", "Item average price"])

        for line in  calculations.generate_average_prices_list(data).items():
            items_stream_writer.writerow([line[item_id_index], line[price_index]])


def data_processing(data, filename):
    generate_general_statistic(data, filename)
    generate_stores_statistic(data, filename)
    generate_items_statistic(data, filename)


def input_file_processing(data_address):
    filename = os.path.splitext(os.path.basename(data_address))[0]

    with open(data_address, newline='') as csv_file:
        stream_reader = csv.reader(csv_file)
        next(stream_reader)

        data = []
        for line in stream_reader:
            data.append(line)

        data_processing(data, filename)


def command_line_input():
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Reports management')
    parser.add_argument('data_address', action='store')
    result = parser.parse_args()

    if not os.path.isfile(result.data_address):
        print("Incorrect Data Address")
    else:
        input_file_processing(result.data_address)

    print(time.time() - start_time)


if __name__ == "__main__":
    command_line_input()
