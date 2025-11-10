# 🚀 QUICKSTART GUIDE

## Get Started in 3 Steps

### Step 1: Setup (One-time)
```bash
cd stock_analysis_project
./setup.sh
```
Wait for dependencies to install (~2 minutes)

### Step 2: Launch
```bash
./run.sh
```
This will:
- Collect stock data from Yahoo Finance
- Launch the dashboard in your browser

### Step 3: Explore
- Browse stocks in the sidebar
- View interactive charts
- Check technical indicators
- See buy/sell/hold signals

## 📱 What You'll See

### Dashboard Features
- **Current Price** with daily change
- **Trend Direction** (uptrend/downtrend)
- **RSI Indicator** (overbought/oversold)
- **MACD Momentum** (bullish/bearish)
- **Overall Signal** (BUY/SELL/HOLD)

### Interactive Charts
- **Candlestick Price Chart** with zoom/pan
- **Moving Averages** (20-day and 50-day)
- **Bollinger Bands** for volatility
- **MACD Chart** for momentum
- **RSI Chart** for strength

## ⚙️ Quick Customization

### Add Your Favorite Stocks
Edit `config.py`:
```python
WATCHLIST = [
    'AAPL',   # Your stocks here
    'TSLA',
    'AMD',
]
```

### Update Data
Click the "Update Data" button in the sidebar, or run:
```bash
source venv/bin/activate
python src/data_collector.py
```

## 💡 Pro Tips

1. **First Launch** - Initial data collection takes 1-2 minutes
2. **Multiple Timeframes** - Switch between 1mo, 3mo, 6mo, 1y, 2y
3. **Refresh Data** - Update daily for accurate signals
4. **Multiple Stocks** - Compare different stocks easily

## 🆘 Common Issues

**"Command not found: streamlit"**
```bash
source venv/bin/activate
./run.sh
```

**"No data available"**
```bash
python src/data_collector.py
```

**Dashboard port already in use**
```bash
streamlit run dashboard.py --server.port 8502
```

## 📚 Learn More

- `README.md` - Full documentation
- `ARCHITECTURE.md` - System design details
- `config.py` - All customization options

---

**Ready? Run `./run.sh` and start analyzing! 📊**
