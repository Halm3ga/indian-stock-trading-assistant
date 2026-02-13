# Indian Stock Trading Analysis & Strategy App

A comprehensive Python-based trading assistant for the Indian stock market (NSE/BSE) with backtesting and real-time analysis capabilities.

## Features
- 📊 **10 Years Historical Data** from Yahoo Finance for NSE/BSE stocks
- 🎯 **Trading Strategies**: Moving Average Crossover, RSI-based strategies
- 📈 **Backtesting Engine** to test strategies on historical data
- 🖥️ **Interactive Dashboard** built with Streamlit
- 🚦 **Real-time Signals**: BUY, SELL, or HOLD recommendations

## Installation

### Prerequisites
- Python 3.8 or higher

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Test Data Download
```bash
python data_loader.py
```

### 2. Run Backtesting
```bash
python strategies.py
```

### 3. Launch Dashboard
```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

## Supported Instruments

### Indices
- **NIFTY 50** (^NSEI)
- **Bank Nifty** (^NSEBANK)
- **Sensex** (^BSESN)

### Popular Stocks
- Reliance, TCS, Infosys, HDFC Bank, ICICI Bank
- ITC, SBI, Wipro, Bharti Airtel, Kotak Bank
- L&T, Hindustan Unilever, and more

## Data Source
- **Yahoo Finance API** via `yfinance` library
- URL: https://finance.yahoo.com/

## Project Structure
```
Trading/
├── data_loader.py      # Data fetching and caching
├── strategies.py       # Trading strategies and backtesting
├── app.py             # Streamlit dashboard
├── requirements.txt   # Python dependencies
└── data_cache/        # Cached historical data
```

## Notes
- Data is cached locally to minimize API calls
- Cache refreshes daily automatically
- Free data source with slight delay for real-time quotes
- Deployed app link: https://indian-stock-trading-assistant-kcmjicwr4bh9vm4cjbnnf8.streamlit.app/
