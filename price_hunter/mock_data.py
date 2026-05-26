"""模拟商品数据 — 覆盖多个品类的真实感商品，用于演示和降级场景。"""

import random

MOCK_PRODUCTS = {
    "无线耳机": [
        {"name": "Apple AirPods Pro (第二代)", "price": 1799.00, "sales": 85000, "rating": 4.8, "shop": "Apple 官方旗舰店", "url": "https://www.amazon.com/dp/B0BDHWDRZ9", "currency": "CNY", "source": "amazon"},
        {"name": "Sony WF-1000XM5 真无线降噪耳机", "price": 1599.00, "sales": 62000, "rating": 4.7, "shop": "Sony 官方旗舰店", "url": "https://www.amazon.com/dp/B0C33LKV7C", "currency": "CNY", "source": "amazon"},
        {"name": "Samsung Galaxy Buds3 Pro", "price": 1399.00, "sales": 41000, "rating": 4.5, "shop": "Samsung 官方店", "url": "https://www.amazon.com/dp/B0D949JX7N", "currency": "CNY", "source": "amazon"},
        {"name": "Bose QuietComfort Ultra 消噪耳机", "price": 2299.00, "sales": 38000, "rating": 4.6, "shop": "Bose 旗舰店", "url": "https://www.amazon.com/dp/B0CD2FSV5B", "currency": "CNY", "source": "amazon"},
        {"name": "JBL Tour Pro 3 真无线耳机", "price": 1899.00, "sales": 15000, "rating": 4.4, "shop": "JBL 官方旗舰店", "url": "https://www.amazon.com/dp/B0DG3XMCMW", "currency": "CNY", "source": "amazon"},
        {"name": "Anker Soundcore Liberty 4 NC", "price": 499.00, "sales": 72000, "rating": 4.5, "shop": "Anker 旗舰店", "url": "https://www.amazon.com/dp/B0C3L7ZVT1", "currency": "CNY", "source": "amazon"},
        {"name": "SoundPEATS Air4 Pro 降噪耳机", "price": 299.00, "sales": 55000, "rating": 4.3, "shop": "SoundPEATS 旗舰店", "url": "https://www.amazon.com/dp/B0CK2RMNDP", "currency": "CNY", "source": "amazon"},
        {"name": "EarFun Air Pro 4 无线耳机", "price": 449.00, "sales": 28000, "rating": 4.4, "shop": "EarFun 官方店", "url": "https://www.amazon.com/dp/B0D6G8HZ4V", "currency": "CNY", "source": "amazon"},
    ],
    "机械键盘": [
        {"name": "Keychron K8 Pro 无线机械键盘", "price": 599.00, "sales": 35000, "rating": 4.7, "shop": "Keychron 旗舰店", "url": "https://www.amazon.com/dp/B0B2DGH287", "currency": "CNY", "source": "amazon"},
        {"name": "Logitech MX Mechanical 无线键盘", "price": 899.00, "sales": 48000, "rating": 4.6, "shop": "Logitech 官方旗舰店", "url": "https://www.amazon.com/dp/B09YLFTS1Z", "currency": "CNY", "source": "amazon"},
        {"name": "ROG Azoth 75% 无线机械键盘", "price": 1499.00, "sales": 12000, "rating": 4.8, "shop": "ROG 玩家国度旗舰店", "url": "https://www.amazon.com/dp/B0BXSKV1H8", "currency": "CNY", "source": "amazon"},
        {"name": "Razer BlackWidow V4 Pro", "price": 1399.00, "sales": 18000, "rating": 4.5, "shop": "Razer 雷蛇旗舰店", "url": "https://www.amazon.com/dp/B0BT2YFFQV", "currency": "CNY", "source": "amazon"},
        {"name": "AULA F75 三模机械键盘", "price": 259.00, "sales": 95000, "rating": 4.5, "shop": "AULA 官方店", "url": "https://www.amazon.com/dp/B0CRGQ4NCZ", "currency": "CNY", "source": "amazon"},
        {"name": "RK Royal Kludge R87 无线键盘", "price": 189.00, "sales": 110000, "rating": 4.4, "shop": "RK 官方旗舰店", "url": "https://www.amazon.com/dp/B0BXSFMXL9", "currency": "CNY", "source": "amazon"},
        {"name": "NuPhy Air75 V2 矮轴机械键盘", "price": 799.00, "sales": 22000, "rating": 4.6, "shop": "NuPhy 旗舰店", "url": "https://www.amazon.com/dp/B0CFYVN2LB", "currency": "CNY", "source": "amazon"},
        {"name": "Lofree Flow 矮轴无线键盘", "price": 899.00, "sales": 16000, "rating": 4.5, "shop": "Lofree 洛斐旗舰店", "url": "https://www.amazon.com/dp/B0CJ57L5FD", "currency": "CNY", "source": "amazon"},
    ],
    "显示器": [
        {"name": "LG 27GP950-B 27寸 4K 160Hz", "price": 4999.00, "sales": 15000, "rating": 4.7, "shop": "LG 旗舰店", "url": "https://www.amazon.com/dp/B093MFKDLB", "currency": "CNY", "source": "amazon"},
        {"name": "Dell S2722QC 27寸 4K USB-C", "price": 2499.00, "sales": 42000, "rating": 4.6, "shop": "Dell 官方旗舰店", "url": "https://www.amazon.com/dp/B09DTDRJWP", "currency": "CNY", "source": "amazon"},
        {"name": "Samsung Odyssey G7 32寸 240Hz", "price": 3499.00, "sales": 22000, "rating": 4.5, "shop": "Samsung 旗舰店", "url": "https://www.amazon.com/dp/B08FF3W3M8", "currency": "CNY", "source": "amazon"},
        {"name": "AOC U27N3C 27寸 4K Type-C", "price": 1699.00, "sales": 56000, "rating": 4.4, "shop": "AOC 旗舰店", "url": "https://www.amazon.com/dp/B09YDLNDPN", "currency": "CNY", "source": "amazon"},
        {"name": "小米 Redmi 27寸 4K 显示器", "price": 1299.00, "sales": 88000, "rating": 4.5, "shop": "小米官方旗舰店", "url": "https://www.amazon.com/dp/B0C7V3JNHX", "currency": "CNY", "source": "amazon"},
        {"name": "ASUS ProArt PA279CRV 27寸 4K", "price": 3299.00, "sales": 18000, "rating": 4.6, "shop": "ASUS 旗舰店", "url": "https://www.amazon.com/dp/B0C4FCV78K", "currency": "CNY", "source": "amazon"},
        {"name": "HKC 27寸 2K 180Hz 电竞屏", "price": 899.00, "sales": 72000, "rating": 4.3, "shop": "HKC 旗舰店", "url": "https://www.amazon.com/dp/B0CKYPNLZP", "currency": "CNY", "source": "amazon"},
        {"name": "ViewSonic VX2758-2K-PRO 27寸", "price": 1099.00, "sales": 38000, "rating": 4.4, "shop": "ViewSonic 旗舰店", "url": "https://www.amazon.com/dp/B0BZJYMWKK", "currency": "CNY", "source": "amazon"},
    ],
    "移动电源": [
        {"name": "Anker PowerCore 26800mAh 87W", "price": 399.00, "sales": 68000, "rating": 4.7, "shop": "Anker 旗舰店", "url": "https://www.amazon.com/dp/B01M9BYX2N", "currency": "CNY", "source": "amazon"},
        {"name": "小米 20000mAh 50W 快充充电宝", "price": 199.00, "sales": 120000, "rating": 4.6, "shop": "小米官方旗舰店", "url": "https://www.amazon.com/dp/B0CKYHZ45P", "currency": "CNY", "source": "amazon"},
        {"name": "Baseus 65W 20000mAh 笔记本充电宝", "price": 259.00, "sales": 95000, "rating": 4.5, "shop": "Baseus 倍思旗舰店", "url": "https://www.amazon.com/dp/B08THMRFZV", "currency": "CNY", "source": "amazon"},
        {"name": "Zendure SuperTank Pro 26800mAh", "price": 899.00, "sales": 8000, "rating": 4.6, "shop": "Zendure 旗舰店", "url": "https://www.amazon.com/dp/B08G1K8CBF", "currency": "CNY", "source": "amazon"},
        {"name": "ROMOSS 30000mAh 22.5W 快充", "price": 129.00, "sales": 150000, "rating": 4.4, "shop": "罗马仕旗舰店", "url": "https://www.amazon.com/dp/B0CKL2MV85", "currency": "CNY", "source": "amazon"},
        {"name": "UGREEN 145W 25000mAh 充电宝", "price": 499.00, "sales": 35000, "rating": 4.6, "shop": "UGREEN 绿联旗舰店", "url": "https://www.amazon.com/dp/B0CRH72TGF", "currency": "CNY", "source": "amazon"},
        {"name": "Mophie Powerstation XXL 20000mAh", "price": 349.00, "sales": 12000, "rating": 4.3, "shop": "Mophie 旗舰店", "url": "https://www.amazon.com/dp/B07H5RPCGK", "currency": "CNY", "source": "amazon"},
        {"name": "SHARGE 闪极 100W 10000mAh", "price": 599.00, "sales": 18000, "rating": 4.5, "shop": "SHARGE 闪极旗舰店", "url": "https://www.amazon.com/dp/B0CLV5HM8Z", "currency": "CNY", "source": "amazon"},
    ],
    "智能手表": [
        {"name": "Apple Watch Ultra 2", "price": 6499.00, "sales": 25000, "rating": 4.8, "shop": "Apple 官方旗舰店", "url": "https://www.amazon.com/dp/B0CHX4TLGX", "currency": "CNY", "source": "amazon"},
        {"name": "Samsung Galaxy Watch6 Classic", "price": 2499.00, "sales": 32000, "rating": 4.5, "shop": "Samsung 官方店", "url": "https://www.amazon.com/dp/B0C799LBM3", "currency": "CNY", "source": "amazon"},
        {"name": "华为 Watch GT 4 46mm", "price": 1488.00, "sales": 95000, "rating": 4.6, "shop": "华为官方旗舰店", "url": "https://www.amazon.com/dp/B0CHB68PY7", "currency": "CNY", "source": "amazon"},
        {"name": "Garmin Fenix 7X Pro", "price": 5880.00, "sales": 8000, "rating": 4.7, "shop": "Garmin 佳明旗舰店", "url": "https://www.amazon.com/dp/B0C4XTBRZ8", "currency": "CNY", "source": "amazon"},
        {"name": "Amazfit GTR 4 智能手表", "price": 999.00, "sales": 55000, "rating": 4.4, "shop": "Amazfit 跃我旗舰店", "url": "https://www.amazon.com/dp/B0B8NGPK2J", "currency": "CNY", "source": "amazon"},
        {"name": "小米 Watch S3", "price": 799.00, "sales": 78000, "rating": 4.3, "shop": "小米官方旗舰店", "url": "https://www.amazon.com/dp/B0CP2K4T2Q", "currency": "CNY", "source": "amazon"},
        {"name": "Google Pixel Watch 2", "price": 2299.00, "sales": 12000, "rating": 4.4, "shop": "Google Store", "url": "https://www.amazon.com/dp/B0CGJ4QPGW", "currency": "CNY", "source": "amazon"},
        {"name": "Fitbit Versa 4 智能手表", "price": 1499.00, "sales": 28000, "rating": 4.3, "shop": "Fitbit 旗舰店", "url": "https://www.amazon.com/dp/B0B4N2VKK4", "currency": "CNY", "source": "amazon"},
    ],
    "蓝牙音箱": [
        {"name": "JBL Flip 6 便携蓝牙音箱", "price": 699.00, "sales": 75000, "rating": 4.7, "shop": "JBL 官方旗舰店", "url": "https://www.amazon.com/dp/B09HC5GRT9", "currency": "CNY", "source": "amazon"},
        {"name": "Marshall Emberton II 蓝牙音箱", "price": 1199.00, "sales": 45000, "rating": 4.7, "shop": "Marshall 官方旗舰店", "url": "https://www.amazon.com/dp/B0B7RHPKV3", "currency": "CNY", "source": "amazon"},
        {"name": "Bose SoundLink Flex 蓝牙音箱", "price": 1099.00, "sales": 28000, "rating": 4.6, "shop": "Bose 旗舰店", "url": "https://www.amazon.com/dp/B099T82KRJ", "currency": "CNY", "source": "amazon"},
        {"name": "Sony SRS-XB100 便携蓝牙音箱", "price": 299.00, "sales": 62000, "rating": 4.5, "shop": "Sony 官方旗舰店", "url": "https://www.amazon.com/dp/B0C33LBC8P", "currency": "CNY", "source": "amazon"},
        {"name": "Tribit StormBox Micro 2", "price": 259.00, "sales": 38000, "rating": 4.4, "shop": "Tribit 旗舰店", "url": "https://www.amazon.com/dp/B0BYN1W481", "currency": "CNY", "source": "amazon"},
        {"name": "Anker Soundcore Motion+", "price": 349.00, "sales": 52000, "rating": 4.5, "shop": "Anker 旗舰店", "url": "https://www.amazon.com/dp/B07P8WDMPW", "currency": "CNY", "source": "amazon"},
        {"name": "Ultimate Ears BOOM 3 蓝牙音箱", "price": 899.00, "sales": 20000, "rating": 4.4, "shop": "UE 旗舰店", "url": "https://www.amazon.com/dp/B07FT2ZVX9", "currency": "CNY", "source": "amazon"},
        {"name": "Harman Kardon Aura Studio 4", "price": 2399.00, "sales": 8000, "rating": 4.7, "shop": "Harman Kardon 旗舰店", "url": "https://www.amazon.com/dp/B0CJ56PQPV", "currency": "CNY", "source": "amazon"},
    ],
}

