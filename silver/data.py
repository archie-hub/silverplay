"""sdfdsf"""
from pydantic import BaseModel
import requests

API_URL = "https://data-asg.goldprice.org/dbXRates/USD"


class Item(BaseModel):
    """asfdsdf"""

    name: str
    symbol: str
    holdings: int
    value: float = 0.0


def get_silver_gold_prices(url=API_URL):
    """dfsdf"""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64;"
        " rv:120.0) Gecko/20100101 Firefox/120.0"
    }
    data = requests.get(url=url, headers=headers, timeout=30).json()
    return data.get("items")[0]


def calculate_our_holdings(holdings, prices):
    """dfsdf"""
    for item in holdings:
        item.value = prices.get(item.symbol) * item.holdings
    return holdings


def new_calculate_our_holdings(holdings, prices):
    """dsfsdf"""
    for item in holdings:
        item["values"] = prices.get(item.get("symbol")) * item.get("holdings")
        item["meltprice"] = prices.get(item.get("symbol"))
    return holdings


def create_ratio(gold, silver):
    """dffd"""
    decimal_value = gold / silver
    numerator = round(decimal_value)
    return f"{numerator}"


def get_melt_prices(silver_onces, gold_onces):
    """dsfsdfds"""
    holdings = [
        {"name": "gold", "symbol": "xauPrice", "holdings": gold_onces},
        {"name": "silver", "symbol": "xagPrice", "holdings": silver_onces},
    ]
    prices = get_silver_gold_prices()

    x = new_calculate_our_holdings(holdings, prices)
    return x
