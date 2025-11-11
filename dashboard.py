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
from src.portfolio_manager import PortfolioManager

# Import stock name mapping for search
try:
    from stock_names import get_stock_display_name, search_stocks
except ImportError:
    # Fallback if stock_names.py doesn't exist
    def get_stock_display_name(ticker):
        return ticker
    def search_stocks(query, available_tickers):
        if not query:
            return available_tickers
        query = query.upper()
        return [t for t in available_tickers if query in t.upper()]


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
    portfolio_mgr = PortfolioManager()
    return db, collector, analyzer, news_fetcher, portfolio_mgr

db, collector, analyzer, news_fetcher, portfolio_mgr = init_components()


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

            # Add visual alert for extreme RSI conditions
            if rsi <= 20:
                st.metric(
                    label="RSI ⚠️ EXTREME OVERSOLD",
                    value=f"{rsi:.1f}",
                    delta=rsi_signal,
                    delta_color="inverse"
                )
            elif rsi <= 30:
                st.metric(
                    label="RSI 🟢 Oversold",
                    value=f"{rsi:.1f}",
                    delta=rsi_signal
                )
            elif rsi >= 80:
                st.metric(
                    label="RSI ⚠️ EXTREME OVERBOUGHT",
                    value=f"{rsi:.1f}",
                    delta=rsi_signal,
                    delta_color="inverse"
                )
            elif rsi >= 70:
                st.metric(
                    label="RSI 🔴 Overbought",
                    value=f"{rsi:.1f}",
                    delta=rsi_signal
                )
            else:
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


def display_signal_conflicts(signals, news_sentiment=None, news_score=None):
    """Detect and explain conflicts between technical signals and news sentiment"""

    overall_technical = signals.get('overall', 'HOLD')
    has_conflicts = False
    conflicts = []

    # Check if we have news sentiment to compare
    if news_sentiment and news_score is not None:
        # Technical vs News Conflict
        if overall_technical == 'BUY' and news_sentiment == 'negative':
            has_conflicts = True
            conflicts.append({
                'type': 'Technical vs News',
                'severity': 'high',
                'description': f"Technical signals suggest **BUY** but news sentiment is **NEGATIVE** ({int(news_score*100)}% positive)",
                'explanation': "The charts show bullish patterns, but recent news is bearish. This could indicate market overreaction to news, or technical indicators haven't caught up to fundamental changes yet.",
                'recommendation': "⚠️ Proceed with caution. Wait for news sentiment to improve or for more confirmation from technical indicators."
            })
        elif overall_technical == 'SELL' and news_sentiment == 'positive':
            has_conflicts = True
            conflicts.append({
                'type': 'Technical vs News',
                'severity': 'high',
                'description': f"Technical signals suggest **SELL** but news sentiment is **POSITIVE** ({int(news_score*100)}% positive)",
                'explanation': "The charts show bearish patterns despite positive news. This could mean the price already ran up on the news, or the market doesn't believe the positive narrative.",
                'recommendation': "⚠️ Be cautious. Positive news with declining technicals might be a distribution phase. Consider the broader market context."
            })
        elif overall_technical == 'HOLD' and news_sentiment in ['positive', 'negative']:
            conflicts.append({
                'type': 'Mixed Signals',
                'severity': 'medium',
                'description': f"Technical signals are **NEUTRAL** but news is **{news_sentiment.upper()}** ({int(news_score*100)}% positive)",
                'explanation': "Technical indicators are showing mixed signals while news has a clear sentiment. This often happens during consolidation periods or when the market is digesting information.",
                'recommendation': "💡 Wait for technical confirmation before acting on news sentiment. Look for a clear breakout or breakdown."
            })

    # Internal Technical Conflicts
    trend = signals.get('trend', 'Unknown')
    rsi_signal = signals.get('rsi_signal', 'Unknown')
    macd_signal = signals.get('macd_signal', 'Unknown')

    # RSI vs Trend Conflict
    if 'Uptrend' in trend and rsi_signal == 'Overbought':
        conflicts.append({
            'type': 'RSI vs Trend',
            'severity': 'medium',
            'description': "**Uptrend** continues but RSI shows **Overbought**",
            'explanation': "The stock is in an uptrend but may be due for a pullback. Strong trends can stay overbought for extended periods.",
            'recommendation': "💡 Consider taking partial profits or waiting for a pullback to add positions. Use trailing stop losses."
        })
    elif 'Downtrend' in trend and rsi_signal == 'Oversold':
        has_conflicts = True
        conflicts.append({
            'type': 'RSI vs Trend',
            'severity': 'medium',
            'description': "**Downtrend** continues but RSI shows **Oversold**",
            'explanation': "The stock is in a downtrend but may be oversold. This could be a bounce opportunity, but the trend is still down.",
            'recommendation': "💡 Possible short-term bounce, but risky. Wait for trend reversal confirmation before going long. Consider this for swing trading only."
        })

    # MACD vs RSI Conflict
    if macd_signal == 'Bullish' and rsi_signal == 'Overbought':
        conflicts.append({
            'type': 'MACD vs RSI',
            'severity': 'low',
            'description': "**MACD is Bullish** but **RSI is Overbought**",
            'explanation': "MACD shows momentum is building, but RSI warns of potential overextension. This is common in strong rallies.",
            'recommendation': "💡 Momentum is strong but watch for exhaustion. Look for divergence or MACD crossover as exit signal."
        })
    elif macd_signal == 'Bearish' and rsi_signal == 'Oversold':
        conflicts.append({
            'type': 'MACD vs RSI',
            'severity': 'low',
            'description': "**MACD is Bearish** but **RSI is Oversold**",
            'explanation': "MACD shows downward momentum, but RSI suggests the selloff may be overdone. Potential for a relief rally.",
            'recommendation': "💡 Watch for MACD bullish crossover combined with RSI recovery as a potential reversal signal."
        })

    # Display conflicts if any exist
    if conflicts:
        st.subheader("⚠️ Signal Conflicts & Analysis")

        for i, conflict in enumerate(conflicts):
            severity_color = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🔵'
            }.get(conflict['severity'], '⚪')

            with st.expander(f"{severity_color} {conflict['type']}: {conflict['description']}", expanded=(i==0 and conflict['severity']=='high')):
                st.write(f"**What's Happening:**")
                st.write(conflict['explanation'])
                st.write("")
                st.write(f"**What To Do:**")
                st.write(conflict['recommendation'])

        return True  # Conflicts exist
    else:
        # No conflicts - all signals align
        st.success("✅ **All Signals Aligned** - Technical indicators and news sentiment are in agreement")
        return False  # No conflicts