PRICE_HISTORY_BASE = {
    "Apple AirPods Pro (第二代)": [1899, 1859, 1829, 1799, 1799, 1849, 1829, 1799, 1799, 1799, 1759, 1799],
    "Sony WF-1000XM5 真无线降噪耳机": [1699, 1659, 1629, 1599, 1599, 1599, 1629, 1599, 1599, 1559, 1599, 1599],
    "Samsung Galaxy Buds3 Pro": [1499, 1459, 1429, 1399, 1399, 1399, 1399, 1429, 1399, 1359, 1399, 1399],
    "Bose QuietComfort Ultra 消噪耳机": [2399, 2359, 2329, 2299, 2299, 2299, 2359, 2299, 2299, 2259, 2299, 2299],
    "JBL Tour Pro 3 真无线耳机": [1999, 1959, 1929, 1899, 1899, 1899, 1929, 1899, 1859, 1859, 1899, 1899],
    "Anker Soundcore Liberty 4 NC": [549, 529, 509, 499, 499, 499, 509, 499, 499, 479, 499, 499],
    "SoundPEATS Air4 Pro 降噪耳机": [329, 309, 299, 299, 289, 299, 299, 289, 279, 299, 299, 299],
    "EarFun Air Pro 4 无线耳机": [499, 479, 459, 449, 449, 449, 459, 449, 429, 429, 449, 449],
}

