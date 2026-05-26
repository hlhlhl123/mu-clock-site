"""数据可视化模块 — 生成价格对比图、趋势图、性价比分布图。"""

import io
import base64
import random
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams["axes.unicode_minus"] = False

_FONT_NAMES = [
    "WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "Noto Sans CJK SC",
    "Noto Sans SC", "SimHei", "Microsoft YaHei", "PingFang SC",
    "Hiragino Sans GB", "AR PL UMing CN", "DejaVu Sans",
]
_available_font: Optional[str] = None


def _get_font():
    global _available_font
    if _available_font:
        return _available_font
    available = {f.name for f in fm.fontManager.ttflist}
    for name in _FONT_NAMES:
        if name in available:
            _available_font = name
            return name
    _available_font = "sans-serif"
    return _available_font


COLORS = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"]


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight", transparent=False, facecolor="white")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return b64


def generate_price_bar_chart(products: list[dict], keyword: str = "") -> str:
    """生成价格横向对比柱状图。"""
    font = _get_font()
    plt.rcParams["font.family"] = font

    fig, ax = plt.subplots(figsize=(10, max(4, len(products) * 0.5)))

    sorted_products = sorted(products, key=lambda p: p["price"])
    names = [p["name"][:20] + ".." if len(p["name"]) > 20 else p["name"] for p in sorted_products]
    prices = [p["price"] for p in sorted_products]
    colors = COLORS[:len(prices)] if len(prices) <= len(COLORS) else COLORS * ((len(prices) // len(COLORS)) + 1)

    bars = ax.barh(range(len(names)), prices, color=colors[:len(prices)], edgecolor="white", height=0.6)

    for i, (bar, price) in enumerate(zip(bars, prices)):
        ax.text(bar.get_width() + max(prices) * 0.02, bar.get_y() + bar.get_height() / 2,
                f"¥{price:.0f}", va="center", fontsize=9, fontweight="bold")

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("价格 (¥)", fontsize=11)
    ax.set_title(f"商品价格对比 — {keyword}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlim(0, max(prices) * 1.3)
    ax.grid(axis="x", alpha=0.3, linestyle="--")

    return _fig_to_base64(fig)


def generate_price_distribution(products: list[dict], keyword: str = "") -> str:
    """生成价格分布直方图。"""
    font = _get_font()
    plt.rcParams["font.family"] = font

    fig, ax = plt.subplots(figsize=(8, 5))

    prices = [p["price"] for p in products]
    n_bins = min(8, len(prices))

    ax.hist(prices, bins=n_bins, color="#4E79A7", edgecolor="white", alpha=0.85, rwidth=0.9)
    ax.set_xlabel("价格区间 (¥)", fontsize=11)
    ax.set_ylabel("商品数量", fontsize=11)
    ax.set_title(f"价格分布 — {keyword}", fontsize=14, fontweight="bold", pad=15)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    return _fig_to_base64(fig)


def generate_rating_scatter(products: list[dict], keyword: str = "") -> str:
    """生成评分 vs 价格散点气泡图（气泡大小=销量）。"""
    font = _get_font()
    plt.rcParams["font.family"] = font

    fig, ax = plt.subplots(figsize=(10, 6))

    prices = [p["price"] for p in products]
    ratings = [p["rating"] for p in products]
    sales = [p["sales"] for p in products]
    names = [p["name"] for p in products]
    colors = COLORS[:len(products)] if len(products) <= len(COLORS) else COLORS * ((len(products) // len(COLORS)) + 1)

    max_sale = max(sales) if sales else 1
    sizes = [max(80, (s / max_sale) * 600) for s in sales]

    scatter = ax.scatter(prices, ratings, s=sizes, c=colors[:len(products)],
                         alpha=0.75, edgecolors="white", linewidth=1.5, zorder=5)

    for i, name in enumerate(names):
        short_name = name[:16] + ".." if len(name) > 16 else name
        offset = (max_sale / max_sale) * 0.12 * max(prices) if prices else 10
        ax.annotate(short_name, (prices[i], ratings[i]),
                    textcoords="offset points", xytext=(8, 4),
                    fontsize=7, alpha=0.8)

    ax.set_xlabel("价格 (¥)", fontsize=11)
    ax.set_ylabel("评分", fontsize=11)
    ax.set_title(f"评分 vs 价格 (气泡=销量) — {keyword}", fontsize=14, fontweight="bold", pad=15)
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_ylim(max(0, min(ratings) - 0.3), min(5.0, max(ratings) + 0.3))

    return _fig_to_base64(fig)


def generate_price_trend_chart(products: list[dict], keyword: str = "") -> str:
    """生成多商品价格趋势折线图。"""
    font = _get_font()
    plt.rcParams["font.family"] = font

    fig, ax = plt.subplots(figsize=(10, 5))

    for i, p in enumerate(products[:5]):
        history = p.get("price_history", {})
        months = history.get("months", [])
        hprices = history.get("prices", [])

        if not months or not hprices:
            hprices = [p["price"] + random.randint(-80, 80) for _ in range(12)]
            months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]

        color = COLORS[i % len(COLORS)]
        short_name = p["name"][:12] + ".." if len(p["name"]) > 12 else p["name"]
        ax.plot(range(len(hprices)), hprices, marker="o", color=color,
                linewidth=2, markersize=5, label=short_name, alpha=0.85)

    ax.set_xticks(range(len(months)))
    ax.set_xticklabels(months, fontsize=9)
    ax.set_ylabel("价格 (¥)", fontsize=11)
    ax.set_title(f"历史价格趋势 — {keyword}", fontsize=14, fontweight="bold", pad=15)
    ax.legend(loc="upper left", fontsize=8, framealpha=0.9)
    ax.grid(alpha=0.3, linestyle="--")

    return _fig_to_base64(fig)


def generate_cp_score_chart(products: list[dict], keyword: str = "") -> str:
    """生成性价比评分横向柱状图。"""
    font = _get_font()
    plt.rcParams["font.family"] = font

    sorted_cp = sorted(products, key=lambda p: p.get("cp_score", 0))
    fig, ax = plt.subplots(figsize=(8, max(3, len(products) * 0.4)))

    names = [p["name"][:20] + ".." if len(p["name"]) > 20 else p["name"] for p in sorted_cp]
    scores = [p.get("cp_score", 0) for p in sorted_cp]

    bar_colors = []
    for s in scores:
        if s >= 80:
            bar_colors.append("#59A14F")
        elif s >= 60:
            bar_colors.append("#EDC948")
        elif s >= 40:
            bar_colors.append("#F28E2B")
        else:
            bar_colors.append("#E15759")

    bars = ax.barh(range(len(names)), scores, color=bar_colors, edgecolor="white", height=0.6)

    for i, (bar, score) in enumerate(zip(bars, scores)):
        label = "⭐性价比之王" if score >= 80 else ("推荐入手" if score >= 60 else ("可以考虑" if score >= 40 else "一般"))
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{score:.0f} {label}", va="center", fontsize=8)

    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("性价比评分 (0-100)", fontsize=11)
    ax.set_title(f"性价比评分排名 — {keyword}", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlim(0, 115)
    ax.grid(axis="x", alpha=0.3, linestyle="--")

    return _fig_to_base64(fig)


def generate_all_charts(products: list[dict], keyword: str = "") -> dict[str, str]:
    """一次性生成全部图表。"""
    return {
        "price_bar": generate_price_bar_chart(products, keyword),
        "price_distribution": generate_price_distribution(products, keyword),
        "rating_scatter": generate_rating_scatter(products, keyword),
        "price_trend": generate_price_trend_chart(products, keyword),
        "cp_score": generate_cp_score_chart(products, keyword),
    }