import json


def play_for(perf, plays):
    return plays[perf["playID"]]


def render_plain_text(data, plays):
    result = f'Statement for {data["customer"]}\n'
    for perf in data["performances"]:
        result += f'\t{play_for(perf, plays)["name"]}: {amount_for(perf, play_for(perf, plays)) / 100} ({perf["audience"]} seats)\n'
    result += f'Amount owed is {total_amount(data, plays) / 100}\n'
    result += f'You earned {total_volume_credits(data, plays)} credits\n'
    return result


def html_statement(invoice, plays):
    return render_html(create_statement_data(invoice, plays), plays)


def render_html(data, plays):
    result = f'<h1>Statement for {data["customer"]}</h1>\n'
    result += "<table>\n"
    result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>"

    for perf in data["performances"]:
        result += f'<tr> <td> {play_for(perf, plays)["name"]} </td><td> {perf["audience"]} </td>'
        result += f'<td>${amount_for(perf, play_for(perf, plays)) / 100}</td></tr>\n'
    result += "</table>\n"
    result += f'<p>Amount owed is <em>{total_amount(data, plays) / 100}</em></p>\n'
    result += f'<p>You earned <em>${total_volume_credits(data, plays)}</em> credits</p>\n'
    return result


def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays), plays)


def create_statement_data(invoice, plays):
    statement_data = {
        "customer": invoice["customer"],
        "performances": invoice["performances"]
    }
    statement_data["total_amount"] = total_amount(statement_data, plays)
    statement_data["total_volume_credits"] = total_volume_credits(statement_data, plays)
    return statement_data


def total_volume_credits(data, plays):
    volume_credits = 0
    for perf in data["performances"]:
        volume_credits = volume_credits_for(perf, plays, volume_credits)
    return volume_credits


def total_amount(data, plays):
    result = 0
    for perf in data["performances"]:
        result += amount_for(perf, play_for(perf, plays))
    return result


def get_data(filename: str) -> dict:
    with open(filename, mode='r', encoding='utf8') as file:
        data = json.load(file)
    return data


def volume_credits_for(a_performance, plays, volume_credits):
    volume_credits += max(a_performance["audience"] - 30, 0)
    if "comedy" == play_for(a_performance, plays)["type"]:
        volume_credits += a_performance["audience"] // 5
    return volume_credits


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
