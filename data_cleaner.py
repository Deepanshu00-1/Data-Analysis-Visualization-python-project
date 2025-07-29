import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_and_clean_stock_data(filepath='data/AAPL_historical_data.csv'):
    """
    Load and clean the stock data by handling missing values and ensuring proper datetime indexing.
    
    Args:
        filepath (str): Path to the CSV file containing stock data
    
    Returns:
        pandas.DataFrame: Cleaned stock data with datetime index
    """
    try:
        print(f"Loading data from {filepath}...")
        
        # Load the data
        data = pd.read_csv(filepath)
        
        print(f"Original data shape: {data.shape}")
        print(f"Original columns: {list(data.columns)}")
        
        # Convert date column to datetime
        data['date'] = pd.to_datetime(data['date'], utc=True)
        
        # Set date as index
        data = data.set_index('date')
        
        print(f"\nData after setting datetime index:")
        print(f"Index type: {type(data.index)}")
        print(f"Index range: {data.index.min()} to {data.index.max()}")
        
        return data
        
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

def check_missing_values(data):
    """
    Check for missing values in the dataset.
    
    Args:
        data (pandas.DataFrame): Stock data to check
    
    Returns:
        dict: Summary of missing values
    """
    print("\n" + "="*60)
    print("MISSING VALUES ANALYSIS")
    print("="*60)
    
    # Check for missing values
    missing_data = data.isnull().sum()
    missing_percentage = (missing_data / len(data)) * 100
    
    missing_summary = {}
    
    print("Missing values by column:")
    for column in data.columns:
        missing_count = missing_data[column]
        missing_pct = missing_percentage[column]
        
        if missing_count > 0:
            print(f"  {column}: {missing_count} missing values ({missing_pct:.2f}%)")
            missing_summary[column] = {
                'count': missing_count,
                'percentage': missing_pct
            }
        else:
            print(f"  {column}: No missing values ✓")
            missing_summary[column] = {
                'count': 0,
                'percentage': 0.0
            }
    
    return missing_summary

def clean_missing_values(data, method='forward_fill'):
    """
    Clean missing values using specified method.
    
    Args:
        data (pandas.DataFrame): Stock data to clean
        method (str): Method to handle missing values ('forward_fill', 'backward_fill', 'drop', 'interpolate')
    
    Returns:
        pandas.DataFrame: Cleaned data
    """
    print(f"\nCleaning missing values using method: {method}")
    
    # Store original shape
    original_shape = data.shape
    
    if method == 'forward_fill':
        # Forward fill missing values
        data_cleaned = data.fillna(method='ffill')
        print("Applied forward fill (ffill)")
        
    elif method == 'backward_fill':
        # Backward fill missing values
        data_cleaned = data.fillna(method='bfill')
        print("Applied backward fill (bfill)")
        
    elif method == 'drop':
        # Drop rows with missing values
        data_cleaned = data.dropna()
        print("Dropped rows with missing values")
        
    elif method == 'interpolate':
        # Interpolate missing values
        data_cleaned = data.interpolate(method='linear')
        print("Applied linear interpolation")
        
    else:
        print(f"Unknown method: {method}. Using forward fill.")
        data_cleaned = data.fillna(method='ffill')
    
    # Check if any missing values remain
    remaining_missing = data_cleaned.isnull().sum().sum()
    if remaining_missing > 0:
        print(f"Warning: {remaining_missing} missing values remain after cleaning")
        # Apply forward fill to any remaining missing values
        data_cleaned = data_cleaned.fillna(method='ffill')
        print("Applied additional forward fill to remaining missing values")
    
    print(f"Data shape before cleaning: {original_shape}")
    print(f"Data shape after cleaning: {data_cleaned.shape}")
    print(f"Rows removed: {original_shape[0] - data_cleaned.shape[0]}")
    
    return data_cleaned

