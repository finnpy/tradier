import json
import unittest

import tradier

local = True


def inject_response(name):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)

