# 📊 S&P 500 Stock List Setup

Your dashboard now has access to **all S&P 500 stocks**!

---

## 🎯 Current Setup

By default, you're using the **Top 100** stocks by market cap for faster performance.

### What You Get:

✅ **100 major stocks** across all sectors  
✅ **Faster data collection** (~2-3 minutes)  
✅ **Lower memory usage**  
✅ **Covers 80%+ of S&P 500 market cap**  

**Stocks included:**
- AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA, etc.
- All FAANG stocks
- Major banks: JPM, BAC, WFC, GS, MS
- Healthcare: UNH, LLY, JNJ, ABBV
- And 80+ more top companies!

---

## 🔄 Switch to All 500+ Stocks

Want access to **every S&P 500 stock**?

### Steps:

1. Open `config.py`
2. Find line 17-18:
```python
WATCHLIST = TOP_100_TICKERS        # ← Currently active
# WATCHLIST = SP500_TICKERS        # ← All S&P 500
```

3. Comment out line 17, uncomment line 18:
```python
# WATCHLIST = TOP_100_TICKERS      # ← Disabled
WATCHLIST = SP500_TICKERS          # ← Now active
```

4. Save and restart dashboard

### Data Collection Time:
- **Top 100**: ~2-3 minutes
- **All 500+**: ~8-12 minutes

### Trade-offs:

| Feature | Top 100 | All 500+ |
|---------|---------|----------|
| Stocks Available | 100 | 500+ |
| Data Collection | Fast (2-3 min) | Slower (8-12 min) |
| Memory Usage | Low | Medium |
| Major Companies | ✅ All included | ✅ All included |
| Small/Mid Caps | Some | ✅ All included |

---

## 📋 Stock Lists Included

### Top 100 Sectors Breakdown:
- **Technology**: AAPL, MSFT, NVDA, GOOGL, META, etc.
- **Finance**: JPM, BAC, V, MA, WFC, GS, etc.
- **Healthcare**: UNH, LLY, JNJ, ABBV, MRK, etc.
- **Consumer**: AMZN, TSLA, WMT, HD, MCD, etc.
- **Energy**: XOM, CVX, COP, SLB, etc.
- **Industrials**: BA, UNP, HON, CAT, etc.

### All S&P 500 includes everything above PLUS:
- Small-cap growth stocks
- Regional banks
- Specialty companies
- REIT sector stocks
- Utilities sector stocks
- Complete materials sector

---

## 🎨 Custom Watchlist

Want to create your own list?

### Option 1: Edit config.py directly
```python
WATCHLIST = [
    'AAPL', 'MSFT', 'GOOGL',  # Your favorites
    'TSLA', 'NVDA', 'AMD',    # Tech picks
    'JPM', 'BAC', 'GS',       # Finance
    # Add any ticker you want!
]
```

### Option 2: Use Portfolio Watchlists
Create custom lists in the dashboard sidebar:
1. Click "📁 My Watchlists"
2. Create new watchlist
3. Add stocks dynamically

---

## 🚀 Data Collection

### First Time Setup:
```bash
cd ~/Documents/Projects/stock-analysis-tool
source venv/bin/activate
python src/data_collector.py
```

**Top 100**: ~2-3 minutes  
**All 500**: ~8-12 minutes

### Update Data:
Use the dashboard buttons:
- "🔄 Update Data" - Single stock
- "🔄 Update All Stocks" - Entire watchlist

---

## 💡 Recommendations

### For Most Users:
**Use Top 100** - It includes all major companies you'll likely trade.

### Use All 500+ if:
- You trade small/mid-cap stocks
- You need complete sector coverage  
- You're doing sector rotation strategies
- You want to scan the entire S&P 500

### Performance Tips:
1. Start with Top 100
2. Use portfolio watchlists for specific groups
3. Only switch to All 500 if you need full coverage
4. Update data during off-hours (less API load)

---

## 📝 Stock List Details

### Top 100 Tickers (Alphabetical):
```
AAPL, ABBV, ABT, ACN, ADBE, ADI, ADP, AMAT, AMGN, AMZN, AVGO, AXP,
BA, BAC, BDX, BLK, BKNG, BMY, BRK.B, BSX, C, CAT, CB, CMCSA, COP,
COST, CRM, CSCO, CVS, CVX, DE, DHR, DIS, DUK, ELV, EOG, GE, GILD,
GS, HD, HON, IBM, INTC, INTU, ISRG, ITW, JNJ, JPM, KO, LIN, LLY,
LOW, LMT, MA, MCD, MDLZ, MDT, META, MMC, MO, MRK, MS, MSFT, NEE,
NFLX, NKE, NVDA, ORCL, PEP, PFE, PG, PGR, PLD, PM, QCOM, REGN,
RTX, SBUX, SCHW, SLB, SO, SPGI, SBUX, SYK, T, TJX, TMO, TMUS,
TXN, UNH, UNP, V, VRTX, VZ, WFC, WMT, XOM, ZTS
```

### Full S&P 500:
Includes all above PLUS 400+ additional companies across all sectors.

---

## 🆘 Troubleshooting

**"Import error: sp500_tickers"**
- File is in your project directory
- Should work automatically
- Fallback list will load if needed

**"Data collection taking too long"**
- Switch to Top 100 in config.py
- Or collect data overnight
- Use "Update Data" for individual stocks

**"Can't find a specific stock"**
- Check if it's in S&P 500
- Use custom watchlist in dashboard
- Or add to config.py manually

---

**You now have 100+ stocks available immediately!** 🎉  
**Switch to 500+ anytime in config.py** ⚡
