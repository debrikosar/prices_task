from collections import Counter, defaultdict

ITEM_ID_COLUMN_INDEX = 0
SHOP_ID_COLUMN_INDEX = 1
PRICE_COLUMN_INDEX = 2
USER_COLUMN_INDEX = 3

USERNAME_INDEX = 0
REVIEWS_INDEX = 1


def generate_unique_items_list(data):
    items_id_list = set(line[ITEM_ID_COLUMN_INDEX] for line in data)

    return items_id_list


def count_unique_items(data):
    return len(generate_unique_items_list(data))


def generate_unique_shops_list(data):
    shop_id_list = set(line[SHOP_ID_COLUMN_INDEX] for line in data)

    return shop_id_list


def count_unique_shops(data):
    return len(generate_unique_shops_list(data))


def generate_user_statistic(data):
    user_statistic = Counter()

    for line in data:
        user_statistic[line[USER_COLUMN_INDEX]] += 1

    return user_statistic


def find_highest_activity_user(data):
    user_statistic = generate_user_statistic(data)

    return max(user_statistic, key=lambda user: user_statistic[user])


def generate_empty_unique_shop_items_list(data):
    return {shop_key: [] for shop_key in generate_unique_shops_list(data)}


def generate_unique_shop_items_list(data):
    unique_shop_items = defaultdict(list)

    for line in data:
        unique_shop_items[line[SHOP_ID_COLUMN_INDEX]].append(line[ITEM_ID_COLUMN_INDEX])

    return unique_shop_items


def generate_average_prices_list(data):
    average_prices_list = defaultdict(list)

    for line in data:
        average_prices_list[line[ITEM_ID_COLUMN_INDEX]].append(float(line[PRICE_COLUMN_INDEX]))

    for item_key, item_value in average_prices_list.items():
        average_prices_list[item_key] = sum(price for price in item_value) / len(average_prices_list[item_key])

    return average_prices_list


def search_for_boundary_prices(data):
    max_price_item = ()
    min_price_item = ()

    for line in data:
        if not max_price_item:
            max_price_item = line
        elif line[PRICE_COLUMN_INDEX] > max_price_item[PRICE_COLUMN_INDEX]:
            max_price_item = line

        if not min_price_item:
            min_price_item = line
        elif line[PRICE_COLUMN_INDEX] < min_price_item[PRICE_COLUMN_INDEX]:
            min_price_item = line

    min_price_item = (min_price_item[ITEM_ID_COLUMN_INDEX], min_price_item[SHOP_ID_COLUMN_INDEX], min_price_item[PRICE_COLUMN_INDEX])
    max_price_item = (max_price_item[ITEM_ID_COLUMN_INDEX], max_price_item[SHOP_ID_COLUMN_INDEX], max_price_item[PRICE_COLUMN_INDEX])

    return min_price_item, max_price_item