def validate_data_quality(data):
    """
    Validate the quality of cleaned data.
    
    Args:
        data (pandas.DataFrame): Cleaned stock data
    
    Returns:
        bool: True if data quality checks pass
    """
    print("\n" + "="*60)
    print("DATA QUALITY VALIDATION")
    print("="*60)
    
    quality_checks = {}
    
    # Check for missing values
    missing_count = data.isnull().sum().sum()
    quality_checks['no_missing_values'] = missing_count == 0
    print(f"No missing values: {'✓' if quality_checks['no_missing_values'] else '✗'} ({missing_count} missing)")
    
    # Check for negative prices
    price_columns = ['open', 'high', 'low', 'close']
    negative_prices = (data[price_columns] <= 0).any().any()
    quality_checks['no_negative_prices'] = not negative_prices
    print(f"No negative prices: {'✓' if quality_checks['no_negative_prices'] else '✗'}")
    
    # Check for zero volume
    zero_volume = (data['volume'] <= 0).any()
    quality_checks['no_zero_volume'] = not zero_volume
    print(f"No zero volume: {'✓' if quality_checks['no_zero_volume'] else '✗'}")
    
    # Check data consistency (high >= low)
    high_low_consistent = (data['high'] >= data['low']).all()
    quality_checks['high_low_consistent'] = high_low_consistent
    print(f"High >= Low for all rows: {'✓' if quality_checks['high_low_consistent'] else '✗'}")
    
    # Check if open and close are within high-low range
    open_in_range = ((data['open'] >= data['low']) & (data['open'] <= data['high'])).all()
    close_in_range = ((data['close'] >= data['low']) & (data['close'] <= data['high'])).all()
    quality_checks['prices_in_range'] = open_in_range and close_in_range
    print(f"Open/Close within High-Low range: {'✓' if quality_checks['prices_in_range'] else '✗'}")
    
    # Check for duplicate dates
    duplicate_dates = data.index.duplicated().any()
    quality_checks['no_duplicate_dates'] = not duplicate_dates
    print(f"No duplicate dates: {'✓' if quality_checks['no_duplicate_dates'] else '✗'}")
    
    # Check if index is sorted
    index_sorted = data.index.is_monotonic_increasing
    quality_checks['index_sorted'] = index_sorted
    print(f"Index is sorted: {'✓' if quality_checks['index_sorted'] else '✗'}")
    
    # Overall quality assessment
    all_checks_passed = all(quality_checks.values())
    print(f"\nOverall data quality: {'✓ PASSED' if all_checks_passed else '✗ FAILED'}")
    
    return all_checks_passed

def save_cleaned_data(data, filename=None):
    """
    Save the cleaned data to a CSV file.
    
    Args:
        data (pandas.DataFrame): Cleaned stock data
        filename (str): Output filename (optional)
    """
    if data is None:
        print("No data to save.")
        return
    
    if filename is None:
        symbol = data['Symbol'].iloc[0] if 'Symbol' in data.columns else 'stock'
        filename = f"data/{symbol}_cleaned_data.csv"
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    try:
        # Reset index to make date a column for CSV
        data_to_save = data.reset_index()
        data_to_save.to_csv(filename, index=False)
        print(f"Cleaned data saved to {filename}")
    except Exception as e:
        print(f"Error saving cleaned data: {str(e)}")

def get_cleaned_data_summary(data):
    """
    Display summary information about the cleaned data.
    
    Args:
        data (pandas.DataFrame): Cleaned stock data
    """
    print("\n" + "="*60)
    print("CLEANED DATA SUMMARY")
    print("="*60)
    
    print(f"Dataset shape: {data.shape}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")
    print(f"Total trading days: {len(data)}")
    print(f"Columns: {list(data.columns)}")
    
    # Basic statistics
    price_columns = ['open', 'high', 'low', 'close']
    print(f"\nPrice statistics:")
    print(data[price_columns].describe())
    
    print(f"\nVolume statistics:")
    print(data['volume'].describe())
    
    # Calculate some metrics
    data['daily_return'] = data['close'].pct_change()
    data['price_range'] = data['high'] - data['low']
    
    print(f"\nKey metrics:")
    print(f"  Average daily return: {data['daily_return'].mean():.4f}")
    print(f"  Daily return volatility: {data['daily_return'].std():.4f}")
    print(f"  Average price range: ${data['price_range'].mean():.2f}")
    print(f"  Total volume: {data['volume'].sum():,}")

if __name__ == "__main__":
    print("Step 3: Data Cleaning")
    print("="*60)
    
    # Load the data
    raw_data = load_and_clean_stock_data()
    
    if raw_data is not None:
        # Check for missing values
        missing_summary = check_missing_values(raw_data)
        
        # Clean missing values
        cleaned_data = clean_missing_values(raw_data, method='forward_fill')
        
        # Validate data quality
        quality_passed = validate_data_quality(cleaned_data)
        
        # Get summary of cleaned data
        get_cleaned_data_summary(cleaned_data)
        
        # Save cleaned data
        save_cleaned_data(cleaned_data)
        
        print("\n" + "="*60)
        if quality_passed:
            print("✅ Step 3 Complete: Data cleaned successfully!")
        else:
            print("⚠️ Step 3 Complete: Data cleaned but quality issues remain!")
        print("="*60)
    else:
        print("❌ Failed to load data for cleaning.") 