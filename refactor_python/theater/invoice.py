import json


def get_data(filename: str) -> dict:
    with open(filename, mode='r', encoding='utf8') as file:
        data = json.load(file)
    return data


def statement(invoice, plays):
    statement_data = {}
    statement_data["customer"] = invoice["customer"]
    statement_data["performances"] = invoice["performances"]
    return render_plain_text(statement_data, plays)


def render_plain_text(data, plays):
    result = f'Statement for {data["customer"]}\n'
    for perf in data["performances"]:
        result += f'\t{play_for(perf, plays)["name"]}: {amount_for(perf, play_for(perf, plays)) / 100} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {total_amount(data, plays) / 100}\n'
    result += f'You earned {total_volume_credits(data, plays)} credits\n'
    return result


def total_amount(data, plays):
    result = 0
    for perf in data["performances"]:
        result += amount_for(perf, play_for(perf, plays))
    return result


def total_volume_credits(data, plays):
    volume_credits = 0
    for perf in data["performances"]:
        volume_credits = volume_credits_for(perf, plays, volume_credits)
    return volume_credits


def volume_credits_for(a_performance, plays, volume_credits):
    volume_credits += max(a_performance["audience"] - 30, 0)
    if "comedy" == play_for(a_performance, plays)["type"]:
        volume_credits += a_performance["audience"] // 5
    return volume_credits


def play_for(perf, plays):
    return plays[perf["playID"]]


def amount_for(a_performance, play):
    if play["type"] == "tragedy":
        result = 40000
        if a_performance["audience"] > 30:
            result += 1000 * (a_performance["audience"] - 30)
    elif play["type"] == "comedy":
        result = 30000
        if a_performance["audience"] > 20:
            result += 10000 + 500 * (a_performance["audience"] - 20)
        result += 300 * a_performance["audience"]
    else:
        raise ValueError(f'unknown type: {play["type"]}')
    return result


if __name__ == '__main__':
    invoice = get_data("invoices.json")[0]
    plays = get_data("plays.json")
    print(statement(invoice, plays))
