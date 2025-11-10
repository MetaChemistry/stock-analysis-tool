"""
Portfolio Manager - Track custom watchlists and positions
"""

import json
import os
from datetime import datetime


class PortfolioManager:
    """Manage user portfolios and watchlists"""
    
    def __init__(self, portfolio_file='data/portfolios.json'):
        """Initialize portfolio manager"""
        self.portfolio_file = portfolio_file
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create portfolio file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.portfolio_file), exist_ok=True)
        if not os.path.exists(self.portfolio_file):
            self.save_portfolios({'watchlists': {}, 'positions': {}})
    
    def load_portfolios(self):
        """Load portfolios from file"""
        try:
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading portfolios: {e}")
            return {'watchlists': {}, 'positions': {}}
    
    def save_portfolios(self, data):
        """Save portfolios to file"""
        try:
            with open(self.portfolio_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving portfolios: {e}")
            return False
    
    def get_watchlists(self):
        """Get all watchlists"""
        data = self.load_portfolios()
        return data.get('watchlists', {})
    
    def create_watchlist(self, name, tickers=None):
        """Create a new watchlist"""
        data = self.load_portfolios()
        
        if name in data['watchlists']:
            return False, "Watchlist already exists"
        
        data['watchlists'][name] = {
            'tickers': tickers or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        if self.save_portfolios(data):
            return True, f"Watchlist '{name}' created successfully"
        return False, "Failed to save watchlist"
    
    def add_to_watchlist(self, watchlist_name, ticker):
        """Add a ticker to a watchlist"""
        data = self.load_portfolios()
        
        if watchlist_name not in data['watchlists']:
            return False, "Watchlist not found"
        
        ticker = ticker.upper()
        if ticker in data['watchlists'][watchlist_name]['tickers']:
            return False, f"{ticker} already in watchlist"
        
        data['watchlists'][watchlist_name]['tickers'].append(ticker)
        data['watchlists'][watchlist_name]['updated_at'] = datetime.now().isoformat()
        
        if self.save_portfolios(data):
            return True, f"Added {ticker} to '{watchlist_name}'"
        return False, "Failed to update watchlist"
    
    def remove_from_watchlist(self, watchlist_name, ticker):
        """Remove a ticker from a watchlist"""
        data = self.load_portfolios()
        
        if watchlist_name not in data['watchlists']:
            return False, "Watchlist not found"
        
        ticker = ticker.upper()
        if ticker not in data['watchlists'][watchlist_name]['tickers']:
            return False, f"{ticker} not in watchlist"
        
        data['watchlists'][watchlist_name]['tickers'].remove(ticker)
        data['watchlists'][watchlist_name]['updated_at'] = datetime.now().isoformat()
        
        if self.save_portfolios(data):
            return True, f"Removed {ticker} from '{watchlist_name}'"
        return False, "Failed to update watchlist"
    
    def delete_watchlist(self, name):
        """Delete a watchlist"""
        data = self.load_portfolios()
        
        if name not in data['watchlists']:
            return False, "Watchlist not found"
        
        del data['watchlists'][name]
        
        if self.save_portfolios(data):
            return True, f"Watchlist '{name}' deleted"
        return False, "Failed to delete watchlist"
    
    def get_watchlist_tickers(self, name):
        """Get tickers from a specific watchlist"""
        watchlists = self.get_watchlists()
        if name in watchlists:
            return watchlists[name]['tickers']
        return []
