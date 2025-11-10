"""
Database Module - SQLite integration for stock data storage
"""

import sqlite3
import pandas as pd
from datetime import datetime
import os


class StockDatabase:
    """Handles all database operations for stock data"""
    
    def __init__(self, db_path='data/stocks.db'):
        """Initialize database connection"""
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.conn = None
        self.create_tables()
    
    def get_connection(self):
        """Get or create database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        return self.conn
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Stock prices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(ticker, date)
            )
        ''')
        
        # Stock information table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_info (
                ticker TEXT PRIMARY KEY,
                company_name TEXT,
                sector TEXT,
                industry TEXT,
                market_cap REAL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Technical indicators table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                date TEXT NOT NULL,
                sma_20 REAL,
                sma_50 REAL,
                rsi REAL,
                macd REAL,
                macd_signal REAL,
                macd_histogram REAL,
                bb_upper REAL,
                bb_middle REAL,
                bb_lower REAL,
                UNIQUE(ticker, date)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ticker_date ON stock_prices(ticker, date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_indicators_ticker ON indicators(ticker, date)')
        
        conn.commit()
        print("✅ Database tables created successfully")
    
    def save_stock_data(self, ticker, df):
        """Save stock price data to database"""
        if df is None or df.empty:
            print(f"⚠️  No data to save for {ticker}")
            return False
        
        conn = self.get_connection()
        
        try:
            # Prepare dataframe
            df_to_save = df.copy()
            df_to_save['ticker'] = ticker
            df_to_save['date'] = df_to_save.index.strftime('%Y-%m-%d')
            
            # Select relevant columns
            columns = ['ticker', 'date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df_to_save = df_to_save[columns]
            df_to_save.columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
            
            # Save to database (replace existing data)
            df_to_save.to_sql('stock_prices', conn, if_exists='append', index=False)
            
            print(f"✅ Saved {len(df_to_save)} records for {ticker}")
            return True
            
        except sqlite3.IntegrityError:
            # Data already exists, update instead
            for _, row in df_to_save.iterrows():
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO stock_prices 
                    (ticker, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row['ticker'], row['date'], row['open'], row['high'], 
                      row['low'], row['close'], row['volume']))
            conn.commit()
            print(f"✅ Updated {len(df_to_save)} records for {ticker}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving data for {ticker}: {e}")
            return False
    
    def get_stock_data(self, ticker, start_date=None, end_date=None):
        """Retrieve stock price data from database"""
        conn = self.get_connection()
        
        query = f"SELECT * FROM stock_prices WHERE ticker = '{ticker}'"
        
        if start_date:
            query += f" AND date >= '{start_date}'"
        if end_date:
            query += f" AND date <= '{end_date}'"
        
        query += " ORDER BY date ASC"
        
        try:
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ Error retrieving data for {ticker}: {e}")
            return pd.DataFrame()
    
    def save_indicators(self, ticker, df):
        """Save calculated technical indicators to database"""
        if df is None or df.empty:
            return False
        
        conn = self.get_connection()
        
        try:
            df_to_save = df.copy()
            df_to_save['ticker'] = ticker
            df_to_save['date'] = df_to_save.index.strftime('%Y-%m-%d')
            
            # Save indicators
            for _, row in df_to_save.iterrows():
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO indicators 
                    (ticker, date, sma_20, sma_50, rsi, macd, macd_signal, 
                     macd_histogram, bb_upper, bb_middle, bb_lower)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ticker, row['date'],
                    row.get('SMA_20'), row.get('SMA_50'), row.get('RSI'),
                    row.get('MACD'), row.get('MACD_Signal'), row.get('MACD_Histogram'),
                    row.get('BB_Upper'), row.get('BB_Middle'), row.get('BB_Lower')
                ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Error saving indicators for {ticker}: {e}")
            return False
    
    def get_indicators(self, ticker):
        """Retrieve technical indicators from database"""
        conn = self.get_connection()
        
        query = f"SELECT * FROM indicators WHERE ticker = '{ticker}' ORDER BY date ASC"
        
        try:
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
            
            return df
            
        except Exception as e:
            print(f"❌ Error retrieving indicators for {ticker}: {e}")
            return pd.DataFrame()
    
    def get_all_tickers(self):
        """Get list of all tickers in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker")
        tickers = [row[0] for row in cursor.fetchall()]
        
        return tickers
    
    def get_latest_price(self, ticker):
        """Get the most recent price for a ticker"""
        conn = self.get_connection()
        
        query = f"""
            SELECT close, date 
            FROM stock_prices 
            WHERE ticker = '{ticker}' 
            ORDER BY date DESC 
            LIMIT 1
        """
        
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                return {'close': result[0], 'date': result[1]}
            return None
            
        except Exception as e:
            print(f"❌ Error getting latest price for {ticker}: {e}")
            return None
    
    def save_stock_info(self, ticker, info):
        """Save stock company information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO stock_info 
                (ticker, company_name, sector, industry, market_cap, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                ticker,
                info.get('longName', ticker),
                info.get('sector', 'Unknown'),
                info.get('industry', 'Unknown'),
                info.get('marketCap', 0),
                datetime.now()
            ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Error saving info for {ticker}: {e}")
            return False
    
    def get_stock_info(self, ticker):
        """Retrieve stock company information"""
        conn = self.get_connection()
        
        query = f"SELECT * FROM stock_info WHERE ticker = '{ticker}'"
        
        try:
            df = pd.read_sql_query(query, conn)
            
            if not df.empty:
                return df.iloc[0].to_dict()
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving info for {ticker}: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
