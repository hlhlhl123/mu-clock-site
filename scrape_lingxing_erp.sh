#!/bin/bash

# 灵星ERP实时销量和销售额抓取脚本
# 使用方法：
# 1. 确保已安装 agent-browser: npm i -g agent-browser
# 2. 确保已安装 Chrome: agent-browser install
# 3. 在已登录灵星ERP的浏览器中运行此脚本

set -e

echo "=== 灵星ERP 实时数据抓取 ==="
echo ""

# 检查 agent-browser 是否已安装
if ! command -v agent-browser &> /dev/null; then
    echo "错误: 未找到 agent-browser，请先运行: npm i -g agent-browser"
    exit 1
fi

# 检查 Chrome 是否已安装
if ! agent-browser install --dry-run 2>&1 | grep -q "is already installed"; then
    echo "警告: Chrome 未安装，正在安装..."
    agent-browser install
fi

# 导入当前浏览器会话的认证状态
echo "步骤 1: 导入浏览器认证状态..."
agent-browser --auto-connect state save ./lingxing_auth.json

# 打开灵星ERP首页
echo "步骤 2: 访问灵星ERP首页..."
agent-browser state load ./lingxing_auth.json

# 导航到首页
agent-browser open https://erp.lingxing.com/erp/home

# 等待页面加载完成
echo "步骤 3: 等待页面加载..."
agent-browser wait --load networkidle

# 获取页面快照以查看元素
echo "步骤 4: 获取页面数据..."
agent-browser snapshot -i > page_snapshot.txt 2>&1

# 尝试提取销量和销售额数据
echo "步骤 5: 提取实时销量和销售额数据..."
echo ""

# 使用 JavaScript 提取页面中的关键数据
agent-browser eval --stdin <<'EVALEOF'
// 查找包含销量和销售额的元素
const data = {};

// 尝试查找常见的销量/销售额相关元素
const allElements = document.querySelectorAll('div, span, p, h1, h2, h3, h4, td, th');

allElements.forEach(el => {
  const text = el.textContent.trim();
  
  // 查找销量相关文本
  if (text.match(/销量|销售量|已售|订单/i) && text.match(/\d/)) {
    if (!data.sales_volume) {
      data.sales_volume = text;
    }
  }
  
  // 查找销售额相关文本
  if (text.match(/销售额|营收|GMV|收入/i) && text.match(/\d/)) {
    if (!data.sales_amount) {
      data.sales_amount = text;
    }
  }
  
  // 查找实时数据
  if (text.match(/实时|今日|今天/i) && text.match(/\d/)) {
    if (!data.realtime) {
      data.realtime = text;
    }
  }
});

// 也尝试查找包含数字的卡片/面板
const cards = document.querySelectorAll('.card, .panel, .stat, .metric, [class*="stat"], [class*="metric"], [class*="data"]');
cards.forEach(card => {
  const title = card.querySelector('h3, h4, .title, .label, [class*="title"], [class*="label"]');
  const value = card.querySelector('.value, .number, .amount, [class*="value"], [class*="number"]');
  
  if (title && value) {
    const titleText = title.textContent.trim();
    const valueText = value.textContent.trim();
    
    if (titleText.match(/销量/i)) {
      data['sales_volume_card'] = { title: titleText, value: valueText };
    }
    if (titleText.match(/销售额/i)) {
      data['sales_amount_card'] = { title: titleText, value: valueText };
    }
  }
});

// 输出找到的数据
console.log(JSON.stringify(data, null, 2));

// 如果没找到结构化数据，输出整个页面的文本内容供分析
if (Object.keys(data).length === 0) {
  console.log("\n=== 页面文本内容（前5000字符）===");
  console.log(document.body.innerText.substring(0, 5000));
}
EVALEOF

echo ""
echo "=== 数据提取完成 ==="
echo ""
echo "如需查看详细页面内容，可以运行:"
echo "  agent-browser screenshot lingxing_homepage.png"
echo ""
echo "清理临时文件:"
echo "  rm -f lingxing_auth.json page_snapshot.txt"