def display_news_and_sentiment(ticker):
    """Display recent news and sentiment analysis"""
    st.subheader(f"📰 Recent News & Market Sentiment for {ticker}")

    with st.spinner(f"Fetching latest news for {ticker}..."):
        articles = news_fetcher.fetch_news(ticker, max_articles=8)

    if not articles:
        st.info(f"📰 No recent news available for {ticker} from Yahoo Finance.")
        st.caption("News availability varies by stock. Try a major stock like AAPL, TSLA, or MSFT.")
        st.caption("Check your terminal/console for debug information.")
        return None, None  # Return None for sentiment data

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

    # Return sentiment data for conflict detection
    return overall_sentiment, sentiment_score


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
    
    # Stock search and selector
    st.sidebar.subheader("🔍 Stock Search")

    # Search input
    search_query = st.sidebar.text_input(
        "Search by ticker or company name",
        placeholder="e.g., AAPL or Apple",
        key="stock_search"
    )

    # Filter tickers based on search
    if search_query:
        filtered_tickers = search_stocks(search_query, available_tickers)
    else:
        filtered_tickers = available_tickers

    # Show search results count
    if search_query:
        st.sidebar.caption(f"Found {len(filtered_tickers)} matches")

    # Display filtered results as buttons
    if filtered_tickers:
        # Use session state to track selected ticker
        if 'selected_ticker' not in st.session_state:
            st.session_state.selected_ticker = filtered_tickers[0]

        # Show results (limit to 10 for better UX)
        display_limit = min(10, len(filtered_tickers))
        st.sidebar.write("**Results:**")

        for ticker in filtered_tickers[:display_limit]:
            display_name = get_stock_display_name(ticker)
            # Highlight if currently selected
            if ticker == st.session_state.selected_ticker:
                if st.sidebar.button(f"✓ {display_name}", key=f"btn_{ticker}", use_container_width=True):
                    st.session_state.selected_ticker = ticker
                    st.rerun()
            else:
                if st.sidebar.button(display_name, key=f"btn_{ticker}", use_container_width=True):
                    st.session_state.selected_ticker = ticker
                    st.rerun()

        if len(filtered_tickers) > display_limit:
            st.sidebar.caption(f"...and {len(filtered_tickers) - display_limit} more. Refine your search.")

        selected_ticker = st.session_state.selected_ticker
    else:
        st.sidebar.warning("No matches found. Try a different search.")
        selected_ticker = available_tickers[0] if available_tickers else None
        st.session_state.selected_ticker = selected_ticker
    
    # Time range selector
    time_range = st.sidebar.selectbox(
        "Time Range",
        options=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'All'],
        index=4  # Default to 6mo
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

    # Stock info - fetch full info from yfinance for detailed metrics
    import yfinance as yf
    stock = yf.Ticker(selected_ticker)
    try:
        full_stock_info = stock.info
    except:
        full_stock_info = {}

    stock_info = db.get_stock_info(selected_ticker)

    # Basic Company Info (always visible)
    st.sidebar.subheader("ℹ️ Company Info")
    company_name = full_stock_info.get('longName') or (stock_info.get('company_name') if stock_info else selected_ticker)
    st.sidebar.write(f"**{company_name}**")

    sector = full_stock_info.get('sector') or (stock_info.get('sector') if stock_info else 'N/A')
    industry = full_stock_info.get('industry') or (stock_info.get('industry') if stock_info else 'N/A')
    st.sidebar.write(f"Sector: {sector}")
    st.sidebar.write(f"Industry: {industry}")

    # Enhanced Financial Metrics (collapsible)

    # Section 1: Valuation Metrics
    with st.sidebar.expander("💰 Valuation Metrics"):
        col1, col2 = st.columns(2)

        with col1:
            pe_ratio = full_stock_info.get('trailingPE')
            if pe_ratio:
                st.metric("P/E Ratio", f"{pe_ratio:.2f}")
                if pe_ratio < 15:
                    st.caption("✅ Below market avg")
                elif pe_ratio > 30:
                    st.caption("⚠️ Premium valuation")
            else:
                st.metric("P/E Ratio", "N/A")

            pb_ratio = full_stock_info.get('priceToBook')
            if pb_ratio:
                st.metric("Price/Book", f"{pb_ratio:.2f}")
            else:
                st.metric("Price/Book", "N/A")

        with col2:
            peg_ratio = full_stock_info.get('pegRatio')
            if peg_ratio:
                st.metric("PEG Ratio", f"{peg_ratio:.2f}")
                if peg_ratio < 1.0:
                    st.caption("🔥 Undervalued")
                elif peg_ratio > 2.0:
                    st.caption("⚠️ Overvalued")
                else:
                    st.caption("✅ Fair value")
            else:
                st.metric("PEG Ratio", "N/A")

            ev_ebitda = full_stock_info.get('enterpriseToEbitda')
            if ev_ebitda:
                st.metric("EV/EBITDA", f"{ev_ebitda:.2f}")
            else:
                st.metric("EV/EBITDA", "N/A")

        # Market Cap with size category
        market_cap = full_stock_info.get('marketCap')
        if market_cap:
            market_cap_b = market_cap / 1e9
            if market_cap_b >= 200:
                size = "Mega Cap"
                icon = "🏢"
            elif market_cap_b >= 10:
                size = "Large Cap"
                icon = "🏛️"
            elif market_cap_b >= 2:
                size = "Mid Cap"
                icon = "🏪"
            else:
                size = "Small Cap"
                icon = "🏠"
            st.write(f"{icon} **Market Cap:** ${market_cap_b:.2f}B ({size})")
        else:
            st.write("Market Cap: N/A")

    # Section 2: Profitability
    with st.sidebar.expander("📈 Profitability"):
        col1, col2 = st.columns(2)

        with col1:
            profit_margin = full_stock_info.get('profitMargins')
            if profit_margin:
                margin_pct = profit_margin * 100
                st.metric("Profit Margin", f"{margin_pct:.1f}%")
                if margin_pct > 20:
                    st.caption("🔥 Excellent")
                elif margin_pct > 10:
                    st.caption("✅ Good")
                elif margin_pct < 0:
                    st.caption("⚠️ Negative")
            else:
                st.metric("Profit Margin", "N/A")

            operating_margin = full_stock_info.get('operatingMargins')
            if operating_margin:
                st.metric("Operating Margin", f"{operating_margin * 100:.1f}%")
            else:
                st.metric("Operating Margin", "N/A")

        with col2:
            roe = full_stock_info.get('returnOnEquity')
            if roe:
                roe_pct = roe * 100
                st.metric("ROE", f"{roe_pct:.1f}%")
                if roe_pct > 15:
                    st.caption("🔥 Strong")
                elif roe_pct > 10:
                    st.caption("✅ Good")
                else:
                    st.caption("Fair")
            else:
                st.metric("ROE", "N/A")

            roa = full_stock_info.get('returnOnAssets')
            if roa:
                st.metric("ROA", f"{roa * 100:.1f}%")
            else:
                st.metric("ROA", "N/A")

    # Section 3: Financial Health
    with st.sidebar.expander("🏦 Financial Health"):
        col1, col2 = st.columns(2)

        with col1:
            debt_to_equity = full_stock_info.get('debtToEquity')
            if debt_to_equity:
                st.metric("Debt/Equity", f"{debt_to_equity / 100:.2f}")
                if debt_to_equity / 100 > 2.0:
                    st.caption("⚠️ High leverage")
                elif debt_to_equity / 100 < 0.5:
                    st.caption("✅ Conservative")
                else:
                    st.caption("Moderate")
            else:
                st.metric("Debt/Equity", "N/A")

            current_ratio = full_stock_info.get('currentRatio')
            if current_ratio:
                st.metric("Current Ratio", f"{current_ratio:.2f}")
                if current_ratio < 1.0:
                    st.caption("⚠️ Liquidity concern")
                elif current_ratio > 2.0:
                    st.caption("✅ Strong liquidity")
                else:
                    st.caption("✅ Adequate")
            else:
                st.metric("Current Ratio", "N/A")

        with col2:
            total_cash = full_stock_info.get('totalCash')
            if total_cash:
                cash_b = total_cash / 1e9
                st.metric("Total Cash", f"${cash_b:.2f}B")
            else:
                st.metric("Total Cash", "N/A")

            quick_ratio = full_stock_info.get('quickRatio')
            if quick_ratio:
                st.metric("Quick Ratio", f"{quick_ratio:.2f}")
                if quick_ratio < 1.0:
                    st.caption("⚠️ Below 1.0")
                else:
                    st.caption("✅ Healthy")
            else:
                st.metric("Quick Ratio", "N/A")

    # Section 4: Shareholder Returns
    with st.sidebar.expander("💵 Shareholder Returns"):
        col1, col2 = st.columns(2)

        with col1:
            div_yield = full_stock_info.get('dividendYield')
            if div_yield and div_yield > 0:
                st.metric("Dividend Yield", f"{div_yield * 100:.2f}%")
                if div_yield * 100 > 4:
                    st.caption("🔥 High yield")
                elif div_yield * 100 > 2:
                    st.caption("✅ Good yield")
            else:
                st.metric("Dividend Yield", "N/A")
                st.caption("No dividend")

            payout_ratio = full_stock_info.get('payoutRatio')
            if payout_ratio and payout_ratio > 0:
                st.metric("Payout Ratio", f"{payout_ratio * 100:.1f}%")
                if payout_ratio > 0.8:
                    st.caption("⚠️ High payout")
                elif payout_ratio < 0.5:
                    st.caption("✅ Sustainable")
            else:
                st.metric("Payout Ratio", "N/A")

        with col2:
            div_rate = full_stock_info.get('dividendRate')
            if div_rate:
                st.metric("Annual Dividend", f"${div_rate:.2f}")
            else:
                st.metric("Annual Dividend", "N/A")

            trailing_eps = full_stock_info.get('trailingEps')
            if trailing_eps:
                st.metric("EPS (TTM)", f"${trailing_eps:.2f}")
            else:
                st.metric("EPS (TTM)", "N/A")

    # Section 5: Performance vs Market
    with st.sidebar.expander("📊 Performance vs Market"):
        col1, col2 = st.columns(2)

        with col1:
            week52_high = full_stock_info.get('fiftyTwoWeekHigh')
            week52_low = full_stock_info.get('fiftyTwoWeekLow')
            current_price = full_stock_info.get('currentPrice') or full_stock_info.get('regularMarketPrice')

            if week52_high:
                st.metric("52-Week High", f"${week52_high:.2f}")
            else:
                st.metric("52-Week High", "N/A")

            if week52_low:
                st.metric("52-Week Low", f"${week52_low:.2f}")
            else:
                st.metric("52-Week Low", "N/A")

            # Calculate position in 52-week range
            if week52_high and week52_low and current_price:
                range_position = ((current_price - week52_low) / (week52_high - week52_low)) * 100
                st.write(f"**Range Position:** {range_position:.1f}%")
                if range_position > 80:
                    st.caption("🔥 Near highs")
                elif range_position < 20:
                    st.caption("⚠️ Near lows")

        with col2:
            beta = full_stock_info.get('beta')
            if beta:
                st.metric("Beta (Volatility)", f"{beta:.2f}")
                if beta > 1.5:
                    st.caption("⚠️ High volatility")
                elif beta < 0.8:
                    st.caption("✅ Low volatility")
                else:
                    st.caption("Market-like")
            else:
                st.metric("Beta", "N/A")

            # 52 week change
            week52_change = full_stock_info.get('52WeekChange')
            if week52_change:
                st.metric("52-Week Return", f"{week52_change * 100:.1f}%")
                if week52_change > 0.3:
                    st.caption("🔥 Strong performer")
                elif week52_change < -0.2:
                    st.caption("⚠️ Underperformer")
            else:
                st.metric("52-Week Return", "N/A")

    st.sidebar.markdown("---")

    # Portfolio Management
    st.sidebar.subheader("📁 My Watchlists")

    # Get existing watchlists
    watchlists = portfolio_mgr.get_watchlists()

    if watchlists:
        watchlist_names = list(watchlists.keys())
        selected_watchlist = st.sidebar.selectbox(
            "Select Watchlist",
            options=['Default'] + watchlist_names,
            index=0
        )

        if selected_watchlist != 'Default':
            # Show watchlist tickers
            wl_tickers = portfolio_mgr.get_watchlist_tickers(selected_watchlist)
            if wl_tickers:
                st.sidebar.write(f"**Stocks ({len(wl_tickers)}):**")
                st.sidebar.write(", ".join(wl_tickers))

                # Remove from watchlist
                ticker_to_remove = st.sidebar.selectbox(
                    "Remove stock",
                    options=wl_tickers,
                    key="remove_ticker"
                )
                if st.sidebar.button(f"🗑️ Remove {ticker_to_remove}"):
                    success, msg = portfolio_mgr.remove_from_watchlist(selected_watchlist, ticker_to_remove)
                    if success:
                        st.sidebar.success(msg)
                        st.rerun()
                    else:
                        st.sidebar.error(msg)

    # Create new watchlist
    with st.sidebar.expander("➕ Create New Watchlist"):
        new_wl_name = st.text_input("Watchlist Name", key="new_watchlist")
        if st.button("Create"):
            if new_wl_name:
                success, msg = portfolio_mgr.create_watchlist(new_wl_name)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.error("Please enter a watchlist name")

    # Add current stock to watchlist
    if watchlists:
        with st.sidebar.expander(f"➕ Add {selected_ticker} to Watchlist"):
            target_watchlist = st.selectbox(
                "Select watchlist",
                options=list(watchlists.keys()),
                key="add_to_watchlist"
            )
            if st.button(f"Add {selected_ticker}"):
                success, msg = portfolio_mgr.add_to_watchlist(target_watchlist, selected_ticker)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    # Get stock data
    df = db.get_stock_data(selected_ticker)
    
    if df.empty:
        st.error(f"No data found for {selected_ticker}")
        return
    
    # Filter by time range
    if time_range != 'All':
        end_date = datetime.now()
        if time_range == '1d':
            start_date = end_date - timedelta(days=1)
        elif time_range == '5d':
            start_date = end_date - timedelta(days=5)
        elif time_range == '1mo':
            start_date = end_date - timedelta(days=30)
        elif time_range == '3mo':
            start_date = end_date - timedelta(days=90)
        elif time_range == '6mo':
            start_date = end_date - timedelta(days=180)
        elif time_range == '1y':
            start_date = end_date - timedelta(days=365)
        elif time_range == '2y':
            start_date = end_date - timedelta(days=730)
        elif time_range == '5y':
            start_date = end_date - timedelta(days=1825)

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

    # Display news and sentiment (get sentiment data back)
    news_sentiment, news_score = display_news_and_sentiment(selected_ticker)

    st.markdown("---")

    # Display signal conflicts and analysis
    display_signal_conflicts(signals, news_sentiment, news_score)

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
