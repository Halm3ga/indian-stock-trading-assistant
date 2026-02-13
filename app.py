"""
Indian Stock Trading Dashboard
Interactive Streamlit app for trading analysis and signals
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime, timedelta
from data_loader import IndianMarketDataLoader
from strategies import SMAStrategy, RSIStrategy, CombinedStrategy


# Page configuration
st.set_page_config(
    page_title="Indian Stock Trading Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .signal-buy {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .signal-sell {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .signal-hold {
        background: linear-gradient(135deg, #FFB75E 0%, #ED8F03 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(ticker, period='10y'):
    """Load historical data with caching"""
    loader = IndianMarketDataLoader()
    return loader.download_data(ticker, period=period)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_latest_data(ticker, days=30):
    """Load latest data for current signals"""
    loader = IndianMarketDataLoader()
    return loader.get_latest_data(ticker, days=days)


def create_price_chart(data, strategy_results=None, strategy_name=""):
    """Create interactive price chart with indicators"""
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.7, 0.3],
        subplot_titles=('Price & Indicators', 'Portfolio Value')
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Add strategy indicators if available
    if strategy_results is not None:
        signals_df = strategy_results['signals_df']
        
        # Add moving averages or RSI based on strategy
        if 'short_ma' in signals_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=signals_df.index,
                    y=signals_df['short_ma'],
                    name='Short MA',
                    line=dict(color='orange', width=1)
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=signals_df.index,
                    y=signals_df['long_ma'],
                    name='Long MA',
                    line=dict(color='blue', width=1)
                ),
                row=1, col=1
            )
        
        # Add buy/sell markers
        buy_signals = signals_df[signals_df['signal'] == 1]
        sell_signals = signals_df[signals_df['signal'] == -1]
        
        if len(buy_signals) > 0:
            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['price'],
                    mode='markers',
                    name='Buy Signal',
                    marker=dict(color='green', size=10, symbol='triangle-up')
                ),
                row=1, col=1
            )
        
        if len(sell_signals) > 0:
            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals['price'],
                    mode='markers',
                    name='Sell Signal',
                    marker=dict(color='red', size=10, symbol='triangle-down')
                ),
                row=1, col=1
            )
        
        # Portfolio value
        fig.add_trace(
            go.Scatter(
                x=signals_df.index,
                y=signals_df['portfolio_value'],
                name='Portfolio Value',
                fill='tonexty',
                line=dict(color='#4ECDC4', width=2)
            ),
            row=2, col=1
        )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        template='plotly_dark',
        hovermode='x unified'
    )
    
    return fig


def display_signal(signal_info):
    """Display trading signal with styled box"""
    signal = signal_info['signal']
    
    if signal == 'BUY':
        st.markdown(f'<div class="signal-buy">🚀 BUY SIGNAL<br/>₹{signal_info["price"]:.2f}</div>', unsafe_allow_html=True)
    elif signal == 'SELL':
        st.markdown(f'<div class="signal-sell">⚠️ SELL SIGNAL<br/>₹{signal_info["price"]:.2f}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="signal-hold">⏸️ HOLD<br/>₹{signal_info["price"]:.2f}</div>', unsafe_allow_html=True)


def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">📈 Indian Stock Trading Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # Ticker selection
    loader = IndianMarketDataLoader()
    ticker_options = list(loader.popular_tickers.keys())
    selected_ticker = st.sidebar.selectbox(
        "Select Stock/Index",
        ticker_options,
        index=0
    )
    
    # Strategy selection
    strategy_type = st.sidebar.selectbox(
        "Select Strategy",
        ["SMA Crossover", "RSI", "Combined (SMA + RSI)"]
    )
    
    # Strategy parameters
    st.sidebar.subheader("Strategy Parameters")
    
    if strategy_type in ["SMA Crossover", "Combined (SMA + RSI)"]:
        short_window = st.sidebar.slider("Short MA Period", 10, 100, 50)
        long_window = st.sidebar.slider("Long MA Period", 100, 300, 200)
    
    if strategy_type in ["RSI", "Combined (SMA + RSI)"]:
        rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)
        oversold = st.sidebar.slider("Oversold Level", 20, 40, 30)
        overbought = st.sidebar.slider("Overbought Level", 60, 80, 70)
    
    # Backtest parameters
    st.sidebar.subheader("Backtesting")
    initial_capital = st.sidebar.number_input(
        "Initial Capital (₹)",
        min_value=10000,
        max_value=10000000,
        value=100000,
        step=10000
    )
    
    period = st.sidebar.selectbox(
        "Historical Period",
        ["1y", "2y", "5y", "10y"],
        index=3
    )
    
    # Load data button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Main content
    try:
        with st.spinner(f'Loading {selected_ticker} data...'):
            data = load_data(selected_ticker, period=period)
        
        if data.empty:
            st.error(f"❌ No data available for {selected_ticker}")
            return
        
        # Display current market info
        col1, col2, col3, col4 = st.columns(4)
        
        latest_price = float(data['Close'].iloc[-1])
        prev_close = float(data['Close'].iloc[-2])
        change = latest_price - prev_close
        change_pct = (change / prev_close) * 100
        
        with col1:
            st.metric(
                "Current Price",
                f"₹{latest_price:.2f}",
                f"{change:+.2f} ({change_pct:+.2f}%)"
            )
        
        with col2:
            st.metric("Volume", f"{float(data['Volume'].iloc[-1]):,.0f}")
        
        with col3:
            high_52w = float(data['High'].tail(252).max())
            st.metric("52W High", f"₹{high_52w:.2f}")
        
        with col4:
            low_52w = float(data['Low'].tail(252).min())
            st.metric("52W Low", f"₹{low_52w:.2f}")
        
        st.markdown("---")
        
        # Initialize strategy
        with st.spinner('Running backtest...'):
            if strategy_type == "SMA Crossover":
                strategy = SMAStrategy(data, short_window=short_window, long_window=long_window)
            elif strategy_type == "RSI":
                strategy = RSIStrategy(data, rsi_period=rsi_period, oversold=oversold, overbought=overbought)
            else:
                strategy = CombinedStrategy(
                    data,
                    short_window=short_window,
                    long_window=long_window,
                    rsi_period=rsi_period,
                    oversold=oversold,
                    overbought=overbought
                )
            
            results = strategy.backtest(initial_capital=initial_capital)
            current_signal = strategy.get_current_signal()
        
        # Display current signal
        st.subheader("🚦 Current Trading Signal")
        display_signal(current_signal)
        
        st.markdown("---")
        
        # Backtest results
        st.subheader(f"📊 Backtest Results ({period})")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Return", f"{results['total_return']:.2f}%")
        
        with col2:
            st.metric("Win Rate", f"{results['win_rate']:.2f}%")
        
        with col3:
            st.metric("Max Drawdown", f"{results['max_drawdown']:.2f}%")
        
        with col4:
            st.metric("Sharpe Ratio", f"{results['sharpe_ratio']:.2f}")
        
        with col5:
            st.metric("Total Trades", f"{results['total_trades']}")
        
        st.markdown("---")
        
        # Price chart
        st.subheader("📈 Price Chart & Indicators")
        fig = create_price_chart(data, results, strategy_type)
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional info
        with st.expander("ℹ️ About This Strategy"):
            if strategy_type == "SMA Crossover":
                st.write(f"""
                **Simple Moving Average Crossover Strategy**
                
                - **Buy Signal**: When {short_window}-day MA crosses above {long_window}-day MA (Golden Cross)
                - **Sell Signal**: When {short_window}-day MA crosses below {long_window}-day MA (Death Cross)
                
                This is a trend-following strategy that aims to capture medium to long-term trends.
                """)
            elif strategy_type == "RSI":
                st.write(f"""
                **RSI (Relative Strength Index) Strategy**
                
                - **Buy Signal**: When RSI crosses below {oversold} (oversold condition)
                - **Sell Signal**: When RSI crosses above {overbought} (overbought condition)
                
                RSI measures momentum and helps identify overbought/oversold conditions.
                """)
            else:
                st.write(f"""
                **Combined SMA + RSI Strategy**
                
                - **Buy Signal**: SMA bullish trend AND RSI oversold
                - **Sell Signal**: SMA bearish trend OR RSI overbought
                
                Combines trend-following (SMA) with momentum (RSI) for more reliable signals.
                """)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
