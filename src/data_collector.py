"""
Data Collector Module - Fetches stock data from Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.database import StockDatabase


class DataCollector:
    """Handles fetching stock data from Yahoo Finance"""
    
    def __init__(self, db_path=None):
        """Initialize data collector"""
        db_path = db_path or config.DATABASE_PATH
        self.db = StockDatabase(db_path)
        self.period = config.DATA_PERIOD
        self.interval = config.DATA_INTERVAL
    
    def fetch_stock_data(self, ticker, period=None, interval=None):
        """Fetch historical stock data from Yahoo Finance"""
        period = period or self.period
        interval = interval or self.interval
        
        try:
            print(f"📥 Fetching data for {ticker}...")
            
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df.empty:
                print(f"⚠️  No data found for {ticker}")
                return None
            
            print(f"✅ Fetched {len(df)} records for {ticker}")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching {ticker}: {e}")
            return None
    
    def fetch_stock_info(self, ticker):
        """Fetch company information for a stock"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if info:
                print(f"✅ Fetched info for {ticker}")
                return info
            
            return None
            
        except Exception as e:
            print(f"⚠️  Error fetching info for {ticker}: {e}")
            return None
    
    def collect_watchlist(self, watchlist=None, save_to_db=True):
        """Collect data for all stocks in watchlist"""
        watchlist = watchlist or config.WATCHLIST
        
        print(f"\n{'='*60}")
        print(f"📊 COLLECTING DATA FOR {len(watchlist)} STOCKS")
        print(f"{'='*60}\n")
        
        results = {}
        
        for i, ticker in enumerate(watchlist, 1):
            print(f"\n[{i}/{len(watchlist)}] Processing {ticker}...")
            
            # Fetch price data
            df = self.fetch_stock_data(ticker)
            
            if df is not None and save_to_db:
                # Save to database
                self.db.save_stock_data(ticker, df)
                
                # Fetch and save company info
                info = self.fetch_stock_info(ticker)
                if info:
                    self.db.save_stock_info(ticker, info)
                
                results[ticker] = {
                    'success': True,
                    'records': len(df),
                    'latest_date': df.index[-1] if not df.empty else None
                }
            else:
                results[ticker] = {
                    'success': False,
                    'records': 0,
                    'latest_date': None
                }
            
            # Rate limiting - be nice to Yahoo Finance
            if i < len(watchlist):
                time.sleep(0.5)
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"📊 COLLECTION SUMMARY")
        print(f"{'='*60}")
        
        successful = sum(1 for r in results.values() if r['success'])
        total_records = sum(r['records'] for r in results.values())
        
        print(f"✅ Successful: {successful}/{len(watchlist)}")
        print(f"📈 Total records: {total_records}")
        print(f"{'='*60}\n")
        
        return results
    
    def update_single_stock(self, ticker):
        """Update data for a single stock"""
        print(f"\n🔄 Updating {ticker}...")
        
        df = self.fetch_stock_data(ticker)
        
        if df is not None:
            self.db.save_stock_data(ticker, df)
            
            info = self.fetch_stock_info(ticker)
            if info:
                self.db.save_stock_info(ticker, info)
            
            print(f"✅ {ticker} updated successfully")
            return True
        
        print(f"❌ Failed to update {ticker}")
        return False
    
    def get_latest_price(self, ticker):
        """Get the most recent price for a ticker"""
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period='1d')
            
            if not df.empty:
                return {
                    'close': df['Close'].iloc[-1],
                    'date': df.index[-1],
                    'change': df['Close'].iloc[-1] - df['Open'].iloc[-1],
                    'change_percent': ((df['Close'].iloc[-1] - df['Open'].iloc[-1]) / df['Open'].iloc[-1]) * 100
                }
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting latest price for {ticker}: {e}")
            return None
    
    def check_data_freshness(self, ticker):
        """Check if data needs updating"""
        latest = self.db.get_latest_price(ticker)
        
        if not latest:
            return True  # No data, needs update
        
        latest_date = pd.to_datetime(latest['date'])
        days_old = (datetime.now() - latest_date).days
        
        if days_old > 1:
            return True  # Data is stale
        
        return False


def main():
    """Main function to run data collection"""
    print("\n" + "="*60)
    print("🚀 STOCK ANALYSIS TOOL - DATA COLLECTOR")
    print("="*60 + "\n")
    
    collector = DataCollector()
    
    # Collect data for all stocks in watchlist
    results = collector.collect_watchlist()
    
    print("\n✅ Data collection complete!")
    print(f"📁 Database: {config.DATABASE_PATH}")
    print("\n💡 Next step: Run the dashboard with 'streamlit run dashboard.py'\n")


if __name__ == '__main__':
    main()
