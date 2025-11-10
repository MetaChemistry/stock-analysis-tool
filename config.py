"""
Stock Analysis Tool - Configuration File
All customizable settings are centralized here.
"""

# Stock Watchlist - Add or remove stocks as needed
WATCHLIST = [
    'AAPL',  # Apple Inc.
    'MSFT',  # Microsoft Corporation
    'GOOGL', # Alphabet Inc.
    'AMZN',  # Amazon.com Inc.
    'TSLA',  # Tesla Inc.
    'NVDA',  # NVIDIA Corporation
    'META',  # Meta Platforms Inc.
    'SPY',   # S&P 500 ETF
]

# Data Collection Settings
DATA_PERIOD = '2y'        # How much historical data to fetch (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
DATA_INTERVAL = '1d'      # Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
UPDATE_FREQUENCY = 3600   # Seconds between automatic updates (3600 = 1 hour)

# Database Settings
DATABASE_PATH = 'data/stocks.db'

# Technical Indicator Settings
SHORT_WINDOW = 20         # Short-term moving average
LONG_WINDOW = 50          # Long-term moving average
RSI_PERIOD = 14           # RSI calculation period
MACD_FAST = 12           # MACD fast EMA period
MACD_SLOW = 26           # MACD slow EMA period
MACD_SIGNAL = 9          # MACD signal line period
BOLLINGER_PERIOD = 20    # Bollinger Bands period
BOLLINGER_STD = 2        # Bollinger Bands standard deviation

# Signal Thresholds
RSI_OVERBOUGHT = 70      # RSI overbought threshold
RSI_OVERSOLD = 30        # RSI oversold threshold

# Dashboard Settings
CHART_HEIGHT = 600        # Chart height in pixels
CHART_THEME = 'plotly'    # Chart theme (plotly, plotly_white, plotly_dark)
DEFAULT_TIMEFRAME = '6mo' # Default chart timeframe

# API Keys (Optional - for future phases)
ALPHA_VANTAGE_API_KEY = None  # For alternative data source
ANTHROPIC_API_KEY = None      # For Claude AI sentiment analysis

# Logging Settings
LOG_LEVEL = 'INFO'        # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = 'data/stock_analysis.log'
