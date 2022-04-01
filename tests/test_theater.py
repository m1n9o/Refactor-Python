from refactor_python.theater.invoice import statement, get_data


class TestTheater:

    def test_result_of_statement(self):
        invoice = get_data("test_invoices.json")[0]
        plays = get_data("test_plays.json")
        print(statement(invoice, plays))
        assert statement(invoice, plays) == 'Statement for BiCo\n\tHamlet: 650.0 (55 seats)\nAmount owed is 650.0\nYou earned 25 credits\n'
