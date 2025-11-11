"""
S&P 500 Stock Tickers
Complete list of S&P 500 companies (as of 2024)
"""

SP500_TICKERS = [
    # Technology
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'GOOG', 'META', 'TSLA', 'AVGO', 'ORCL', 'ADBE',
    'CRM', 'ACN', 'CSCO', 'AMD', 'IBM', 'INTC', 'NOW', 'TXN', 'QCOM', 'INTU',
    'AMAT', 'ADI', 'MU', 'LRCX', 'KLAC', 'SNPS', 'CDNS', 'MCHP', 'FTNT', 'PANW',
    
    # Financial Services
    'BRK.B', 'JPM', 'V', 'MA', 'BAC', 'WFC', 'MS', 'GS', 'SPGI', 'BLK',
    'C', 'SCHW', 'AXP', 'PGR', 'CB', 'MMC', 'ICE', 'AON', 'TFC', 'USB',
    'PNC', 'COF', 'CME', 'AIG', 'ALL', 'MET', 'PRU', 'AFL', 'TRV', 'AJG',
    
    # Healthcare
    'UNH', 'LLY', 'JNJ', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'PFE', 'BMY',
    'AMGN', 'GILD', 'CVS', 'CI', 'ELV', 'REGN', 'VRTX', 'HUM', 'ISRG', 'BSX',
    'SYK', 'ZTS', 'MDT', 'BIIB', 'EW', 'IDXX', 'HCA', 'A', 'IQV', 'RMD',
    
    # Consumer Discretionary
    'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'TJX', 'BKNG', 'ABNB',
    'CMG', 'ORLY', 'MAR', 'GM', 'F', 'DHI', 'YUM', 'ROST', 'AZO', 'LEN',
    'HLT', 'GPC', 'DG', 'APTV', 'EBAY', 'TSCO', 'ULTA', 'POOL', 'TPR', 'RL',
    
    # Communication Services
    'GOOGL', 'GOOG', 'META', 'NFLX', 'DIS', 'CMCSA', 'T', 'VZ', 'TMUS', 'CHTR',
    'EA', 'TTWO', 'OMC', 'IPG', 'PARA', 'MTCH', 'FOXA', 'FOX', 'NWSA', 'NWS',
    
    # Industrials  
    'BA', 'UNP', 'HON', 'UPS', 'RTX', 'CAT', 'GE', 'LMT', 'DE', 'MMM',
    'GD', 'NOC', 'ETN', 'ITW', 'PH', 'WM', 'EMR', 'CSX', 'NSC', 'FDX',
    'CARR', 'PCAR', 'JCI', 'TDG', 'ROK', 'OTIS', 'CTAS', 'SWK', 'FAST', 'VRSK',
    
    # Consumer Staples
    'WMT', 'PG', 'COST', 'KO', 'PEP', 'PM', 'MO', 'MDLZ', 'CL', 'ADM',
    'GIS', 'KMB', 'SYY', 'HSY', 'K', 'CHD', 'CLX', 'MKC', 'TSN', 'HRL',
    'CPB', 'CAG', 'SJM', 'LW', 'TAP', 'BG', 'MNST', 'KDP', 'KHC', 'EL',
    
    # Energy
    'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'WMB',
    'KMI', 'HES', 'HAL', 'DVN', 'FANG', 'BKR', 'TRGP', 'EQT', 'OKE', 'CTRA',
    
    # Real Estate
    'PLD', 'AMT', 'CCI', 'EQIX', 'PSA', 'SPG', 'O', 'WELL', 'DLR', 'VICI',
    'AVB', 'EQR', 'SBAC', 'INVH', 'ARE', 'MAA', 'ESS', 'VTR', 'EXR', 'PEAK',
    
    # Materials
    'LIN', 'APD', 'SHW', 'FCX', 'ECL', 'NEM', 'CTVA', 'DOW', 'DD', 'PPG',
    'NUE', 'ALB', 'BALL', 'AVY', 'AMCR', 'PKG', 'IP', 'CE', 'VMC', 'MLM',
    
    # Utilities
    'NEE', 'SO', 'DUK', 'CEG', 'SRE', 'AEP', 'VST', 'D', 'PEG', 'EXC',
    'XEL', 'ED', 'ETR', 'WEC', 'AWK', 'DTE', 'ES', 'FE', 'PPL', 'AEE',
    
    # Additional Major Companies
    'NFLX', 'PYPL', 'SHOP', 'SQ', 'ADSK', 'WDAY', 'TEAM', 'DDOG', 'ZM', 'SNOW',
    'ROKU', 'SPOT', 'UBER', 'LYFT', 'ABNB', 'DASH', 'COIN', 'PLTR', 'RBLX', 'U',
]

# Remove duplicates and sort
SP500_TICKERS = sorted(list(set(SP500_TICKERS)))

# Top 100 by market cap (for faster initial data collection)
TOP_100_TICKERS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK.B', 'LLY', 'V',
    'UNH', 'XOM', 'JPM', 'JNJ', 'WMT', 'MA', 'PG', 'AVGO', 'HD', 'CVX',
    'ABBV', 'MRK', 'COST', 'ORCL', 'KO', 'PEP', 'ADBE', 'BAC', 'CRM', 'NFLX',
    'MCD', 'ACN', 'CSCO', 'TMO', 'AMD', 'NKE', 'LIN', 'ABT', 'CMCSA', 'DHR',
    'DIS', 'TXN', 'VZ', 'INTC', 'PM', 'WFC', 'NEE', 'QCOM', 'INTU', 'COP',
    'IBM', 'RTX', 'UNP', 'AMGN', 'T', 'SPGI', 'LOW', 'HON', 'CAT', 'PFE',
    'AMAT', 'GE', 'SBUX', 'BA', 'BKNG', 'MS', 'GS', 'BLK', 'ELV', 'SYK',
    'AXP', 'DE', 'MDT', 'LMT', 'BMY', 'GILD', 'ADI', 'MMC', 'VRTX', 'TJX',
    'PLD', 'ISRG', 'AMT', 'CI', 'TMUS', 'C', 'CB', 'SLB', 'REGN', 'SCHW',
    'MO', 'ZTS', 'PGR', 'EOG', 'DUK', 'SO', 'CVS', 'BSX', 'BDX', 'ITW',
]
