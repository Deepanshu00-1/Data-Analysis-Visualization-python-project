import pandas as pd
import numpy as np
from datetime import datetime

def verify_stock_data(filepath='data/AAPL_historical_data.csv'):
    """
    Verify the quality and completeness of the downloaded stock data.
    
    Args:
        filepath (str): Path to the CSV file containing stock data
    """
    try:
        # Load the data
        print(f"Loading data from {filepath}...")
        data = pd.read_csv(filepath)
        
        # Convert date column to datetime
        data['date'] = pd.to_datetime(data['date'])
        
        print("\n" + "="*60)
        print("DATA VERIFICATION REPORT")
        print("="*60)
        
        # Basic information
        print(f"Dataset shape: {data.shape}")
        print(f"Date range: {data['date'].min()} to {data['date'].max()}")
        print(f"Total trading days: {len(data)}")
        print(f"Symbol: {data['Symbol'].iloc[0]}")
        
        # Check for missing values
        print("\nMissing values:")
        missing_data = data.isnull().sum()
        for column, missing_count in missing_data.items():
            if missing_count > 0:
                print(f"  {column}: {missing_count} missing values")
            else:
                print(f"  {column}: No missing values ✓")
        
        # Check data types
        print("\nData types:")
        for column, dtype in data.dtypes.items():
            print(f"  {column}: {dtype}")
        
        # Price statistics
        price_columns = ['open', 'high', 'low', 'close']
        print(f"\nPrice statistics ({price_columns}):")
        price_stats = data[price_columns].describe()
        print(price_stats)
        
        # Volume statistics
        print(f"\nVolume statistics:")
        volume_stats = data['volume'].describe()
        print(volume_stats)
        
        # Check for data consistency
        print("\nData consistency checks:")
        
        # Check if high >= low for all rows
        high_low_check = (data['high'] >= data['low']).all()
        print(f"  High >= Low for all rows: {'✓' if high_low_check else '✗'}")
        
        # Check if open and close are within high-low range
        open_in_range = ((data['open'] >= data['low']) & (data['open'] <= data['high'])).all()
        close_in_range = ((data['close'] >= data['low']) & (data['close'] <= data['high'])).all()
        print(f"  Open price within high-low range: {'✓' if open_in_range else '✗'}")
        print(f"  Close price within high-low range: {'✓' if close_in_range else '✗'}")
        
        # Check for zero or negative prices
        zero_prices = (data[price_columns] <= 0).any().any()
        print(f"  Zero or negative prices: {'✗' if zero_prices else '✓'}")
        
        # Check for zero volume
        zero_volume = (data['volume'] <= 0).any()
        print(f"  Zero volume days: {'✗' if zero_volume else '✓'}")
        
        # Calculate some basic metrics
        print("\nBasic metrics:")
        data['daily_return'] = data['close'].pct_change()
        data['price_range'] = data['high'] - data['low']
        data['price_range_pct'] = (data['price_range'] / data['close']) * 100
        
        print(f"  Average daily return: {data['daily_return'].mean():.4f}")
        print(f"  Daily return std dev: {data['daily_return'].std():.4f}")
        print(f"  Average price range: ${data['price_range'].mean():.2f}")
        print(f"  Average price range %: {data['price_range_pct'].mean():.2f}%")
        print(f"  Total volume: {data['volume'].sum():,}")
        print(f"  Average volume: {data['volume'].mean():,.0f}")
        
        # Check for dividends and stock splits
        total_dividends = data['dividends'].sum()
        total_splits = data['stock_splits'].sum()
        print(f"  Total dividends: {total_dividends}")
        print(f"  Total stock splits: {total_splits}")
        
        print("\n" + "="*60)
        print("VERIFICATION COMPLETE")
        print("="*60)
        
        return data
        
    except Exception as e:
        print(f"Error verifying data: {str(e)}")
        return None

if __name__ == "__main__":
    print("Step 2: Data Verification")
    print("="*60)
    
    # Verify the downloaded data
    verified_data = verify_stock_data()
    
    if verified_data is not None:
        print("\n✅ Data verification completed successfully!")
        print("The AAPL stock data has been loaded and verified.")
    else:
        print("\n❌ Data verification failed!") 