MONTHS = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]


def get_mock_products(keyword: str):
    """根据关键词返回匹配的模拟商品列表。"""
    if keyword in MOCK_PRODUCTS:
        return MOCK_PRODUCTS[keyword]

    for category, products in MOCK_PRODUCTS.items():
        if keyword in category or category in keyword:
            return products

    matched = []
    for category, products in MOCK_PRODUCTS.items():
        for p in products:
            if keyword.lower() in p["name"].lower():
                matched.append(p)

    if matched:
        return matched

    all_products = []
    for products in MOCK_PRODUCTS.values():
        all_products.extend(products)
    random.shuffle(all_products)
    return all_products[:6]


def get_price_history(product_name: str):
    """获取某商品的历史价格模拟数据。"""
    if product_name in PRICE_HISTORY_BASE:
        return {"months": MONTHS, "prices": PRICE_HISTORY_BASE[product_name]}

    base_price = random.choice([199, 299, 399, 499, 599, 699, 899, 1299, 1599, 1999])
    prices = []
    current = base_price + random.randint(0, 200)
    for _ in range(12):
        variation = random.randint(-50, 50)
        current = max(int(current * 0.7), current + variation)
        if random.random() < 0.3:
            current = int(current * random.uniform(0.85, 1.0))
        prices.append(current)
    return {"months": MONTHS, "prices": prices}


def get_available_keywords():
    return list(MOCK_PRODUCTS.keys())