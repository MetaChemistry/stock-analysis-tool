"""
Technical Analyzer Module - Calculate technical indicators and generate signals
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class TechnicalAnalyzer:
    """Calculate technical indicators and identify trading signals"""
    
    def __init__(self):
        """Initialize analyzer with configuration"""
        self.short_window = config.SHORT_WINDOW
        self.long_window = config.LONG_WINDOW
        self.rsi_period = config.RSI_PERIOD
        self.macd_fast = config.MACD_FAST
        self.macd_slow = config.MACD_SLOW
        self.macd_signal = config.MACD_SIGNAL
        self.bb_period = config.BOLLINGER_PERIOD
        self.bb_std = config.BOLLINGER_STD
    
    def calculate_sma(self, df, window):
        """Calculate Simple Moving Average"""
        close_col = 'Close' if 'Close' in df.columns else 'close'
        return df[close_col].rolling(window=window).mean()

    def calculate_ema(self, df, window):
        """Calculate Exponential Moving Average"""
        close_col = 'Close' if 'Close' in df.columns else 'close'
        return df[close_col].ewm(span=window, adjust=False).mean()

    def calculate_rsi(self, df, period=None):
        """Calculate Relative Strength Index"""
        period = period or self.rsi_period
        close_col = 'Close' if 'Close' in df.columns else 'close'

        # Calculate price changes
        delta = df[close_col].diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=period).mean()
        avg_losses = losses.rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, df):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        # Calculate EMAs
        ema_fast = self.calculate_ema(df, self.macd_fast)
        ema_slow = self.calculate_ema(df, self.macd_slow)
        
        # Calculate MACD line
        macd = ema_fast - ema_slow
        
        # Calculate signal line
        signal = macd.ewm(span=self.macd_signal, adjust=False).mean()
        
        # Calculate histogram
        histogram = macd - signal
        
        return macd, signal, histogram
    
    def calculate_bollinger_bands(self, df):
        """Calculate Bollinger Bands"""
        close_col = 'Close' if 'Close' in df.columns else 'close'

        # Calculate middle band (SMA)
        middle = df[close_col].rolling(window=self.bb_period).mean()

        # Calculate standard deviation
        std = df[close_col].rolling(window=self.bb_period).std()
        
        # Calculate upper and lower bands
        upper = middle + (std * self.bb_std)
        lower = middle - (std * self.bb_std)
        
        return upper, middle, lower
    
    def calculate_all_indicators(self, df):
        """Calculate all technical indicators"""
        if df is None or df.empty:
            return None
        
        result = df.copy()
        
        # Moving Averages
        result['SMA_20'] = self.calculate_sma(df, self.short_window)
        result['SMA_50'] = self.calculate_sma(df, self.long_window)
        
        # RSI
        result['RSI'] = self.calculate_rsi(df)
        
        # MACD
        macd, signal, histogram = self.calculate_macd(df)
        result['MACD'] = macd
        result['MACD_Signal'] = signal
        result['MACD_Histogram'] = histogram
        
        # Bollinger Bands
        upper, middle, lower = self.calculate_bollinger_bands(df)
        result['BB_Upper'] = upper
        result['BB_Middle'] = middle
        result['BB_Lower'] = lower
        
        return result
    
    def identify_trend(self, df):
        """Identify current trend based on moving averages"""
        if df is None or df.empty or 'SMA_20' not in df.columns:
            return 'Unknown'

        latest = df.iloc[-1]
        close_col = 'Close' if 'Close' in df.columns else 'close'

        if pd.isna(latest['SMA_20']) or pd.isna(latest['SMA_50']):
            return 'Unknown'

        if latest['SMA_20'] > latest['SMA_50']:
            if latest[close_col] > latest['SMA_20']:
                return 'Strong Uptrend'
            return 'Uptrend'
        elif latest['SMA_20'] < latest['SMA_50']:
            if latest[close_col] < latest['SMA_20']:
                return 'Strong Downtrend'
            return 'Downtrend'
        else:
            return 'Sideways'
    
    def get_rsi_signal(self, df):
        """Get RSI-based signal"""
        if df is None or df.empty or 'RSI' not in df.columns:
            return 'Unknown'
        
        latest_rsi = df['RSI'].iloc[-1]
        
        if pd.isna(latest_rsi):
            return 'Unknown'
        
        if latest_rsi >= config.RSI_OVERBOUGHT:
            return 'Overbought'
        elif latest_rsi <= config.RSI_OVERSOLD:
            return 'Oversold'
        elif latest_rsi > 50:
            return 'Bullish'
        else:
            return 'Bearish'
    
    def get_macd_signal(self, df):
        """Get MACD-based signal"""
        if df is None or df.empty or 'MACD' not in df.columns:
            return 'Unknown'
        
        latest = df.iloc[-1]
        
        if pd.isna(latest['MACD']) or pd.isna(latest['MACD_Signal']):
            return 'Unknown'
        
        if latest['MACD'] > latest['MACD_Signal']:
            return 'Bullish'
        else:
            return 'Bearish'
    
    def get_bollinger_signal(self, df):
        """Get Bollinger Bands signal"""
        if df is None or df.empty or 'BB_Upper' not in df.columns:
            return 'Unknown'

        latest = df.iloc[-1]
        close_col = 'Close' if 'Close' in df.columns else 'close'

        if pd.isna(latest['BB_Upper']) or pd.isna(latest['BB_Lower']):
            return 'Unknown'

        price = latest[close_col]

        if price >= latest['BB_Upper']:
            return 'Overbought'
        elif price <= latest['BB_Lower']:
            return 'Oversold'
        else:
            return 'Neutral'
    
    def generate_signals(self, df):
        """Generate comprehensive trading signals"""
        if df is None or df.empty:
            return {}
        
        signals = {
            'trend': self.identify_trend(df),
            'rsi_signal': self.get_rsi_signal(df),
            'macd_signal': self.get_macd_signal(df),
            'bb_signal': self.get_bollinger_signal(df),
        }
        
        # Overall recommendation
        bullish_count = 0
        bearish_count = 0
        
        if 'Uptrend' in signals['trend']:
            bullish_count += 2
        elif 'Downtrend' in signals['trend']:
            bearish_count += 2
        
        if signals['rsi_signal'] in ['Bullish', 'Oversold']:
            bullish_count += 1
        elif signals['rsi_signal'] in ['Bearish', 'Overbought']:
            bearish_count += 1
        
        if signals['macd_signal'] == 'Bullish':
            bullish_count += 1
        elif signals['macd_signal'] == 'Bearish':
            bearish_count += 1
        
        if signals['bb_signal'] == 'Oversold':
            bullish_count += 1
        elif signals['bb_signal'] == 'Overbought':
            bearish_count += 1
        
        # Determine overall signal
        if bullish_count > bearish_count + 1:
            signals['overall'] = 'BUY'
        elif bearish_count > bullish_count + 1:
            signals['overall'] = 'SELL'
        else:
            signals['overall'] = 'HOLD'
        
        # Add numeric values for display
        latest = df.iloc[-1]
        close_col = 'Close' if 'Close' in df.columns else 'close'
        signals['values'] = {
            'price': latest[close_col],
            'sma_20': latest.get('SMA_20'),
            'sma_50': latest.get('SMA_50'),
            'rsi': latest.get('RSI'),
            'macd': latest.get('MACD'),
            'macd_signal': latest.get('MACD_Signal'),
        }
        
        return signals
    
    def get_support_resistance(self, df, window=20):
        """Identify support and resistance levels"""
        if df is None or df.empty:
            return None, None

        recent = df.tail(window)
        low_col = 'Low' if 'Low' in df.columns else 'low'
        high_col = 'High' if 'High' in df.columns else 'high'

        support = recent[low_col].min()
        resistance = recent[high_col].max()

        return support, resistance

    def calculate_volatility(self, df, window=20):
        """Calculate price volatility"""
        if df is None or df.empty:
            return None

        close_col = 'Close' if 'Close' in df.columns else 'close'
        returns = df[close_col].pct_change()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)  # Annualized

        return volatility.iloc[-1] if not volatility.empty else None
