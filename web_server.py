"""Flask Web演示服务。"""

from flask import Flask, render_template, request, jsonify

from price_hunter.engine import create_engine
from price_hunter.cleaner import clean_products, filter_outliers, compute_cost_performance
from price_hunter.analyzer import ProductAnalyzer
from price_hunter.visualizer import generate_all_charts
from price_hunter.mock_data import get_available_keywords

import os


def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))

    @app.route("/")
    def index():
        keywords = get_available_keywords()
        return render_template("index.html", keywords=keywords)

    @app.route("/api/search")
    def api_search():
        keyword = request.args.get("keyword", "").strip()
        count = request.args.get("count", 20, type=int)
        use_mock = request.args.get("live", "0") != "1"

        if not keyword:
            return jsonify({"error": "请输入搜索关键词"}), 400

        engine = create_engine(use_mock=use_mock)
        raw = engine.search_amazon(keyword, max_items=count)

        if not raw:
            return jsonify({"error": "未找到匹配商品", "available_keywords": get_available_keywords()}), 404

        products = clean_products(raw)
        products = filter_outliers(products)
        products = compute_cost_performance(products)
        products = sorted(products, key=lambda p: p["price"])

        analyzer = ProductAnalyzer(products)
        rec = analyzer.generate_recommendations()

        charts = generate_all_charts(products, keyword)

        return jsonify({
            "keyword": keyword,
            "products": products,
            "statistics": rec["statistics"],
            "recommendations": rec,
            "charts": charts,
            "source": "mock" if use_mock else "live",
        })

    @app.route("/api/keywords")
    def api_keywords():
        return jsonify({"keywords": get_available_keywords()})

    @app.route("/api/demo")
    def api_demo():
        keyword = "无线耳机"
        engine = create_engine(use_mock=True)
        raw = engine.search_amazon(keyword, max_items=20)
        products = clean_products(raw)
        products = filter_outliers(products)
        products = compute_cost_performance(products)
        products = sorted(products, key=lambda p: p["price"])

        analyzer = ProductAnalyzer(products)
        rec = analyzer.generate_recommendations()
        charts = generate_all_charts(products, keyword)

        return jsonify({
            "keyword": keyword,
            "products": products,
            "statistics": rec["statistics"],
            "recommendations": rec,
            "charts": charts,
            "source": "mock",
            "is_demo": True,
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)