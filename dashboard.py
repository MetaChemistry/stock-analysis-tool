"""
Stock Analysis Dashboard - Interactive Streamlit Web Interface
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from src.database import StockDatabase
from src.data_collector import DataCollector
from src.analyzer import TechnicalAnalyzer
from src.news_fetcher import NewsFetcher


# Page configuration
st.set_page_config(
    page_title="Stock Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def init_components():
    """Initialize database, collector, and analyzer"""
    db = StockDatabase(config.DATABASE_PATH)
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    news_fetcher = NewsFetcher()
    return db, collector, analyzer, news_fetcher

db, collector, analyzer, news_fetcher = init_components()


def create_candlestick_chart(df, ticker):
    """Create interactive candlestick chart with indicators"""
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=(f'{ticker} Price & Indicators', 'MACD', 'RSI')
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Add moving averages
    if 'SMA_20' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['SMA_20'],
                name='SMA 20',
                line=dict(color='orange', width=1)
            ),
            row=1, col=1
        )
    
    if 'SMA_50' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['SMA_50'],
                name='SMA 50',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
    
    # Add Bollinger Bands
    if 'BB_Upper' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BB_Upper'],
                name='BB Upper',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['BB_Lower'],
                name='BB Lower',
                line=dict(color='gray', width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(128, 128, 128, 0.1)',
                showlegend=False
            ),
            row=1, col=1
        )
    
    # MACD
    if 'MACD' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD'],
                name='MACD',
                line=dict(color='blue', width=1)
            ),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['MACD_Signal'],
                name='Signal',
                line=dict(color='red', width=1)
            ),
            row=2, col=1
        )
        
        # MACD Histogram
        colors = ['green' if val >= 0 else 'red' for val in df['MACD_Histogram']]
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['MACD_Histogram'],
                name='Histogram',
                marker_color=colors
            ),
            row=2, col=1
        )
    
    # RSI
    if 'RSI' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['RSI'],
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=3, col=1
        )
        
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # Update layout
    fig.update_layout(
        height=config.CHART_HEIGHT,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    
    return fig


def display_metrics(ticker, df_with_indicators):
    """Display key metrics in columns"""
    if df_with_indicators is None or df_with_indicators.empty:
        st.warning("No data available")
        return
    
    latest = df_with_indicators.iloc[-1]
    signals = analyzer.generate_signals(df_with_indicators)
    
    # Create columns for metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        price = latest['close']
        prev_price = df_with_indicators.iloc[-2]['close'] if len(df_with_indicators) > 1 else price
        change = price - prev_price
        change_pct = (change / prev_price) * 100
        
        st.metric(
            label="Current Price",
            value=f"${price:.2f}",
            delta=f"{change_pct:.2f}%"
        )
    
    with col2:
        trend = signals.get('trend', 'Unknown')
        trend_emoji = "📈" if "Up" in trend else "📉" if "Down" in trend else "➡️"
        st.metric(
            label="Trend",
            value=trend_emoji,
            delta=trend
        )
    
    with col3:
        rsi = latest.get('RSI', 0)
        if pd.notna(rsi):
            rsi_signal = signals.get('rsi_signal', 'Unknown')
            st.metric(
                label="RSI",
                value=f"{rsi:.1f}",
                delta=rsi_signal
            )
    
    with col4:
        macd_signal = signals.get('macd_signal', 'Unknown')
        macd_emoji = "🟢" if macd_signal == "Bullish" else "🔴" if macd_signal == "Bearish" else "⚪"
        st.metric(
            label="MACD",
            value=macd_emoji,
            delta=macd_signal
        )
    
    with col5:
        overall = signals.get('overall', 'HOLD')
        overall_color = "🟢" if overall == "BUY" else "🔴" if overall == "SELL" else "🟡"
        st.metric(
            label="Signal",
            value=overall_color,
            delta=overall
        )


def display_signals_panel(signals):
    """Display detailed signals panel"""
    st.subheader("📊 Technical Analysis Signals")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Trend Analysis**")
        st.write(f"- Trend: {signals.get('trend', 'Unknown')}")
        st.write(f"- Bollinger Bands: {signals.get('bb_signal', 'Unknown')}")

    with col2:
        st.write("**Momentum Indicators**")
        st.write(f"- RSI Signal: {signals.get('rsi_signal', 'Unknown')}")
        st.write(f"- MACD Signal: {signals.get('macd_signal', 'Unknown')}")

    # Overall recommendation
    overall = signals.get('overall', 'HOLD')

    if overall == 'BUY':
        st.success(f"🟢 Overall Signal: **{overall}** - Bullish indicators dominate")
    elif overall == 'SELL':
        st.error(f"🔴 Overall Signal: **{overall}** - Bearish indicators dominate")
    else:
        st.warning(f"🟡 Overall Signal: **{overall}** - Mixed signals, wait for clearer trend")


def display_news_and_sentiment(ticker):
    """Display recent news and sentiment analysis"""
    st.subheader("📰 Recent News & Market Sentiment")

    with st.spinner("Fetching latest news..."):
        articles = news_fetcher.fetch_news(ticker, max_articles=8)

    if not articles:
        st.info(f"📰 No recent news available for {ticker} from Yahoo Finance.")
        st.caption("News availability varies by stock. Try a major stock like AAPL, TSLA, or MSFT.")
        st.caption("Check your terminal/console for debug information.")
        return

    # Calculate overall sentiment
    overall_sentiment, sentiment_score = news_fetcher.get_overall_sentiment(articles)

    # Display overall sentiment
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        sentiment_emoji = news_fetcher.get_sentiment_emoji(overall_sentiment)
        st.metric(
            label="News Sentiment",
            value=sentiment_emoji,
            delta=overall_sentiment.upper()
        )

    with col2:
        # Sentiment gauge
        sentiment_percentage = int(sentiment_score * 100)

        if overall_sentiment == 'positive':
            st.success(f"📈 Market sentiment is **{overall_sentiment.upper()}** ({sentiment_percentage}% positive)")
        elif overall_sentiment == 'negative':
            st.error(f"📉 Market sentiment is **{overall_sentiment.upper()}** ({sentiment_percentage}% positive)")
        else:
            st.info(f"➡️ Market sentiment is **{overall_sentiment.upper()}** ({sentiment_percentage}% positive)")

    with col3:
        st.metric(
            label="Articles Analyzed",
            value=len(articles)
        )

    st.markdown("---")

    # Display news articles
    st.write("**Latest Headlines:**")

    for i, article in enumerate(articles, 1):
        sentiment = article['sentiment']
        sentiment_color = news_fetcher.get_sentiment_color(sentiment)
        sentiment_emoji = news_fetcher.get_sentiment_emoji(sentiment)

        # Create columns for article display
        col_main, col_sentiment = st.columns([5, 1])

        with col_main:
            # Article title with link
            st.markdown(f"**{i}. [{article['title']}]({article['link']})**")

            # Publisher and time
            st.caption(f"{article['publisher']} • {article['published']}")

        with col_sentiment:
            # Sentiment indicator
            if sentiment == 'positive':
                st.success(f"{sentiment_emoji} Positive")
            elif sentiment == 'negative':
                st.error(f"{sentiment_emoji} Negative")
            else:
                st.info(f"{sentiment_emoji} Neutral")

        # Add spacing
        if i < len(articles):
            st.markdown("")


def main():
    """Main dashboard function"""
    
    # Title
    st.title("📊 Stock Analysis Tool")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    
    # Get available tickers
    available_tickers = db.get_all_tickers()
    
    if not available_tickers:
        st.warning("⚠️ No data available. Please run data collection first!")
        
        if st.button("🔄 Collect Data Now"):
            with st.spinner("Collecting data... This may take a minute..."):
                collector.collect_watchlist()
                st.success("✅ Data collected! Refreshing...")
                st.rerun()
        
        st.info("💡 Or run: `python src/data_collector.py` from terminal")
        return
    
    # Stock selector
    selected_ticker = st.sidebar.selectbox(
        "Select Stock",
        options=available_tickers,
        index=0
    )
    
    # Time range selector
    time_range = st.sidebar.selectbox(
        "Time Range",
        options=['1mo', '3mo', '6mo', '1y', '2y', 'All'],
        index=2
    )
    
    # Update button
    if st.sidebar.button("🔄 Update Data"):
        with st.spinner(f"Updating {selected_ticker}..."):
            collector.update_single_stock(selected_ticker)
            st.sidebar.success("✅ Updated!")
            st.rerun()
    
    # Update all button
    if st.sidebar.button("🔄 Update All Stocks"):
        with st.spinner("Updating all stocks..."):
            collector.collect_watchlist()
            st.sidebar.success("✅ All stocks updated!")
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Stock info
    stock_info = db.get_stock_info(selected_ticker)
    if stock_info:
        st.sidebar.subheader("ℹ️ Company Info")
        st.sidebar.write(f"**{stock_info.get('company_name', selected_ticker)}**")
        st.sidebar.write(f"Sector: {stock_info.get('sector', 'N/A')}")
        st.sidebar.write(f"Industry: {stock_info.get('industry', 'N/A')}")
    
    # Get stock data
    df = db.get_stock_data(selected_ticker)
    
    if df.empty:
        st.error(f"No data found for {selected_ticker}")
        return
    
    # Filter by time range
    if time_range != 'All':
        end_date = datetime.now()
        if time_range == '1mo':
            start_date = end_date - timedelta(days=30)
        elif time_range == '3mo':
            start_date = end_date - timedelta(days=90)
        elif time_range == '6mo':
            start_date = end_date - timedelta(days=180)
        elif time_range == '1y':
            start_date = end_date - timedelta(days=365)
        elif time_range == '2y':
            start_date = end_date - timedelta(days=730)
        
        df = df[df.index >= start_date]
    
    # Calculate indicators
    df_with_indicators = analyzer.calculate_all_indicators(df)
    
    # Save indicators to database
    db.save_indicators(selected_ticker, df_with_indicators)
    
    # Generate signals
    signals = analyzer.generate_signals(df_with_indicators)
    
    # Display metrics
    display_metrics(selected_ticker, df_with_indicators)
    
    st.markdown("---")
    
    # Display chart
    st.subheader(f"📈 {selected_ticker} Chart")
    fig = create_candlestick_chart(df_with_indicators, selected_ticker)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Display signals
    display_signals_panel(signals)

    st.markdown("---")

    # Display news and sentiment
    display_news_and_sentiment(selected_ticker)

    st.markdown("---")

    # Display raw data
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            df_with_indicators.tail(50).sort_index(ascending=False),
            use_container_width=True
        )
    
    # Footer
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("⚠️ This tool is for educational purposes only. Not financial advice.")


if __name__ == '__main__':
    main()
