from collections import Counter, defaultdict


def generate_unique_items_list(data):
    items_id_column_index = 0
    items_id_list = []

    for line in data:
        if not line[items_id_column_index] in items_id_list:
            items_id_list.append(line[items_id_column_index])

    return items_id_list


def count_unique_items(data):
    return len(generate_unique_items_list(data))


def generate_unique_shops_list(data):
    shop_id_column_index = 1
    shop_id_list = []

    for line in data:
        if not line[shop_id_column_index] in shop_id_list:
            shop_id_list.append(line[shop_id_column_index])

    return shop_id_list


def count_unique_shops(data):
    return len(generate_unique_shops_list(data))


def generate_user_statistic(data):
    user_column_index = 3
    user_statistic = Counter()

    for line in data:
        user_statistic[line[user_column_index]] += 1

    return user_statistic


def find_highest_activity_user(data):
    username_index = 0
    reviews_number_index = 1
    highest_activity_user = ("None", 0)
    user_statistic = generate_user_statistic(data)

    for user in user_statistic.items():
        if user[reviews_number_index] > highest_activity_user[reviews_number_index]:
            highest_activity_user = user

    return highest_activity_user[username_index]


def generate_empty_unique_shop_items_list(data):
    return {shop_key: [] for shop_key in generate_unique_shops_list(data)}


def generate_unique_shop_items_list(data):
    item_id_column_index = 0
    store_id_column_index = 1
    empty_unique_shop_items = generate_empty_unique_shop_items_list(data)
    unique_shop_items = empty_unique_shop_items

    for line in data:
        if not line[item_id_column_index] in empty_unique_shop_items[line[store_id_column_index]]:
            unique_shop_items[line[store_id_column_index]].append(line[item_id_column_index])

    return unique_shop_items


def generate_average_prices_list(data):
    item_id_index = 0
    item_price_index = 2

    apl = defaultdict(list)

    for line in data:
        apl[line[item_id_index]].append(float(line[item_price_index]))

    for item_key, item_value in apl.items():
        apl[item_key] = sum(price for price in item_value) / len(apl[item_key])

    return apl


def search_for_boundary_prices(data):
    item_id_index = 0
    store_id_index = 1
    price_index = 2
    max_price_item = ()
    min_price_item = ()

    for line in data:
        if not max_price_item:
            max_price_item = line
        elif line[price_index] > max_price_item[price_index]:
                max_price_item = line

        if not min_price_item:
            min_price_item = line
        elif line[price_index] < min_price_item[price_index]:
                min_price_item = line

    min_price_item = (min_price_item[item_id_index], min_price_item[store_id_index], min_price_item[price_index])
    max_price_item = (max_price_item[item_id_index], max_price_item[store_id_index], max_price_item[price_index])

    return min_price_item, max_price_item
