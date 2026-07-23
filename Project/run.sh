#!/bin/bash
# 价值投资分析工具启动脚本

echo "🚀 启动价值投资分析工具..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.9 或更高版本"
    exit 1
fi

# 检查是否安装了依赖
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 正在安装依赖包..."
    pip3 install -r requirements.txt
    echo ""
fi

# 启动Streamlit应用
echo "✅ 启动应用..."
echo "浏览器将自动打开 http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止应用"
echo ""

cd "$(dirname "$0")"
python3 -m streamlit run dashboard/app_enhanced.py
