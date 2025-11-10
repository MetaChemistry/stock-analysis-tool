# Stock Analysis Project - Setup Guide

## Project Structure
```
stock_analysis/
├── data/                   # Raw and processed data
├── models/                 # Trained ML models
├── notebooks/              # Jupyter notebooks for exploration
├── src/
│   ├── data_collector.py   # Fetch stock data
│   ├── analyzer.py         # Technical analysis
│   ├── predictor.py        # ML predictions
│   └── database.py         # Database operations
├── dashboard.py            # Streamlit dashboard
├── requirements.txt        # Python dependencies
└── .env                    # API keys (create this)
```

## Installation Steps

### 1. Open Terminal and Create Project Directory
```bash
cd ~/Desktop  # or wherever you want the project
mkdir stock_analysis
cd stock_analysis
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Activate virtual environment
```

### 3. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 4. Create Directories
```bash
mkdir data models notebooks src
```

### 5. Test Installation
```bash
python3 -c "import yfinance as yf; print('Setup successful!')"
```

## Quick Start

After setup, run the data collector:
```bash
python3 src/data_collector.py
```

Launch the dashboard:
```bash
streamlit run dashboard.py
```

## Next Steps
1. Configure your stock watchlist in `config.py`
2. Run data collection to fetch historical data
3. Explore the dashboard to see trends
4. Train your first ML model

## Troubleshooting

**If you get SSL errors with yfinance:**
```bash
pip3 install --upgrade yfinance requests
```

**If Streamlit won't start:**
```bash
pip3 install --upgrade streamlit
```

## Free Data Sources We're Using
- **yfinance**: Historical OHLCV data, company info
- **Alpha Vantage** (optional): More detailed data with free API key

## What We're Building (MVP)
✅ Automated data collection for your watchlist
✅ Technical indicators (SMA, RSI, MACD, Bollinger Bands)
✅ Price trend analysis
✅ Interactive dashboard with charts
✅ SQLite database for historical storage
✅ Basic ML model for pattern recognition

Later we'll add:
- Claude API for sentiment analysis
- More advanced ML models
- Real-time alerts
- Portfolio tracking
