"""统一入口 — CLI工具 与 Web服务。"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from price_hunter.cli import main
    main()