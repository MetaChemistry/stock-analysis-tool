# 📊 Stock Analysis Tool

A powerful, local-first stock analysis tool with technical indicators, interactive charts, and real-time data from Yahoo Finance.

## ✨ Features

- **Real-time Stock Data** - Fetch historical and current data from Yahoo Finance
- **Technical Indicators** - SMA, RSI, MACD, Bollinger Bands, and more
- **Interactive Dashboard** - Beautiful Streamlit web interface
- **Trading Signals** - Automated buy/sell/hold recommendations
- **Local Database** - All data stored locally in SQLite
- **Customizable** - Easy to configure watchlist and parameters

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Internet connection (for fetching stock data)

### Installation

1. **Extract the project** (if you received a .tar.gz file):
```bash
tar -xzf stock_analysis_project.tar.gz
cd stock_analysis_project
```

2. **Run the setup script**:
```bash
./setup.sh
```

3. **Launch the application**:
```bash
./run.sh
```

The dashboard will open in your browser at `http://localhost:8501`

## 📖 Usage

### Basic Workflow

1. **Initial Data Collection** - First run collects 2 years of historical data
2. **View Dashboard** - Explore stocks, charts, and indicators
3. **Update Data** - Click "Update Data" button to refresh
4. **Analyze Signals** - Review technical indicators and recommendations

### Customizing Your Watchlist

Edit `config.py` to add or remove stocks:

```python
WATCHLIST = [
    'AAPL',  # Apple Inc.
    'MSFT',  # Microsoft Corporation
    'GOOGL', # Alphabet Inc.
    # Add your stocks here
]
```

### Manual Data Collection

```bash
source venv/bin/activate
python src/data_collector.py
```

### Running the Dashboard

```bash
source venv/bin/activate
streamlit run dashboard.py
```

## 📊 Technical Indicators Explained

### Moving Averages (SMA)
- **SMA 20** - Short-term trend (20 days)
- **SMA 50** - Long-term trend (50 days)
- **Signal**: Price above SMA = Bullish, below = Bearish

### RSI (Relative Strength Index)
- Measures momentum on a 0-100 scale
- **Above 70** - Overbought (potential sell)
- **Below 30** - Oversold (potential buy)
- **50-70** - Bullish momentum
- **30-50** - Bearish momentum

### MACD (Moving Average Convergence Divergence)
- Shows relationship between two moving averages
- **MACD > Signal** - Bullish
- **MACD < Signal** - Bearish
- **Histogram** - Strength of trend

### Bollinger Bands
- Show volatility and potential price extremes
- **Price at Upper Band** - Overbought
- **Price at Lower Band** - Oversold
- **Bands Narrow** - Low volatility, potential breakout

## 🎯 Understanding Signals

### Overall Signal
The tool combines multiple indicators to generate an overall signal:

- **🟢 BUY** - Multiple bullish indicators align
- **🔴 SELL** - Multiple bearish indicators align
- **🟡 HOLD** - Mixed signals, wait for clarity

### Signal Weight
- Trend (Moving Averages): 2 points
- RSI: 1 point
- MACD: 1 point
- Bollinger Bands: 1 point

## 🛠️ Configuration

Edit `config.py` to customize:

```python
# Data Collection
DATA_PERIOD = '2y'        # Historical data range
DATA_INTERVAL = '1d'      # Data frequency

# Technical Indicators
SHORT_WINDOW = 20         # Short-term MA
LONG_WINDOW = 50          # Long-term MA
RSI_PERIOD = 14           # RSI calculation period

# Signal Thresholds
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
```

## 📁 Project Structure

```
stock_analysis_project/
├── config.py              # Configuration settings
├── dashboard.py           # Streamlit web interface
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup automation
├── run.sh                # Launch script
├── src/
│   ├── __init__.py
│   ├── database.py       # SQLite integration
│   ├── data_collector.py # Yahoo Finance API
│   └── analyzer.py       # Technical analysis
└── data/
    └── stocks.db         # SQLite database
```

## 🔧 Troubleshooting

### "No module named 'yfinance'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "No data available"
```bash
python src/data_collector.py
```

### Dashboard won't open
- Check if port 8501 is available
- Try: `streamlit run dashboard.py --server.port 8502`

### Data not updating
- Yahoo Finance may rate limit requests
- Wait a few minutes and try again
- Check your internet connection

## ⚠️ Important Disclaimers

- **Not Financial Advice** - This tool is for educational purposes only
- **No Guarantees** - Past performance doesn't predict future results
- **Do Your Research** - Always verify information independently
- **Risk Warning** - Trading stocks involves risk of loss

## 🎓 Learning Resources

### Technical Analysis
- [Investopedia - Technical Analysis](https://www.investopedia.com/technical-analysis-4689657)
- [Investopedia - RSI](https://www.investopedia.com/terms/r/rsi.asp)
- [Investopedia - MACD](https://www.investopedia.com/terms/m/macd.asp)

### Python & Data Science
- [Python Documentation](https://docs.python.org/3/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🚀 Future Enhancements

See `ROADMAP.md` for planned features:
- Machine Learning price prediction
- AI-powered sentiment analysis
- Advanced pattern recognition
- Cloud deployment
- Mobile app

## 📄 License

This project is for educational purposes. Use at your own risk.

## 🤝 Contributing

This is a personal project, but feel free to fork and customize!

## 📧 Support

For issues or questions:
1. Check the FAQ.md file
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify your Python version (3.8+)

## 🌟 Features Highlight

### What Makes This Tool Special?

✅ **Local-First** - All data stored on your machine  
✅ **Free** - Uses free Yahoo Finance API  
✅ **Fast** - Optimized database queries  
✅ **Beautiful** - Modern, interactive UI  
✅ **Extensible** - Easy to add new indicators  
✅ **Educational** - Learn technical analysis  

## 📊 Example Screenshots

### Dashboard Overview
- Real-time price updates
- Multiple technical indicators
- Interactive charts with zoom/pan
- Clear buy/sell/hold signals

### Supported Stocks
- US stocks (NYSE, NASDAQ)
- ETFs (SPY, QQQ, etc.)
- Major indices
- Cryptocurrencies (BTC-USD, ETH-USD)

## 🎯 Best Practices

1. **Update Regularly** - Keep data fresh for accurate signals
2. **Multiple Timeframes** - Check different time ranges
3. **Confirm Signals** - Don't rely on one indicator
4. **Paper Trade** - Test strategies before real money
5. **Risk Management** - Never invest more than you can lose

## 💡 Tips for Success

- **Trend is Your Friend** - Trade with the trend, not against it
- **Wait for Confirmation** - Multiple indicators should align
- **Set Stop Losses** - Protect your capital
- **Stay Disciplined** - Follow your strategy
- **Keep Learning** - Markets always evolve

---

**Happy Trading! 📈**

Remember: This is a tool to assist your analysis, not a crystal ball. Always do your own research and never invest money you can't afford to lose.
