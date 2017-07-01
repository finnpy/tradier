import json
import time
import urllib
from collections import namedtuple

import requests

Profile = namedtuple("Profile",
                     ["account_number", "day_trader", "option_level", "type", "last_update", "name", "id", "status",
                      "classification"])


def user_profile():
    rsrc = "/v1/user/profile"
    results = _get_all(rsrc, {})
    return results


Balances = namedtuple("Balances", ["account_number", "account_type", "cash_available", "close_pl",
                                   "current_requirement", "day_trade_buying_power", "dividend_balance", "equity",
                                   "fed_call", "long_liquid_value", "long_market_value", "maintenance_call",
                                   "market_value", "net_value", "open_pl", "option_buying_power", "option_long_value",
                                   "option_requirement", "option_short_value", "pending_cash", "pending_orders_count",
                                   "sweep", "short_liquid_value", "short_market_value", "stock_buying_power",
                                   "stock_long_value", "stock_short_value", "uncleared_funds", "unsettled_funds",
                                   "total_cash", "total_equity"])


def user_balances():
    rsrc = "/v1/user/balances"
    results = _get_all(rsrc, {}, shape=Balances)
    return results


def account_balances(account_id):
    rsrc = "/v1/accounts/{}/balances".format(account_id)
    results = _get_all(rsrc, {}, shape=Balances)
    return results


Position = namedtuple('Position', ["cost_basis", "date_acquired", "id", "quantity", "symbol"])


def user_positions():
    rsrc = "/v1/user/positions"
    results = _get_all(rsrc, {}, shape=Position)
    for entry in results:
        print(entry)
    return results


def account_positions(account_id):
    rsrc = "/v1/accounts/{}/positions".format(account_id)


Event = namedtuple('Event', ["amount", "date", "type", "description", "commission",
                             "price", "quantity", "symbol", "trade_type"])


def user_history():
    rsrc = "/v1/user/history"
    results = _get_all(rsrc, {}, shape=Event)
    for entry in results:
        print(entry)
    return results


def account_history(account_id):
    rsrc = "/v1/accounts/{}/history".format(account_id)
    results = _get_all(rsrc, {}, shape=Event)
    for entry in results:
        print(entry)
    return results


CostBasis = namedtuple('CostBasis', ["close_date", "cost", "gain_loss", "gain_loss_percent", "open_date",
                                     "proceeds", "quantity", "symbol", "term"])


def user_gainloss():
    rsrc = "/v1/user/gainloss"
    results = _get_all(rsrc, {}, shape=CostBasis)
    return results


def account_gainloss(account_id):
    rsrc = "/v1/accounts/{}/gainloss".format(account_id)
    results = _get_all(rsrc, {}, shape=CostBasis)
    return results


Order = namedtuple("Order", ["id", "type",  # "class" # FIXME: not supported,
                             "symbol", "side", "quantity", "status", "duration", "price",
                             "option_type", "expiration_date", "exch", "avg_fill_price", "exec_quantity", "exec_exch",
                             "last_price", "last_quantity", "remaining_quantity", "stop_price", "num_legs", "strategy"])


def user_orders():
    rsrc = "/v1/user/orders"
    results = _get_all(rsrc, {}, shape=Order)
    return results


def account_orders(account_id):
    rsrc = "/v1/accounts/{}/orders".format(account_id)
    results = _get_all(rsrc, {}, shape=Order)
    return results


# ---------------------------------------------------------------

QuoteX = namedtuple("QuoteX", ["symbol", "root_symbols", "last", "description", "exch", "type", "change",
                             "open", "close", "prevclose", "low", "high", "week_52_low", "week_52_high",
                             "change_percentage", "volume", "trade_date", "average_volume", "last_volume",
                             "ask", "askexch", "ask_date", "asksize",
                             "bid", "bidexch", "bid_date", "bidsize"])


def market_quotes(symbols):
    results = []
    rsrc = "/v1/markets/quotes"
    params = {"symbols": ",".join(symbols)}
    js = _get_all(rsrc, params)
    for q in js['quotes']['quote']:
        results.append(QuoteX(**q))
    return results


Quote = namedtuple('Quote', ["high", "volume", "low", "date", "close", "open"])


def market_history(symbol, interval=None, start=None, end=None):
    results = []
    rsrc = "/v1/markets/history"
    params = {"symbol": symbol}
    if interval is not None:
        params["interval"] = interval
    if start is not None:
        params["start"] = start
    if end is not None:
        params["end"] = end

    js = _get_all(rsrc, params)
    for s in js['history']['day']: # TODO: support different intervals
        results.append(Quote(**s))
    return results


CalendarDay = namedtuple("CalendarDay", ["date", "status", "description"])


def market_calendar():
    results = []
    rsrc = "/v1/markets/calendar"
    js = _get_all(rsrc, {})
    for day in js['calendar']['days']['day']:
        # print(type(day), day)
        results.append(CalendarDay(date=day["date"], status=day["status"], description=day["description"]))
    return results


# TODO : /v1/markets/timesales
# TODO : /v1/markets/options/chains
# TODO : /v1/markets/options/strikes
# TODO : /v1/markets/options/expirations
# TODO : /v1/markets/clock
# TODO : /v1/markets/search
# TODO : /v1/markets/lookup

# ---------------------------------------------------------------


max_pages = None


def _get(resource, params):
    # TODO : don't open the keys file on every page get
    # TODO : move implementation into separate get_auth() function
    with open("keys.json") as f:
        keys = json.load(f)['tradier']

    query = urllib.urlencode(params)
    uri = "https://sandbox.tradier.com{}?{}".format(resource, query)
    headers = {"Accept": "application/json",
               "Authorization": "Bearer {}".format(keys["token"])}
    t0 = time.time()
    r = requests.get(uri, headers=headers)
    js = r.json()
    with open("raw.text", "w") as f:
        f.write(json.dumps(js))
    t1 = time.time()
    print(json.dumps(js))
    print(t1 - t0)
    return js


def _get_all(resource, params, shape=None):
    return _get(resource, params)


if __name__ == "__main__":
    res = market_calendar()
    print(res)
