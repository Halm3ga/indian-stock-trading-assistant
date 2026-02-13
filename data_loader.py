"""
Data Loader for Indian Stock Market Data
Downloads historical data from NSE using yfinance
"""
import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import os


class IndianMarketDataLoader:
    """Handles downloading and caching of Indian market data"""
    
    def __init__(self, cache_dir="data_cache"):
        """
        Initialize the data loader
        
        Args:
            cache_dir: Directory to cache downloaded data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Common Indian market tickers
        self.popular_tickers = {
            'NIFTY50': '^NSEI',
            'BANKNIFTY': '^NSEBANK',
            'SENSEX': '^BSESN',
            'RELIANCE': 'RELIANCE.NS',
            'TCS': 'TCS.NS',
            'INFY': 'INFY.NS',
            'HDFC': 'HDFCBANK.NS',
            'ICICI': 'ICICIBANK.NS',
            'ITC': 'ITC.NS',
            'SBIN': 'SBIN.NS',
            'WIPRO': 'WIPRO.NS',
            'BHARTIARTL': 'BHARTIARTL.NS',
            'KOTAKBANK': 'KOTAKBANK.NS',
            'LT': 'LT.NS',
            'HINDUNILVR': 'HINDUNILVR.NS',
        }
    
    def get_ticker_symbol(self, name):
        """
        Convert common name to Yahoo Finance ticker
        
        Args:
            name: Common name or ticker symbol
            
        Returns:
            Yahoo Finance ticker symbol
        """
        # If it's already a valid ticker format, return as-is
        if '.' in name or '^' in name:
            return name
        
        # Check if it's in our popular tickers
        name_upper = name.upper()
        if name_upper in self.popular_tickers:
            return self.popular_tickers[name_upper]
        
        # Assume it's an NSE stock, append .NS
        return f"{name_upper}.NS"
    
    def download_data(self, ticker, period='10y', use_cache=True):
        """
        Download historical data for a ticker
        
        Args:
            ticker: Stock ticker or common name
            period: Time period (e.g., '10y', '5y', '1y')
            use_cache: Whether to use cached data if available
            
        Returns:
            pandas DataFrame with OHLCV data
        """
        # Convert to proper ticker symbol
        ticker_symbol = self.get_ticker_symbol(ticker)
        
        # Check cache
        cache_file = self.cache_dir / f"{ticker_symbol.replace('^', '').replace('.', '_')}_{period}.csv"
        
        if use_cache and cache_file.exists():
            # Check if cache is recent (less than 1 day old)
            cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            if cache_age < timedelta(days=1):
                print(f"Loading {ticker_symbol} from cache...")
                return pd.read_csv(cache_file, index_col=0, parse_dates=True)
        
        # Download fresh data
        print(f"Downloading {ticker_symbol} data for period {period}...")
        try:
            data = yf.download(ticker_symbol, period=period, progress=False)
            
            if data.empty:
                raise ValueError(f"No data found for {ticker_symbol}")
            
            # Save to cache
            data.to_csv(cache_file)
            print(f"Downloaded {len(data)} rows of data")
            
            return data
            
        except Exception as e:
            print(f"Error downloading {ticker_symbol}: {str(e)}")
            return pd.DataFrame()
    
    def download_multiple(self, tickers, period='10y'):
        """
        Download data for multiple tickers
        
        Args:
            tickers: List of tickers or common names
            period: Time period
            
        Returns:
            Dictionary mapping ticker to DataFrame
        """
        results = {}
        for ticker in tickers:
            data = self.download_data(ticker, period)
            if not data.empty:
                results[ticker] = data
        return results
    
    def get_latest_data(self, ticker, days=30):
        """
        Get most recent data for real-time analysis
        
        Args:
            ticker: Stock ticker or common name
            days: Number of recent days to fetch
            
        Returns:
            pandas DataFrame
        """
        ticker_symbol = self.get_ticker_symbol(ticker)
        print(f"Fetching latest {days} days for {ticker_symbol}...")
        
        data = yf.download(ticker_symbol, period=f'{days}d', progress=False)
        return data


def main():
    """Test the data loader"""
    loader = IndianMarketDataLoader()
    
    print("=" * 60)
    print("Testing Indian Market Data Loader")
    print("=" * 60)
    
    # Test downloading Nifty 50
    print("\n1. Downloading NIFTY 50 (10 years)...")
    nifty_data = loader.download_data('NIFTY50', period='10y')
    if not nifty_data.empty:
        print(f"   ✓ Success! Got {len(nifty_data)} rows")
        print(f"   Date range: {nifty_data.index[0]} to {nifty_data.index[-1]}")
        print(f"   Columns: {list(nifty_data.columns)}")
        print(f"\n   Latest data:")
        print(nifty_data.tail(3))
    
    # Test downloading a stock
    print("\n2. Downloading RELIANCE (10 years)...")
    reliance_data = loader.download_data('RELIANCE', period='10y')
    if not reliance_data.empty:
        print(f"   ✓ Success! Got {len(reliance_data)} rows")
        print(f"   Current price: ₹{reliance_data['Close'].iloc[-1]:.2f}")
    
    # Test multiple downloads
    print("\n3. Downloading multiple stocks...")
    stocks = ['TCS', 'INFY', 'HDFC']
    data_dict = loader.download_multiple(stocks, period='1y')
    print(f"   ✓ Downloaded {len(data_dict)} stocks")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
