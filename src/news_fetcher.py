"""
News Fetcher Module - Fetch and analyze stock-related news
"""

import yfinance as yf
from datetime import datetime, timedelta
import re


class NewsFetcher:
    """Fetch news and perform basic sentiment analysis"""
    
    def __init__(self):
        """Initialize news fetcher"""
        self.sentiment_words = {
            'positive': [
                'surge', 'soar', 'rally', 'gain', 'rise', 'jump', 'climb', 'boost', 
                'profit', 'beat', 'exceed', 'outperform', 'strong', 'growth', 
                'upgrade', 'bullish', 'breakthrough', 'success', 'record', 'high',
                'positive', 'optimistic', 'confident', 'impressive', 'stellar'
            ],
            'negative': [
                'fall', 'drop', 'plunge', 'decline', 'loss', 'miss', 'weak', 'concern',
                'downgrade', 'bearish', 'struggle', 'slump', 'crash', 'tumble', 'slide',
                'negative', 'pessimistic', 'warning', 'risk', 'threat', 'disappointing',
                'fear', 'volatile', 'uncertainty', 'crisis', 'failed'
            ]
        }
    
    def fetch_news(self, ticker, max_articles=10):
        """Fetch recent news for a stock ticker"""
        try:
            stock = yf.Ticker(ticker)

            # Try to get news
            try:
                news = stock.news
            except AttributeError:
                # Fallback: try alternative method
                print(f"News attribute not available for {ticker}, trying alternative...")
                news = []

            # Debug: print what we got
            print(f"DEBUG: Fetched {len(news) if news else 0} news items for {ticker}")

            if not news or len(news) == 0:
                print(f"No news data available from Yahoo Finance for {ticker}")
                return []

            # Limit to max_articles
            news = news[:max_articles]

            # Process news items
            articles = []
            for idx, item in enumerate(news):
                # Debug: print item structure
                if idx == 0:
                    print(f"DEBUG: First news item keys: {item.keys()}")

                # Handle new yfinance structure with 'content' key
                if 'content' in item and isinstance(item['content'], dict):
                    content = item['content']
                    # Extract data from content object
                    title = content.get('title') or content.get('headline') or 'No title available'
                    publisher = content.get('provider', {}).get('displayName') or content.get('publisher') or 'Unknown'
                    link = content.get('clickThroughUrl', {}).get('url') or content.get('link') or '#'
                    thumbnail = ''

                    # Try to get thumbnail
                    if 'thumbnail' in content:
                        thumb = content['thumbnail']
                        if isinstance(thumb, dict) and 'resolutions' in thumb and thumb['resolutions']:
                            thumbnail = thumb['resolutions'][0].get('url', '')

                    # Handle timestamp
                    timestamp = content.get('pubDate') or content.get('providerPublishTime') or 0
                else:
                    # Fallback to old structure
                    title = item.get('title') or item.get('headline') or 'No title available'
                    publisher = item.get('publisher') or item.get('source') or 'Unknown'
                    link = item.get('link') or item.get('url') or '#'
                    timestamp = item.get('providerPublishTime') or item.get('publishedAt') or 0
                    thumbnail = item.get('thumbnail', {}).get('resolutions', [{}])[0].get('url', '') if isinstance(item.get('thumbnail'), dict) else ''

                article = {
                    'title': title,
                    'publisher': publisher,
                    'link': link,
                    'published': self._format_timestamp(timestamp),
                    'thumbnail': thumbnail,
                }

                # Add sentiment
                article['sentiment'] = self._analyze_sentiment(article['title'])
                articles.append(article)

            print(f"Successfully processed {len(articles)} articles for {ticker}")
            return articles

        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _format_timestamp(self, timestamp):
        """Convert Unix timestamp to readable date"""
        try:
            dt = datetime.fromtimestamp(timestamp)
            
            # Calculate time ago
            now = datetime.now()
            diff = now - dt
            
            if diff.days == 0:
                hours = diff.seconds // 3600
                if hours == 0:
                    minutes = diff.seconds // 60
                    return f"{minutes} minutes ago"
                return f"{hours} hours ago"
            elif diff.days == 1:
                return "Yesterday"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            else:
                return dt.strftime('%b %d, %Y')
                
        except Exception:
            return "Recently"
    
    def _analyze_sentiment(self, text):
        """Simple sentiment analysis based on keyword matching"""
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        
        # Count positive and negative words
        positive_count = sum(1 for word in self.sentiment_words['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_words['negative'] if word in text_lower)
        
        # Determine sentiment
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def get_overall_sentiment(self, articles):
        """Calculate overall sentiment from multiple articles"""
        if not articles:
            return 'neutral', 0.5
        
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for article in articles:
            sentiment = article.get('sentiment', 'neutral')
            sentiment_counts[sentiment] += 1
        
        total = len(articles)
        positive_ratio = sentiment_counts['positive'] / total
        negative_ratio = sentiment_counts['negative'] / total
        
        # Calculate sentiment score (0 = very negative, 1 = very positive)
        sentiment_score = (positive_ratio + (1 - negative_ratio)) / 2
        
        # Determine overall sentiment
        if sentiment_score >= 0.6:
            overall = 'positive'
        elif sentiment_score <= 0.4:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return overall, sentiment_score
    
    def get_sentiment_emoji(self, sentiment):
        """Get emoji representation of sentiment"""
        emoji_map = {
            'positive': '😊',
            'negative': '😟',
            'neutral': '😐'
        }
        return emoji_map.get(sentiment, '😐')
    
    def get_sentiment_color(self, sentiment):
        """Get color for sentiment"""
        color_map = {
            'positive': 'green',
            'negative': 'red',
            'neutral': 'gray'
        }
        return color_map.get(sentiment, 'gray')
