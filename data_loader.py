import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def load_stock_data(symbol='AAPL', start_date='2018-01-01', end_date='2023-01-01'):
    """
    Download historical stock data using yfinance and store in a Pandas DataFrame.
    
    Args:
        symbol (str): Stock symbol (default: 'AAPL')
        start_date (str): Start date in 'YYYY-MM-DD' format (default: '2018-01-01')
        end_date (str): End date in 'YYYY-MM-DD' format (default: '2023-01-01')
    
    Returns:
        pandas.DataFrame: Historical stock data
    """
    try:
        print(f"Downloading {symbol} stock data from {start_date} to {end_date}...")
        
        # Download stock data using yfinance
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)
        
        # Reset index to make Date a column
        data = data.reset_index()
        
        # Add symbol column
        data['Symbol'] = symbol
        
        # Rename columns for clarity
        data = data.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
            'Dividends': 'dividends',
            'Stock Splits': 'stock_splits'
        })
        
        print(f"Successfully downloaded {len(data)} records for {symbol}")
        print(f"Data shape: {data.shape}")
        print(f"Date range: {data['date'].min()} to {data['date'].max()}")
        
        return data
    
    except Exception as e:
        print(f"Error downloading data for {symbol}: {str(e)}")
        return None

def save_data_to_csv(data, filename=None):
    """
    Save the stock data to a CSV file.
    
    Args:
        data (pandas.DataFrame): Stock data to save
        filename (str): Output filename (optional)
    """
    if data is None:
        print("No data to save.")
        return
    
    if filename is None:
        symbol = data['Symbol'].iloc[0] if 'Symbol' in data.columns else 'stock'
        filename = f"data/{symbol}_historical_data.csv"
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    try:
        data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {str(e)}")

def get_data_info(data):
    """
    Display information about the loaded data.
    
    Args:
        data (pandas.DataFrame): Stock data to analyze
    """
    if data is None:
        print("No data to analyze.")
        return
    
    print("\n" + "="*50)
    print("DATA INFORMATION")
    print("="*50)
    print(f"Shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    print(f"Date range: {data['date'].min()} to {data['date'].max()}")
    print(f"Total trading days: {len(data)}")
    
    print("\nFirst 5 rows:")
    print(data.head())
    
    print("\nData types:")
    print(data.dtypes)
    
    print("\nBasic statistics:")
    numeric_columns = ['open', 'high', 'low', 'close', 'volume']
    print(data[numeric_columns].describe())

if __name__ == "__main__":
    # Load AAPL stock data
    print("Step 2: Loading Stock Data")
    print("="*50)
    
    # Download the data
    stock_data = load_stock_data('AAPL', '2018-01-01', '2023-01-01')
    
    if stock_data is not None:
        # Display data information
        get_data_info(stock_data)
        
        # Save data to CSV
        save_data_to_csv(stock_data)
        
        print("\n" + "="*50)
        print("Step 2 Complete: Data loaded successfully!")
        print("="*50)
    else:
        print("Failed to load stock data.") 