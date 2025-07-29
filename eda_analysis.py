import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

def load_cleaned_data(filepath='data/AAPL_cleaned_data.csv'):
    """
    Load the cleaned stock data for analysis.
    
    Args:
        filepath (str): Path to the cleaned CSV file
    
    Returns:
        pandas.DataFrame: Cleaned stock data with datetime index
    """
    try:
        print(f"Loading cleaned data from {filepath}...")
        
        # Load the data
        data = pd.read_csv(filepath)
        
        # Convert date column to datetime
        data['date'] = pd.to_datetime(data['date'], utc=True)
        
        # Set date as index
        data = data.set_index('date')
        
        print(f"Data loaded successfully!")
        print(f"Shape: {data.shape}")
        print(f"Date range: {data.index.min()} to {data.index.max()}")
        
        return data
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def calculate_moving_averages(data):
    """
    Calculate 50-day and 200-day moving averages for the close price.
    
    Args:
        data (pandas.DataFrame): Stock data with datetime index
    
    Returns:
        pandas.DataFrame: Data with moving averages added
    """
    print("\n" + "="*60)
    print("CALCULATING MOVING AVERAGES")
    print("="*60)
    
    # Create a copy to avoid modifying original data
    data_with_ma = data.copy()
    
    # Calculate moving averages
    data_with_ma['MA_50'] = data_with_ma['close'].rolling(window=50).mean()
    data_with_ma['MA_200'] = data_with_ma['close'].rolling(window=200).mean()
    
    # Calculate percentage difference from moving averages
    data_with_ma['Pct_From_MA50'] = ((data_with_ma['close'] - data_with_ma['MA_50']) / data_with_ma['MA_50']) * 100
    data_with_ma['Pct_From_MA200'] = ((data_with_ma['close'] - data_with_ma['MA_200']) / data_with_ma['MA_200']) * 100
    
    print(f"50-day moving average calculated")
    print(f"200-day moving average calculated")
    print(f"Percentage differences from moving averages calculated")
    
    # Show some statistics
    print(f"\nMoving Average Statistics:")
    print(f"  MA_50 - Mean: ${data_with_ma['MA_50'].mean():.2f}")
    print(f"  MA_200 - Mean: ${data_with_ma['MA_200'].mean():.2f}")
    print(f"  Current price vs MA50: {data_with_ma['Pct_From_MA50'].iloc[-1]:.2f}%")
    print(f"  Current price vs MA200: {data_with_ma['Pct_From_MA200'].iloc[-1]:.2f}%")
    
    return data_with_ma

