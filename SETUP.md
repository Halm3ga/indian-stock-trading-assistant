# Installation & Setup Guide

## Prerequisites

You need Python 3.8 or higher installed on your system.

### Check Python Installation

Open PowerShell and run:
```powershell
python --version
```

If Python is not found, download and install from:
**https://www.python.org/downloads/**

> ⚠️ **Important**: During installation, check "Add Python to PATH"

## Setup Steps

### 1. Install Dependencies

Navigate to the project directory and install required packages:

```powershell
cd c:\Users\Me\Desktop\Files\Python\Trading
pip install -r requirements.txt
```

This will install:
- `yfinance` - For downloading market data from Yahoo Finance
- `pandas` - For data manipulation
- `pandas-ta` - For technical indicators
- `streamlit` - For web dashboard
- `plotly` - For interactive charts
- `matplotlib` - For additional plotting

### 2. Test Data Download

Verify that data downloading works:

```powershell
python data_loader.py
```

Expected output:
- ✓ Downloads NIFTY 50 data (10 years)
- ✓ Downloads RELIANCE stock data
- ✓ Creates `data_cache/` folder with CSV files

### 3. Test Strategies

Run the backtesting module:

```powershell
python strategies.py
```

Expected output:
- Performance metrics for SMA strategy
- Performance metrics for RSI strategy
- Performance metrics for Combined strategy
- Current trading signals for each strategy

### 4. Launch Dashboard

Start the Streamlit web application:

```powershell
streamlit run app.py
```

The dashboard will automatically open in your browser at:
**http://localhost:8501**

## Usage

### Dashboard Features

1. **Sidebar Settings**:
   - Select stock/index (NIFTY50, RELIANCE, TCS, etc.)
   - Choose strategy (SMA, RSI, or Combined)
   - Adjust strategy parameters
   - Set initial capital and time period

2. **Main View**:
   - Current market metrics (price, volume, 52W high/low)
   - **Trading Signal**: BUY/SELL/HOLD recommendation
   - Backtest performance metrics
   - Interactive price chart with indicators
   - Portfolio value over time

3. **Refresh Data**: Click "🔄 Refresh Data" to get latest quotes

### Available Tickers

**Indices:**
- NIFTY50 - Nifty 50 Index
- BANKNIFTY - Bank Nifty Index
- SENSEX - BSE Sensex

**Stocks (add .NS for custom stocks):**
- RELIANCE, TCS, INFY (Infosys)
- HDFC (HDFC Bank), ICICI (ICICI Bank)
- ITC, SBIN (State Bank), WIPRO
- BHARTIARTL (Airtel), KOTAKBANK
- LT (L&T), HINDUNILVR

### Custom Tickers

To add any NSE stock, use format: `SYMBOL.NS`
Example: `TATAMOTORS.NS`

## Troubleshooting

### Python not found
- Reinstall Python from https://www.python.org/
- Ensure "Add to PATH" is checked during installation
- Restart PowerShell after installation

### pip not working
```powershell
python -m pip install -r requirements.txt
```

### Streamlit won't start
```powershell
python -m streamlit run app.py
```

### No data downloaded
- Check internet connection
- Verify ticker symbol is correct (add .NS for NSE stocks)
- Yahoo Finance may have temporary outages

### Module not found errors
```powershell
pip install --upgrade -r requirements.txt
```

## Data Sources

- **Yahoo Finance** (https://finance.yahoo.com/)
  - Free historical data
  - 15-20 minute delay for real-time quotes
  - 10+ years of historical data available

## Next Steps

1. ✅ Experiment with different strategies and parameters
2. ✅ Test on multiple stocks to find what works best
3. ✅ Use backtesting results to validate strategies
4. ⚠️ **Remember**: Past performance doesn't guarantee future results
5. ⚠️ **Trading Risk**: Always do your own research before trading

## Optional Enhancements

Want to extend the app? Consider:
- Adding more technical indicators (MACD, Bollinger Bands)
- Implementing stop-loss/take-profit rules
- Creating custom alert notifications
- Exporting backtest results to CSV
- Adding sector rotation strategies
