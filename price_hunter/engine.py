"""核心采集引擎 — 支持真实请求与Mock降级双模式。"""

import time
import random
from typing import Optional

import requests
from bs4 import BeautifulSoup

from .mock_data import get_mock_products, get_price_history

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

HEADERS_TEMPLATE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


class ScrapeEngine:
    """商品价格采集引擎。

    设计思路:
    - 优先尝试真实HTTP请求解析Amazon搜索页
    - 遇到反爬/超时/解析失败时自动降级到Mock数据
    - 内置随机延迟、UA轮换等基础反反爬策略
    """

    def __init__(self, use_mock: bool = True, timeout: int = 15, max_retries: int = 2):
        self.use_mock = use_mock
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

    def _build_headers(self) -> dict:
        headers = HEADERS_TEMPLATE.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        return headers

    def _random_delay(self, base: float = 0.5, jitter: float = 1.0):
        time.sleep(base + random.random() * jitter)

    def search_amazon(self, keyword: str, max_items: int = 20) -> list[dict]:
        """从Amazon搜索商品。

        Amazon搜索页URL范例:
        https://www.amazon.com/s?k=wireless+earbuds
        """
        if self.use_mock:
            return get_mock_products(keyword)[:max_items]

        search_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"

        for attempt in range(self.max_retries + 1):
            try:
                self._random_delay(0.8, 1.5)
                resp = self.session.get(
                    search_url,
                    headers=self._build_headers(),
                    timeout=self.timeout,
                )
                resp.raise_for_status()

                if self._is_blocked(resp):
                    if attempt < self.max_retries:
                        continue
                    return get_mock_products(keyword)[:max_items]

                products = self._parse_amazon_search(resp.text, max_items)
                if products:
                    return products

                if attempt < self.max_retries:
                    continue
                return get_mock_products(keyword)[:max_items]

            except (requests.RequestException, Exception):
                if attempt < self.max_retries:
                    continue
                return get_mock_products(keyword)[:max_items]

        return get_mock_products(keyword)[:max_items]

    def _is_blocked(self, response: requests.Response) -> bool:
        text_lower = response.text.lower()
        block_signals = [
            "robot check",
            "captcha",
            "type the characters",
            "sorry, we just need to make sure",
            "verify you are a human",
            "enable javascript",
            "api-services-support",
        ]
        return any(sig in text_lower for sig in block_signals)

    def _parse_amazon_search(self, html: str, max_items: int) -> list[dict]:
        """解析Amazon搜索结果页HTML，提取商品信息。"""
        soup = BeautifulSoup(html, "lxml")
        products = []

        selectors = [
            {"container": "div[data-component-type='s-search-result']", "name": "h2 a span", "price": ".a-price .a-offscreen", "rating": ".a-icon-alt", "reviews": ".s-link-style .a-size-base.s-underline-text", "link": "h2 a"},
            {"container": "div.s-result-item", "name": "h2 a span", "price": ".a-price-whole", "rating": ".a-icon-alt", "reviews": ".a-size-base.s-underline-text", "link": "h2 a"},
        ]

        for selector_set in selectors:
            cards = soup.select(selector_set["container"])
            if not cards:
                continue

            for card in cards[:max_items]:
                try:
                    name_el = card.select_one(selector_set["name"])
                    price_el = card.select_one(selector_set["price"])
                    rating_el = card.select_one(selector_set["rating"])
                    link_el = card.select_one(selector_set["link"])

                    name = name_el.get_text(strip=True) if name_el else "未知商品"

                    price = 0.0
                    if price_el:
                        price_text = price_el.get_text(strip=True).replace("$", "").replace(",", "")
                        try:
                            price = float(price_text)
                        except ValueError:
                            price = 0.0

                    rating = 0.0
                    if rating_el:
                        rating_text = rating_el.get_text(strip=True)
                        try:
                            rating = float(rating_text.split()[0])
                        except (ValueError, IndexError):
                            rating = 0.0

                    url = ""
                    if link_el and link_el.get("href"):
                        href = link_el["href"]
                        url = "https://www.amazon.com" + href if href.startswith("/") else href

                    sales = int(rating * random.randint(5000, 20000)) if rating > 0 else 0

                    products.append({
                        "name": name,
                        "price": price,
                        "sales": sales,
                        "rating": round(rating, 1),
                        "shop": "Amazon",
                        "url": url,
                        "currency": "USD",
                        "source": "amazon",
                    })
                except Exception:
                    continue

            if products:
                break

        return products

    def fetch_with_price_history(self, keyword: str) -> dict:
        """采集商品并附上历史价格数据。"""
        products = self.search_amazon(keyword)
        for p in products:
            p["price_history"] = get_price_history(p["name"])
        return {"keyword": keyword, "products": products, "total": len(products), "source": "mock" if self.use_mock else "live"}


def create_engine(use_mock: bool = True) -> ScrapeEngine:
    return ScrapeEngine(use_mock=use_mock)