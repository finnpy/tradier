import json
import unittest
import datetime
import os.path

import tradier

local = True


def inject_response(name):
    name = os.path.join(os.path.dirname(__file__), name)
    with open(name, "r") as f:
        lines = f.readlines()
    print(len(lines))
    tradier._get = lambda rsrc, params: json.loads(lines[0])


class TestAPI(unittest.TestCase):

    def test_market_quotes(self):
        if local:
            inject_response("market_quotes.json")
        r = tradier.market_quotes(["spy", "aapl"])
        print(r)
        if local:
            self.assertEqual(len(r), 2)
            self.assertEqual(r[0].symbol, "SPY")
            self.assertEqual(r[0].high, 243.715)
            self.assertEqual(r[0].volume, 70042599)
            self.assertEqual(r[1].symbol, "AAPL")
            self.assertEqual(r[1].high, 146.11)
            self.assertEqual(r[1].volume, 22082432)

    def test_market_history(self):
        if local:
            inject_response("market_history.json")
        r = tradier.market_history("aapl")
        print(r)
        if local:
            self.assertEqual(len(r), 123)
            self.assertEqual(r[0].high, 116.33)
            self.assertEqual(r[-1].high, 146.11)

    def test_market_calendar(self):
        if local:
            inject_response("market_calendar.json")
        r = tradier.market_calendar()
        for day in r:
            print(day.status),
        if local:
            self.assertEqual(len(r), 30)
            self.assertEqual(r[0].date, "2017-06-01")
            self.assertEqual(r[0].status, "open")
            self.assertEqual(r[24].date, "2017-06-25")
            self.assertEqual(r[24].status, "closed")
            self.assertEqual(r[29].date, "2017-06-30")
            self.assertEqual(r[29].status, "open")


class TestAccounts(unittest.TestCase):

    def test_account_positions(self):
        if local:
            inject_response("account_positions.json")
        pos = tradier.account_positions("87654321")
        if local:
            self.assertEqual(len(pos), 8)
            self.assertSequenceEqual(sorted([c.symbol for c in pos]),
                                     ["AAPL", "BBRY131019P00008000", "DD", "GE",
                                      "GE140118C00025000", "INTC", "SPY131019C00168000", "SPY131019C00170000"])
            for p in pos:
                self.assertIsInstance(p.date_acquired, datetime.datetime)

    def test_user_positions(self):
        if local:
            inject_response("user_positions.json")
        accts = tradier.user_positions()
        if local:
            for pos in accts:
                print(pos)
            self.assertEqual(len(accts), 2)
            self.assertEqual(accts[0].account_number, "12345678")
            self.assertEqual(len(accts[0].positions), 3)
            self.assertEqual(accts[1].account_number, "87654321")
            self.assertEqual(len(accts[1].positions), 8)



if __name__ == "__main__":
    unittest.main(verbosity=2)

