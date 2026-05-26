"""数据清洗与去重模块。"""

import re
from typing import Any


def clean_products(products: list[dict]) -> list[dict]:
    """清洗商品列表：去重、价格标准化、异常值过滤。"""
    cleaned = []

    for p in products:
        cp = p.copy()

        cp["name"] = cp.get("name", "").strip()
        if not cp["name"] or cp["name"] == "未知商品":
            continue

        cp["name"] = re.sub(r"\s+", " ", cp["name"])

        price = cp.get("price", 0)
        try:
            price = float(price)
        except (ValueError, TypeError):
            price = 0.0
        cp["price"] = round(max(price, 0), 2)

        rating = cp.get("rating", 0)
        try:
            rating = float(rating)
        except (ValueError, TypeError):
            rating = 0.0
        cp["rating"] = round(min(max(rating, 0), 5.0), 1)

        sales = cp.get("sales", 0)
        try:
            sales = int(sales)
        except (ValueError, TypeError):
            sales = 0
        cp["sales"] = max(sales, 0)

        cp["shop"] = cp.get("shop", "未知店铺").strip()
        cp["url"] = cp.get("url", "").strip()
        cp["currency"] = cp.get("currency", "CNY")
        cp["source"] = cp.get("source", "unknown")

        cleaned.append(cp)

    return deduplicate(cleaned)


def deduplicate(products: list[dict]) -> list[dict]:
    """按商品名称去重，保留首次出现的数据。"""
    seen = set()
    unique = []
    for p in products:
        name_key = p["name"].lower().strip()
        if name_key not in seen:
            seen.add(name_key)
            unique.append(p)
    return unique


def filter_outliers(products: list[dict], price_upper_percentile: float = 95.0) -> list[dict]:
    """过滤价格异常值（价格过高或为0的商品）。"""
    prices = [p["price"] for p in products if p["price"] > 0]
    if not prices:
        return products

    sorted_prices = sorted(prices)
    idx = min(int(len(sorted_prices) * price_upper_percentile / 100), len(sorted_prices) - 1)
    upper_bound = sorted_prices[idx] * 1.5 if idx < len(sorted_prices) else float("inf")

    return [p for p in products if 0 < p["price"] <= upper_bound]


def compute_cost_performance(products: list[dict]) -> list[dict]:
    """计算性价比评分: (rating * log(sales+1)) / price，归一化到0~100。"""
    for p in products:
        if p["price"] > 0:
            import math
            raw = (p["rating"] * math.log(p["sales"] + 1)) / p["price"]
        else:
            raw = 0
        p["cp_score_raw"] = raw

    scores = [p.get("cp_score_raw", 0) for p in products]
    max_score = max(scores) if scores else 1
    min_score = min(scores) if scores else 0
    score_range = max_score - min_score if max_score > min_score else 1

    for p in products:
        raw = p.pop("cp_score_raw", 0)
        p["cp_score"] = round((raw - min_score) / score_range * 100, 1)

    return products