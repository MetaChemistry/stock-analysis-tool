#!/bin/bash

echo "========================================"
echo "Stock Analysis Tool - Launch Script"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if database exists
if [ ! -f "data/stocks.db" ]; then
    echo "📊 No data found. Collecting stock data..."
    echo ""
    python src/data_collector.py
    echo ""
fi

# Launch dashboard
echo "🚀 Launching Stock Analysis Dashboard..."
echo ""
echo "💡 Dashboard will open in your browser at http://localhost:8501"
echo "💡 Press Ctrl+C to stop the dashboard"
echo ""

streamlit run dashboard.py
