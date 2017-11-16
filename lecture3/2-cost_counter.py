import csv


def read_amounts():
    with open('goods_amount.csv', 'rt') as file:
        amounts = {}

        r = csv.DictReader(file)
        for row in r:
            if row['name'] in amounts:
                amounts[row['name']] += int(row['amount'])
            else:
                amounts[row['name']] = int(row['amount'])

        return amounts


def read_prices():
    with open('goods_prices.csv', 'rt') as file:
        prices = {}

        r = csv.DictReader(file)
        for row in r:
            prices[row['name']] = float(row['price'])

        return prices


def read_costs():
    with open('goods_prices.csv', 'rt') as prices_file:
        amounts = read_amounts()
        prices = read_prices()
        costs = {}

        for name, amount in amounts.items():
            costs[name] = amount * prices[name]

        return costs


print(read_costs())
