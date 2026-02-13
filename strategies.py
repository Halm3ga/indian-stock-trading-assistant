"""
Trading Strategies and Backtesting Engine
Implements various trading strategies for Indian stock market
"""
import pandas as pd
import numpy as np
from data_loader import IndianMarketDataLoader
from datetime import datetime


class TradingStrategy:
    """Base class for trading strategies"""
    
    def __init__(self, data):
        """
        Initialize strategy with historical data
        
        Args:
            data: DataFrame with OHLCV data
        """
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        self.signals['price'] = data['Close']
        self.signals['signal'] = 0  # 0: hold, 1: buy, -1: sell
        self.signals['position'] = 0  # Current position
        
    def generate_signals(self):
        """Generate trading signals - to be implemented by subclasses"""
        raise NotImplementedError
        
    def backtest(self, initial_capital=100000):
        """
        Backtest the strategy
        
        Args:
            initial_capital: Starting capital in INR
            
        Returns:
            Dictionary with performance metrics
        """
        self.generate_signals()
        
        # Calculate position (1 = long, 0 = flat)
        self.signals['position'] = self.signals['signal'].replace(-1, 0).cumsum()
        
        # Calculate returns
        self.signals['market_return'] = self.signals['price'].pct_change()
        self.signals['strategy_return'] = self.signals['position'].shift(1) * self.signals['market_return']
        
        # Calculate cumulative returns
        self.signals['cumulative_market'] = (1 + self.signals['market_return']).cumprod()
        self.signals['cumulative_strategy'] = (1 + self.signals['strategy_return']).cumprod()
        
        # Calculate portfolio value
        self.signals['portfolio_value'] = initial_capital * self.signals['cumulative_strategy']
        
        # Performance metrics
        total_return = (self.signals['portfolio_value'].iloc[-1] - initial_capital) / initial_capital * 100
        
        # Win rate
        winning_trades = self.signals[self.signals['strategy_return'] > 0]
        total_trades = self.signals[self.signals['signal'] != 0]
        win_rate = len(winning_trades) / len(total_trades) * 100 if len(total_trades) > 0 else 0
        
        # Max drawdown
        cumulative = self.signals['cumulative_strategy']
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # Sharpe ratio (assuming 252 trading days, 6% risk-free rate)
        risk_free_rate = 0.06
        excess_returns = self.signals['strategy_return'] - risk_free_rate/252
        sharpe_ratio = np.sqrt(252) * excess_returns.mean() / excess_returns.std() if excess_returns.std() != 0 else 0
        
        return {
            'total_return': total_return,
            'win_rate': win_rate,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'final_value': self.signals['portfolio_value'].iloc[-1],
            'total_trades': len(total_trades),
            'signals_df': self.signals
        }
    
    def get_current_signal(self):
        """Get the most recent trading signal"""
        if len(self.signals) == 0:
            self.generate_signals()
        
        latest_signal = self.signals['signal'].iloc[-1]
        latest_price = self.signals['price'].iloc[-1]
        
        signal_map = {1: 'BUY', -1: 'SELL', 0: 'HOLD'}
        return {
            'signal': signal_map.get(latest_signal, 'HOLD'),
            'price': latest_price,
            'date': self.signals.index[-1]
        }


class SMAStrategy(TradingStrategy):
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self, data, short_window=50, long_window=200):
        """
        Initialize SMA strategy
        
        Args:
            data: OHLCV DataFrame
            short_window: Short-term SMA period
            long_window: Long-term SMA period
        """
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self):
        """Generate signals based on SMA crossover"""
        # Calculate moving averages
        self.signals['short_ma'] = self.signals['price'].rolling(window=self.short_window).mean()
        self.signals['long_ma'] = self.signals['price'].rolling(window=self.long_window).mean()
        
        # Generate signals
        # Buy when short MA crosses above long MA
        # Sell when short MA crosses below long MA
        self.signals['signal'] = 0
        self.signals.loc[self.signals['short_ma'] > self.signals['long_ma'], 'signal'] = 1
        self.signals.loc[self.signals['short_ma'] < self.signals['long_ma'], 'signal'] = -1
        
        # Only trigger on crossover (change in signal)
        self.signals['signal'] = self.signals['signal'].diff()
        self.signals['signal'].fillna(0, inplace=True)


