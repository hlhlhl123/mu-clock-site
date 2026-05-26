"""命令行工具入口。"""

import argparse
import json
import sys

from .engine import create_engine
from .cleaner import clean_products, filter_outliers, compute_cost_performance
from .analyzer import ProductAnalyzer
from .visualizer import generate_all_charts
from .mock_data import get_available_keywords


def format_table(products: list[dict]) -> str:
    """格式化为可读表格。"""
    lines = []
    header = f"{'序号':<5} {'商品名称':<40} {'价格':<10} {'评分':<6} {'销量':<8} {'性价比':<8} {'标签':<20}"
    lines.append(header)
    lines.append("-" * len(header))

    for i, p in enumerate(products, 1):
        name = p["name"][:37] + ".." if len(p["name"]) > 37 else p["name"]
        price_str = f"¥{p['price']:.2f}"
        rating_str = f"{p['rating']:.1f}"
        sales_str = f"{p['sales']:,}"
        cp_str = f"{p.get('cp_score', 0):.0f}分"
        labels = ", ".join(p.get("label", ["-"]))[:18]

        lines.append(f"{i:<5} {name:<40} {price_str:<10} {rating_str:<6} {sales_str:<8} {cp_str:<8} {labels:<20}")

    return "\n".join(lines)


def cmd_search(args):
    """搜索命令处理。"""
    keyword = args.keyword
    count = args.count
    use_mock = not args.live

    print(f"\n🔍 正在搜索: {keyword}")
    print(f"📡 数据源: {'Mock模拟数据' if use_mock else 'Amazon实时抓取'}")
    print(f"📊 期望数量: {count}\n")

    engine = create_engine(use_mock=use_mock)
    raw_products = engine.search_amazon(keyword, max_items=count)

    if not raw_products:
        print("⚠️  未找到匹配的商品。")
        print(f"\n💡 可用的关键词: {', '.join(get_available_keywords())}")
        return

    products = clean_products(raw_products)
    products = filter_outliers(products)
    products = compute_cost_performance(products)
    products = sorted(products, key=lambda p: p["price"])

    analyzer = ProductAnalyzer(products)
    rec = analyzer.generate_recommendations()

    print(format_table(products))
    print()

    stats = rec["statistics"]
    print("=" * 70)
    print("📈 品类统计概览")
    print(f"  商品总数: {stats['total_products']}")
    print(f"  价格区间: ¥{stats['price']['min']:.2f} ~ ¥{stats['price']['max']:.2f}")
    print(f"  均价: ¥{stats['price']['avg']:.2f}  |  中位数: ¥{stats['price']['median']:.2f}")
    print(f"  评分区间: {stats['rating']['min']:.1f} ~ {stats['rating']['max']:.1f}  |  均分: {stats['rating']['avg']:.1f}")
    print(f"  总销量: {stats['sales']['total']:,}")

    print()
    print("🏆 智能推荐")
    for insight in rec["insights"]:
        print(f"  • {insight}")

    if args.charts:
        print()
        print("📊 正在生成图表...")
        charts = generate_all_charts(products, keyword)
        for name, b64 in charts.items():
            out_path = f"{keyword}_{name}.png"
            with open(out_path, "wb") as f:
                import base64
                f.write(base64.b64decode(b64))
            print(f"  ✅ 已保存: {out_path}")

    if args.output:
        export_data = {"keyword": keyword, "products": products, "statistics": stats, "recommendations": rec["insights"]}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 数据已导出: {args.output}")


def cmd_list(args):
    """列出可用关键词。"""
    keywords = get_available_keywords()
    print("\n📋 可用搜索关键词:")
    for kw in keywords:
        print(f"  • {kw}")
    print()


def cmd_web(args):
    """启动Web演示服务。"""
    from web_server import create_app
    app = create_app()
    print(f"\n🌐 Web演示服务启动中...")
    print(f"   地址: http://127.0.0.1:{args.port}")
    print(f"   按 Ctrl+C 停止\n")
    app.run(host="0.0.0.0", port=args.port, debug=False)


def main():
    parser = argparse.ArgumentParser(
        prog="price-hunter",
        description="电商商品价格自动化采集与对比工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s search "无线耳机"              # 搜索无线耳机
  %(prog)s search "机械键盘" --live       # 尝试实时抓取
  %(prog)s search "显示器" -n 10 --charts # 搜索并生成图表
  %(prog)s search "移动电源" -o result.json # 导出JSON
  %(prog)s list                            # 列出可用关键词
  %(prog)s web                             # 启动Web演示
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    search_parser = subparsers.add_parser("search", help="搜索商品")
    search_parser.add_argument("keyword", help="搜索关键词")
    search_parser.add_argument("-n", "--count", type=int, default=20, help="最大采集数量 (默认: 20)")
    search_parser.add_argument("--live", action="store_true", help="启用实时抓取模式 (默认使用Mock)")
    search_parser.add_argument("--charts", action="store_true", help="生成并保存图表")
    search_parser.add_argument("-o", "--output", help="导出JSON结果文件路径")
    search_parser.set_defaults(func=cmd_search)

    list_parser = subparsers.add_parser("list", help="列出可用关键词")
    list_parser.set_defaults(func=cmd_list)

    web_parser = subparsers.add_parser("web", help="启动Web演示服务")
    web_parser.add_argument("-p", "--port", type=int, default=5000, help="监听端口 (默认: 5000)")
    web_parser.set_defaults(func=cmd_web)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()