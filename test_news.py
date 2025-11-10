"""
Test script to check if news is being fetched properly
"""

import yfinance as yf
from src.news_fetcher import NewsFetcher

# Test with a few different stocks
test_stocks = ['AAPL', 'TSLA', 'MSFT', 'AMZN']

print("="*60)
print("NEWS FETCHING TEST")
print("="*60)

for ticker in test_stocks:
    print(f"\n{'='*60}")
    print(f"Testing {ticker}...")
    print(f"{'='*60}")
    
    # Test direct yfinance access
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        print(f"✓ Direct yfinance: {len(news) if news else 0} articles found")
        
        if news:
            print(f"\nFirst article:")
            print(f"  Title: {news[0].get('title', 'N/A')}")
            print(f"  Publisher: {news[0].get('publisher', 'N/A')}")
            print(f"  Link: {news[0].get('link', 'N/A')}")
    except Exception as e:
        print(f"✗ Direct yfinance failed: {e}")
    
    # Test with our NewsFetcher class
    print(f"\nUsing NewsFetcher class:")
    fetcher = NewsFetcher()
    articles = fetcher.fetch_news(ticker, max_articles=3)
    
    if articles:
        print(f"✓ Successfully fetched {len(articles)} articles")
        for i, article in enumerate(articles, 1):
            print(f"\n  Article {i}:")
            print(f"    Title: {article['title'][:80]}...")
            print(f"    Sentiment: {article['sentiment']}")
    else:
        print(f"✗ No articles returned")

print(f"\n{'='*60}")
print("TEST COMPLETE")
print(f"{'='*60}\n")
