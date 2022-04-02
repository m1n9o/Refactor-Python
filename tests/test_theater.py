from refactor_python.theater.invoice import statement, get_data, html_statement


class TestTheater:

    def test_result_of_statement(self):
        invoice = get_data("test_invoices.json")[0]
        plays = get_data("test_plays.json")
        assert statement(invoice,
                         plays) == 'Statement for BiCo\n\tHamlet: 650.0 (55 seats)\nAmount owed is 650.0\nYou earned 25 credits\n'

    def test_result_of_html_statement(self):
        invoice = get_data("test_invoices.json")[0]
        plays = get_data("test_plays.json")
        assert html_statement(invoice, plays) == '<h1>Statement for BiCo</h1>\n<table>\n<tr><th>play</th><th>seats</th><th>cost</th></tr><tr> <td> Hamlet </td><td> 55 </td><td>$650.0</td></tr>\n</table>\n<p>Amount owed is <em>650.0</em></p>\n<p>You earned <em>$25</em> credits</p>\n'