def calculate_technical_indicators(data):
    """
    Calculate additional technical indicators for analysis.
    
    Args:
        data (pandas.DataFrame): Stock data with moving averages
    
    Returns:
        pandas.DataFrame: Data with technical indicators added
    """
    print("\n" + "="*60)
    print("CALCULATING TECHNICAL INDICATORS")
    print("="*60)
    
    # Create a copy
    data_with_indicators = data.copy()
    
    # Calculate daily returns
    data_with_indicators['daily_return'] = data_with_indicators['close'].pct_change()
    
    # Calculate cumulative returns
    data_with_indicators['cumulative_return'] = (1 + data_with_indicators['daily_return']).cumprod()
    
    # Calculate volatility (rolling 20-day standard deviation)
    data_with_indicators['volatility_20d'] = data_with_indicators['daily_return'].rolling(window=20).std()
    
    # Calculate price range
    data_with_indicators['price_range'] = data_with_indicators['high'] - data_with_indicators['low']
    data_with_indicators['price_range_pct'] = (data_with_indicators['price_range'] / data_with_indicators['close']) * 100
    
    # Calculate volume moving average
    data_with_indicators['volume_ma_20'] = data_with_indicators['volume'].rolling(window=20).mean()
    
    # Calculate RSI (Relative Strength Index) - 14-day
    delta = data_with_indicators['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data_with_indicators['RSI'] = 100 - (100 / (1 + rs))
    
    print("Technical indicators calculated:")
    print("  - Daily returns")
    print("  - Cumulative returns")
    print("  - 20-day volatility")
    print("  - Price range and percentage")
    print("  - 20-day volume moving average")
    print("  - 14-day RSI")
    
    return data_with_indicators

def perform_statistical_analysis(data):
    """
    Perform comprehensive statistical analysis on the stock data.
    
    Args:
        data (pandas.DataFrame): Stock data with indicators
    """
    print("\n" + "="*60)
    print("STATISTICAL ANALYSIS")
    print("="*60)
    
    # Basic statistics
    price_columns = ['open', 'high', 'low', 'close']
    print("Price Statistics:")
    print(data[price_columns].describe())
    
    print("\nVolume Statistics:")
    print(data['volume'].describe())
    
    # Returns analysis
    print("\nReturns Analysis:")
    returns_stats = data['daily_return'].describe()
    print(returns_stats)
    
    # Volatility analysis
    print("\nVolatility Analysis (20-day rolling):")
    vol_stats = data['volatility_20d'].describe()
    print(vol_stats)
    
    # Moving averages analysis
    print("\nMoving Averages Analysis:")
    ma_stats = data[['MA_50', 'MA_200']].describe()
    print(ma_stats)
    
    # Correlation analysis
    print("\nCorrelation Matrix (Price Data):")
    correlation_matrix = data[price_columns + ['volume']].corr()
    print(correlation_matrix)
    
    # Performance metrics
    print("\nPerformance Metrics:")
    total_return = (data['close'].iloc[-1] / data['close'].iloc[0] - 1) * 100
    annualized_return = ((data['close'].iloc[-1] / data['close'].iloc[0]) ** (252/len(data)) - 1) * 100
    sharpe_ratio = data['daily_return'].mean() / data['daily_return'].std() * np.sqrt(252)
    
    print(f"  Total Return: {total_return:.2f}%")
    print(f"  Annualized Return: {annualized_return:.2f}%")
    print(f"  Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"  Max Drawdown: {calculate_max_drawdown(data):.2f}%")
    
    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': calculate_max_drawdown(data)
    }

def calculate_max_drawdown(data):
    """
    Calculate the maximum drawdown of the stock.
    
    Args:
        data (pandas.DataFrame): Stock data
    
    Returns:
        float: Maximum drawdown percentage
    """
    cumulative_returns = data['cumulative_return']
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max * 100
    return drawdown.min()

def create_visualizations(data):
    """
    Create comprehensive visualizations for the stock data.
    
    Args:
        data (pandas.DataFrame): Stock data with indicators
    """
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Create output directory for plots
    os.makedirs('plots', exist_ok=True)
    
    # 1. Price and Moving Averages Chart
    create_price_chart(data)
    
    # 2. Volume Analysis
    create_volume_chart(data)
    
    # 3. Returns Distribution
    create_returns_distribution(data)
    
    # 4. Volatility Analysis
    create_volatility_chart(data)
    
    # 5. Technical Indicators
    create_technical_indicators_chart(data)
    
    # 6. Correlation Heatmap
    create_correlation_heatmap(data)
    
    print("All visualizations created and saved to 'plots' directory!")

def create_price_chart(data):
    """Create price chart with moving averages."""
    plt.figure(figsize=(15, 8))
    
    # Plot price and moving averages
    plt.plot(data.index, data['close'], label='Close Price', linewidth=1, alpha=0.8)
    plt.plot(data.index, data['MA_50'], label='50-day MA', linewidth=2, alpha=0.8)
    plt.plot(data.index, data['MA_200'], label='200-day MA', linewidth=2, alpha=0.8)
    
    plt.title('AAPL Stock Price with Moving Averages', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('plots/price_with_moving_averages.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_volume_chart(data):
    """Create volume analysis chart."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # Volume chart
    ax1.bar(data.index, data['volume'], alpha=0.6, color='skyblue', label='Volume')
    ax1.plot(data.index, data['volume_ma_20'], color='red', linewidth=2, label='20-day Volume MA')
    ax1.set_title('Trading Volume Analysis', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Volume', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Price range chart
    ax2.plot(data.index, data['price_range_pct'], color='green', alpha=0.7)
    ax2.set_title('Daily Price Range (% of Close)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Price Range (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/volume_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_returns_distribution(data):
    """Create returns distribution chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histogram of returns
    ax1.hist(data['daily_return'].dropna(), bins=50, alpha=0.7, color='lightblue', edgecolor='black')
    ax1.set_title('Distribution of Daily Returns', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Daily Return', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Cumulative returns
    ax2.plot(data.index, data['cumulative_return'], linewidth=2, color='green')
    ax2.set_title('Cumulative Returns', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Cumulative Return', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/returns_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_volatility_chart(data):
    """Create volatility analysis chart."""
    plt.figure(figsize=(15, 8))
    
    plt.plot(data.index, data['volatility_20d'], linewidth=2, color='red', alpha=0.8)
    plt.title('20-Day Rolling Volatility', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Volatility (Standard Deviation)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('plots/volatility_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_technical_indicators_chart(data):
    """Create technical indicators chart."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # RSI
    ax1.plot(data.index, data['RSI'], linewidth=2, color='purple', alpha=0.8)
    ax1.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
    ax1.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
    ax1.set_title('Relative Strength Index (RSI)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('RSI', fontsize=12)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Percentage from moving averages
    ax2.plot(data.index, data['Pct_From_MA50'], label='% from MA50', linewidth=2, alpha=0.8)
    ax2.plot(data.index, data['Pct_From_MA200'], label='% from MA200', linewidth=2, alpha=0.8)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.set_title('Percentage Deviation from Moving Averages', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Percentage (%)', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/technical_indicators.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_correlation_heatmap(data):
    """Create correlation heatmap."""
    # Select relevant columns for correlation
    correlation_columns = ['open', 'high', 'low', 'close', 'volume', 'MA_50', 'MA_200', 'daily_return', 'volatility_20d', 'RSI']
    correlation_data = data[correlation_columns].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, square=True, fmt='.2f')
    plt.title('Correlation Matrix of Stock Data', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig('plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def save_analysis_results(data, performance_metrics):
    """
    Save the analysis results to a CSV file.
    
    Args:
        data (pandas.DataFrame): Analyzed stock data
        performance_metrics (dict): Performance metrics
    """
    print("\n" + "="*60)
    print("SAVING ANALYSIS RESULTS")
    print("="*60)
    
    # Create analysis directory
    os.makedirs('analysis', exist_ok=True)
    
    # Save the complete dataset with all indicators
    analysis_file = 'analysis/AAPL_analysis_results.csv'
    data.reset_index().to_csv(analysis_file, index=False)
    print(f"Complete analysis data saved to: {analysis_file}")
    
    # Save performance summary
    summary_file = 'analysis/performance_summary.txt'
    with open(summary_file, 'w') as f:
        f.write("AAPL STOCK ANALYSIS SUMMARY\n")
        f.write("="*50 + "\n\n")
        f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Data Period: {data.index.min()} to {data.index.max()}\n")
        f.write(f"Total Trading Days: {len(data)}\n\n")
        
        f.write("PERFORMANCE METRICS:\n")
        f.write(f"  Total Return: {performance_metrics['total_return']:.2f}%\n")
        f.write(f"  Annualized Return: {performance_metrics['annualized_return']:.2f}%\n")
        f.write(f"  Sharpe Ratio: {performance_metrics['sharpe_ratio']:.4f}\n")
        f.write(f"  Maximum Drawdown: {performance_metrics['max_drawdown']:.2f}%\n\n")
        
        f.write("PRICE STATISTICS:\n")
        price_stats = data[['open', 'high', 'low', 'close']].describe()
        f.write(str(price_stats))
        f.write("\n\n")
        
        f.write("VOLUME STATISTICS:\n")
        volume_stats = data['volume'].describe()
        f.write(str(volume_stats))
        f.write("\n\n")
        
        f.write("RETURNS STATISTICS:\n")
        returns_stats = data['daily_return'].describe()
        f.write(str(returns_stats))
    
    print(f"Performance summary saved to: {summary_file}")

if __name__ == "__main__":
    print("Step 4: Exploratory Data Analysis (EDA)")
    print("="*60)
    
    # Load the cleaned data
    data = load_cleaned_data()
    
    if data is not None:
        # Calculate moving averages
        data_with_ma = calculate_moving_averages(data)
        
        # Calculate technical indicators
        data_with_indicators = calculate_technical_indicators(data_with_ma)
        
        # Perform statistical analysis
        performance_metrics = perform_statistical_analysis(data_with_indicators)
        
        # Create visualizations
        create_visualizations(data_with_indicators)
        
        # Save analysis results
        save_analysis_results(data_with_indicators, performance_metrics)
        
        print("\n" + "="*60)
        print("✅ Step 4 Complete: EDA Analysis completed successfully!")
        print("="*60)
        print("\nFiles created:")
        print("  - analysis/AAPL_analysis_results.csv (Complete dataset with indicators)")
        print("  - analysis/performance_summary.txt (Performance metrics)")
        print("  - plots/ (Directory with all visualizations)")
    else:
        print("❌ Failed to load data for analysis.") 