class RSIStrategy(TradingStrategy):
    """Relative Strength Index Strategy"""
    
    def __init__(self, data, rsi_period=14, oversold=30, overbought=70):
        """
        Initialize RSI strategy
        
        Args:
            data: OHLCV DataFrame
            rsi_period: RSI calculation period
            oversold: Oversold threshold (buy signal)
            overbought: Overbought threshold (sell signal)
        """
        super().__init__(data)
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def generate_signals(self):
        """Generate signals based on RSI"""
        # Calculate RSI
        delta = self.signals['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        
        rs = gain / loss
        self.signals['rsi'] = 100 - (100 / (1 + rs))
        
        # Generate signals
        self.signals['signal'] = 0
        
        # Buy when RSI crosses above oversold
        self.signals.loc[
            (self.signals['rsi'] < self.oversold) & 
            (self.signals['rsi'].shift(1) >= self.oversold), 
            'signal'
        ] = 1
        
        # Sell when RSI crosses above overbought
        self.signals.loc[
            (self.signals['rsi'] > self.overbought) & 
            (self.signals['rsi'].shift(1) <= self.overbought), 
            'signal'
        ] = -1


class CombinedStrategy(TradingStrategy):
    """Combined SMA + RSI Strategy"""
    
    def __init__(self, data, short_window=50, long_window=200, rsi_period=14, oversold=30, overbought=70):
        """Initialize combined strategy"""
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def generate_signals(self):
        """Generate signals based on both SMA and RSI"""
        # Calculate SMA
        self.signals['short_ma'] = self.signals['price'].rolling(window=self.short_window).mean()
        self.signals['long_ma'] = self.signals['price'].rolling(window=self.long_window).mean()
        
        # Calculate RSI
        delta = self.signals['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
        rs = gain / loss
        self.signals['rsi'] = 100 - (100 / (1 + rs))
        
        # Generate signals - both conditions must be met
        self.signals['signal'] = 0
        
        # Buy: Short MA > Long MA AND RSI oversold
        self.signals.loc[
            (self.signals['short_ma'] > self.signals['long_ma']) & 
            (self.signals['rsi'] < self.oversold),
            'signal'
        ] = 1
        
        # Sell: Short MA < Long MA OR RSI overbought
        self.signals.loc[
            (self.signals['short_ma'] < self.signals['long_ma']) | 
            (self.signals['rsi'] > self.overbought),
            'signal'
        ] = -1
        
        # Only trigger on signal change
        self.signals['signal'] = self.signals['signal'].diff()
        self.signals['signal'].fillna(0, inplace=True)


def main():
    """Test strategies"""
    print("=" * 70)
    print("TESTING TRADING STRATEGIES")
    print("=" * 70)
    
    # Load data
    loader = IndianMarketDataLoader()
    print("\n📊 Loading NIFTY 50 data (10 years)...")
    nifty_data = loader.download_data('NIFTY50', period='10y')
    
    if nifty_data.empty:
        print("❌ Failed to load data")
        return
    
    print(f"✓ Loaded {len(nifty_data)} days of data")
    print(f"  Date range: {nifty_data.index[0].date()} to {nifty_data.index[-1].date()}")
    
    initial_capital = 100000  # 1 Lakh INR
    
    # Test SMA Strategy
    print("\n" + "=" * 70)
    print("1. SIMPLE MOVING AVERAGE (SMA) STRATEGY")
    print("   Golden Cross: 50-day crosses above 200-day MA")
    print("=" * 70)
    
    sma_strategy = SMAStrategy(nifty_data, short_window=50, long_window=200)
    sma_results = sma_strategy.backtest(initial_capital)
    
    print(f"\n📈 Performance Metrics:")
    print(f"   Initial Capital:  ₹{initial_capital:,.2f}")
    print(f"   Final Value:      ₹{sma_results['final_value']:,.2f}")
    print(f"   Total Return:     {sma_results['total_return']:.2f}%")
    print(f"   Win Rate:         {sma_results['win_rate']:.2f}%")
    print(f"   Max Drawdown:     {sma_results['max_drawdown']:.2f}%")
    print(f"   Sharpe Ratio:     {sma_results['sharpe_ratio']:.2f}")
    print(f"   Total Trades:     {sma_results['total_trades']}")
    
    current_signal = sma_strategy.get_current_signal()
    print(f"\n🚦 Current Signal: {current_signal['signal']} @ ₹{current_signal['price']:.2f}")
    
    # Test RSI Strategy
    print("\n" + "=" * 70)
    print("2. RSI (RELATIVE STRENGTH INDEX) STRATEGY")
    print("   Buy: RSI < 30 (oversold), Sell: RSI > 70 (overbought)")
    print("=" * 70)
    
    rsi_strategy = RSIStrategy(nifty_data, rsi_period=14, oversold=30, overbought=70)
    rsi_results = rsi_strategy.backtest(initial_capital)
    
    print(f"\n📈 Performance Metrics:")
    print(f"   Initial Capital:  ₹{initial_capital:,.2f}")
    print(f"   Final Value:      ₹{rsi_results['final_value']:,.2f}")
    print(f"   Total Return:     {rsi_results['total_return']:.2f}%")
    print(f"   Win Rate:         {rsi_results['win_rate']:.2f}%")
    print(f"   Max Drawdown:     {rsi_results['max_drawdown']:.2f}%")
    print(f"   Sharpe Ratio:     {rsi_results['sharpe_ratio']:.2f}")
    print(f"   Total Trades:     {rsi_results['total_trades']}")
    
    current_signal = rsi_strategy.get_current_signal()
    print(f"\n🚦 Current Signal: {current_signal['signal']} @ ₹{current_signal['price']:.2f}")
    
    # Test Combined Strategy
    print("\n" + "=" * 70)
    print("3. COMBINED SMA + RSI STRATEGY")
    print("   Entry when both SMA and RSI conditions align")
    print("=" * 70)
    
    combined_strategy = CombinedStrategy(nifty_data)
    combined_results = combined_strategy.backtest(initial_capital)
    
    print(f"\n📈 Performance Metrics:")
    print(f"   Initial Capital:  ₹{initial_capital:,.2f}")
    print(f"   Final Value:      ₹{combined_results['final_value']:,.2f}")
    print(f"   Total Return:     {combined_results['total_return']:.2f}%")
    print(f"   Win Rate:         {combined_results['win_rate']:.2f}%")
    print(f"   Max Drawdown:     {combined_results['max_drawdown']:.2f}%")
    print(f"   Sharpe Ratio:     {combined_results['sharpe_ratio']:.2f}")
    print(f"   Total Trades:     {combined_results['total_trades']}")
    
    current_signal = combined_strategy.get_current_signal()
    print(f"\n🚦 Current Signal: {current_signal['signal']} @ ₹{current_signal['price']:.2f}")
    
    print("\n" + "=" * 70)
    print("✅ STRATEGY TESTING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
