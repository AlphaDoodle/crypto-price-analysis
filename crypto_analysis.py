import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns

def fetch_crypto_data(crypto_symbol, start_date, end_date):
    """
    Fetch historical cryptocurrency data using yfinance
    """
    ticker = yf.Ticker(f"{crypto_symbol}-USD")
    df = ticker.history(start=start_date, end=end_date)
    return df['Close']

def analyze_crypto_prices(start_date, end_date):
    """
    Analyze and compare Bitcoin and Ethereum prices
    """
    # Fetch data
    btc_prices = fetch_crypto_data('BTC', start_date, end_date)
    eth_prices = fetch_crypto_data('ETH', start_date, end_date)
    
    # Combine into a single DataFrame
    df = pd.DataFrame({
        'Bitcoin': btc_prices,
        'Ethereum': eth_prices
    })
    
    # Calculate daily returns
    df_returns = df.pct_change()
    
    # Calculate metrics
    metrics = pd.DataFrame({
        'Metric': ['Mean Daily Return', 'Volatility', 'Max Price', 'Min Price'],
        'Bitcoin': [
            df_returns['Bitcoin'].mean() * 100,
            df_returns['Bitcoin'].std() * 100,
            df['Bitcoin'].max(),
            df['Bitcoin'].min()
        ],
        'Ethereum': [
            df_returns['Ethereum'].mean() * 100,
            df_returns['Ethereum'].std() * 100,
            df['Ethereum'].max(),
            df['Ethereum'].min()
        ]
    })
    
    return df, metrics

def plot_comparison(df, save_path='crypto_comparison.png'):
    """
    Create visualization comparing Bitcoin and Ethereum
    """
    # Set up the plot style
    plt.style.use('seaborn')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot prices
    df.plot(ax=ax1)
    ax1.set_title('Bitcoin vs Ethereum Price Comparison')
    ax1.set_ylabel('Price (USD)')
    ax1.legend(loc='upper left')
    
    # Plot normalized prices
    normalized_df = df / df.iloc[0] * 100
    normalized_df.plot(ax=ax2)
    ax2.set_title('Normalized Price Comparison (First Day = 100)')
    ax2.set_ylabel('Normalized Price')
    ax2.legend(loc='upper left')
    
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    # Set date range for analysis (1 year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Perform analysis
    df, metrics = analyze_crypto_prices(start_date, end_date)
    
    # Create visualization
    plot_comparison(df)
    
    # Print metrics
    print("\nCrypto Comparison Metrics:")
    print(metrics.to_string(index=False))
    
    return df, metrics

if __name__ == "__main__":
    main()