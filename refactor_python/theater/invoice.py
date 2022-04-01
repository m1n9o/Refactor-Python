import json


def get_data(filename: str) -> dict:
    with open(filename, mode='r', encoding='utf8') as file:
        data = json.load(file)
    return data


def statement(invoice, plays):
    total_amount = 0
    volume_credits = 0
    result = f'Statement for {invoice["customer"]}\n'

    for perf in invoice["performances"]:
        play = plays[perf["playID"]]
        this_amount = amount_for(perf, play)

        # add volume cradits
        volume_credits += max(perf["audience"] - 30, 0)

        # add extra credit for every ten comedy attendees
        if "comedy" == play["type"]:
            volume_credits += perf["audience"] // 5

        # print line for this order
        result += f'\t{play["name"]}: {this_amount / 100} ({perf["audience"]} seats)\n'
        total_amount += this_amount

    result += f'Amount owed is {total_amount / 100}\n'
    result += f'You earned {volume_credits} credits\n'

    return result


def amount_for(perf, play):
    if play["type"] == "tragedy":
        this_amount = 40000
        if perf["audience"] > 30:
            this_amount += 1000 * (perf["audience"] - 30)
    elif play["type"] == "comedy":
        this_amount = 30000
        if perf["audience"] > 20:
            this_amount += 10000 + 500 * (perf["audience"] - 20)
        this_amount += 300 * perf["audience"]
    else:
        raise ValueError(f'unknown type: {play["type"]}')
    return this_amount


if __name__ == '__main__':
    invoice = get_data("invoices.json")[0]
    plays = get_data("plays.json")
    print(statement(invoice, plays))
