"""
Stock ticker to company name mapping
Maps stock symbols to their full company names for search functionality
"""

STOCK_NAMES = {
    # Technology
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corporation',
    'NVDA': 'NVIDIA Corporation',
    'GOOGL': 'Alphabet Inc.',
    'GOOG': 'Alphabet Inc.',
    'META': 'Meta Platforms Inc.',
    'TSLA': 'Tesla Inc.',
    'AVGO': 'Broadcom Inc.',
    'ORCL': 'Oracle Corporation',
    'ADBE': 'Adobe Inc.',
    'CRM': 'Salesforce Inc.',
    'ACN': 'Accenture plc',
    'CSCO': 'Cisco Systems Inc.',
    'AMD': 'Advanced Micro Devices Inc.',
    'IBM': 'International Business Machines',
    'INTC': 'Intel Corporation',
    'NOW': 'ServiceNow Inc.',
    'TXN': 'Texas Instruments',
    'QCOM': 'Qualcomm Inc.',
    'INTU': 'Intuit Inc.',
    'AMAT': 'Applied Materials Inc.',
    
    # Financial Services
    'BRK.B': 'Berkshire Hathaway Inc.',
    'JPM': 'JPMorgan Chase & Co.',
    'V': 'Visa Inc.',
    'MA': 'Mastercard Inc.',
    'BAC': 'Bank of America Corp',
    'WFC': 'Wells Fargo & Company',
    'MS': 'Morgan Stanley',
    'GS': 'Goldman Sachs Group Inc.',
    'SPGI': 'S&P Global Inc.',
    'BLK': 'BlackRock Inc.',
    'C': 'Citigroup Inc.',
    'SCHW': 'Charles Schwab Corporation',
    'AXP': 'American Express Company',
    'PGR': 'Progressive Corporation',
    'CB': 'Chubb Limited',
    'MMC': 'Marsh & McLennan',
    
    # Healthcare
    'UNH': 'UnitedHealth Group',
    'LLY': 'Eli Lilly and Company',
    'JNJ': 'Johnson & Johnson',
    'ABBV': 'AbbVie Inc.',
    'MRK': 'Merck & Co. Inc.',
    'TMO': 'Thermo Fisher Scientific',
    'ABT': 'Abbott Laboratories',
    'DHR': 'Danaher Corporation',
    'PFE': 'Pfizer Inc.',
    'BMY': 'Bristol-Myers Squibb',
    'AMGN': 'Amgen Inc.',
    'GILD': 'Gilead Sciences Inc.',
    'CVS': 'CVS Health Corporation',
    'CI': 'Cigna Corporation',
    'VRTX': 'Vertex Pharmaceuticals',
    'ISRG': 'Intuitive Surgical Inc.',
    'REGN': 'Regeneron Pharmaceuticals',
    
    # Consumer Discretionary
    'AMZN': 'Amazon.com Inc.',
    'HD': 'Home Depot Inc.',
    'MCD': "McDonald's Corporation",
    'NKE': 'Nike Inc.',
    'LOW': "Lowe's Companies Inc.",
    'SBUX': 'Starbucks Corporation',
    'TJX': 'TJX Companies Inc.',
    'BKNG': 'Booking Holdings Inc.',
    'CMG': 'Chipotle Mexican Grill',
    'MAR': 'Marriott International',
    'GM': 'General Motors Company',
    'F': 'Ford Motor Company',
    
    # Communication Services
    'NFLX': 'Netflix Inc.',
    'DIS': 'Walt Disney Company',
    'CMCSA': 'Comcast Corporation',
    'T': 'AT&T Inc.',
    'VZ': 'Verizon Communications',
    'TMUS': 'T-Mobile US Inc.',
    
    # Industrials
    'BA': 'Boeing Company',
    'UNP': 'Union Pacific Corporation',
    'HON': 'Honeywell International',
    'UPS': 'United Parcel Service',
    'RTX': 'RTX Corporation',
    'CAT': 'Caterpillar Inc.',
    'GE': 'General Electric Company',
    'LMT': 'Lockheed Martin Corporation',
    'DE': 'Deere & Company',
    'MMM': '3M Company',
    
    # Consumer Staples
    'WMT': 'Walmart Inc.',
    'PG': 'Procter & Gamble Company',
    'COST': 'Costco Wholesale Corporation',
    'KO': 'Coca-Cola Company',
    'PEP': 'PepsiCo Inc.',
    'PM': 'Philip Morris International',
    'MO': 'Altria Group Inc.',
    'MDLZ': 'Mondelez International',
    
    # Energy
    'XOM': 'Exxon Mobil Corporation',
    'CVX': 'Chevron Corporation',
    'COP': 'ConocoPhillips',
    'SLB': 'Schlumberger Limited',
    'EOG': 'EOG Resources Inc.',
    
    # Real Estate
    'PLD': 'Prologis Inc.',
    'AMT': 'American Tower Corporation',
    
    # Materials
    'LIN': 'Linde plc',
    
    # Utilities
    'NEE': 'NextEra Energy Inc.',
    'SO': 'Southern Company',
    'DUK': 'Duke Energy Corporation',
    
    # ETFs
    'SPY': 'SPDR S&P 500 ETF Trust',
    'QQQ': 'Invesco QQQ Trust',
    'DIA': 'SPDR Dow Jones Industrial Average ETF',
}

def get_stock_display_name(ticker):
    """Get display name for a ticker (Ticker - Company Name)"""
    company_name = STOCK_NAMES.get(ticker, ticker)
    return f"{ticker} - {company_name}"

def search_stocks(query, available_tickers):
    """
    Search stocks by ticker or company name
    Returns list of matching tickers
    """
    if not query:
        return available_tickers
    
    query = query.upper().strip()
    matches = []
    
    for ticker in available_tickers:
        company_name = STOCK_NAMES.get(ticker, '').upper()
        ticker_upper = ticker.upper()
        
        # Match by ticker or company name
        if query in ticker_upper or query in company_name:
            matches.append(ticker)
    
    return matches if matches else available_tickers
