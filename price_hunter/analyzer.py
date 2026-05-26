"""商品对比分析模块 — 排序、横向对比、性价比推荐。"""

import statistics
from typing import Any


class ProductAnalyzer:
    """商品分析器: 排序、统计汇总、推荐标注。"""

    def __init__(self, products: list[dict]):
        self.products = products

    def sort_by_price(self, ascending: bool = True) -> list[dict]:
        return sorted(self.products, key=lambda p: p["price"], reverse=not ascending)

    def sort_by_rating(self, ascending: bool = False) -> list[dict]:
        return sorted(self.products, key=lambda p: p["rating"], reverse=not ascending)

    def sort_by_sales(self, ascending: bool = False) -> list[dict]:
        return sorted(self.products, key=lambda p: p["sales"], reverse=not ascending)

    def sort_by_cp_score(self, ascending: bool = False) -> list[dict]:
        return sorted(self.products, key=lambda p: p.get("cp_score", 0), reverse=not ascending)

    def get_statistics(self) -> dict[str, Any]:
        prices = [p["price"] for p in self.products]
        ratings = [p["rating"] for p in self.products]
        sales = [p["sales"] for p in self.products]

        return {
            "total_products": len(self.products),
            "price": {
                "min": min(prices) if prices else 0,
                "max": max(prices) if prices else 0,
                "avg": round(statistics.mean(prices), 2) if prices else 0,
                "median": round(statistics.median(prices), 2) if prices else 0,
                "range": max(prices) - min(prices) if prices else 0,
            },
            "rating": {
                "min": min(ratings) if ratings else 0,
                "max": max(ratings) if ratings else 0,
                "avg": round(statistics.mean(ratings), 2) if ratings else 0,
            },
            "sales": {
                "total": sum(sales),
                "avg": int(statistics.mean(sales)) if sales else 0,
            },
        }

    def compare_products(self) -> list[dict]:
        """生成横向对比数据，包含性价比标注。"""
        if not self.products:
            return []

        stats = self.get_statistics()
        avg_price = stats["price"]["avg"]
        avg_rating = stats["rating"]["avg"]
        avg_sales = stats["sales"]["avg"]

        compared = []
        for p in self.products:
            item = p.copy()

            item["label"] = []
            if p["price"] <= avg_price * 0.7:
                item["label"].append("低价优选")
            if p["rating"] >= avg_rating * 1.1:
                item["label"].append("高评分")
            if p["sales"] >= avg_sales * 1.5:
                item["label"].append("热销爆款")

            cp_score = p.get("cp_score", 0)
            if cp_score >= 80:
                item["label"].append("⭐ 性价比之王")
            elif cp_score >= 60:
                item["label"].append("推荐入手")
            elif cp_score >= 40:
                item["label"].append("可以考虑")

            if not item["label"]:
                item["label"].append("一般")

            item["price_vs_avg"] = round((p["price"] - avg_price) / avg_price * 100, 1) if avg_price else 0
            item["rating_vs_avg"] = round((p["rating"] - avg_rating) / avg_rating * 100, 1) if avg_rating else 0

            compared.append(item)

        return compared

    def generate_recommendations(self) -> dict:
        """生成智能推荐报告。"""
        compared = self.compare_products()
        stats = self.get_statistics()

        top3_cp = self.sort_by_cp_score()[:3]
        best_value = top3_cp[0] if top3_cp else None
        cheapest = self.sort_by_price(ascending=True)[0] if self.products else None
        highest_rated = self.sort_by_rating()[:3]
        bestsellers = self.sort_by_sales()[:3]

        insights = []
        if stats["price"]["range"] > stats["price"]["avg"]:
            insights.append("该品类价格跨度较大，建议根据预算和需求选择合适档位。")
        if stats["rating"]["avg"] >= 4.5:
            insights.append("该品类整体评分较高，产品质量普遍有保障。")
        if stats["rating"]["avg"] < 4.0:
            insights.append("该品类评分分化明显，选购时请仔细甄别。")
        if best_value:
            cp_score = best_value.get("cp_score", 0)
            if cp_score >= 80:
                insights.append(f"强烈推荐 [{best_value['name']}] — 性价比评分 {cp_score} 分，综合表现突出。")

        return {
            "statistics": stats,
            "top_by_cp_score": top3_cp,
            "best_value": best_value,
            "cheapest": cheapest,
            "highest_rated": highest_rated,
            "bestsellers": bestsellers,
            "insights": insights,
            "all_compared": compared,
        }