import pandas as pd
import numpy as np

def preview_stock_data(filepath='data/AAPL_historical_data.csv', num_rows=10):
    """
    Preview the stock data with formatted output.
    
    Args:
        filepath (str): Path to the CSV file
        num_rows (int): Number of rows to display
    """
    try:
        # Load the data
        data = pd.read_csv(filepath)
        
        # Convert date column to datetime
        data['date'] = pd.to_datetime(data['date'], utc=True)
        
        print("="*80)
        print("AAPL STOCK DATA PREVIEW")
        print("="*80)
        print(f"Dataset: {filepath}")
        print(f"Shape: {data.shape[0]} rows × {data.shape[1]} columns")
        print(f"Date range: {data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
        print(f"Symbol: {data['Symbol'].iloc[0]}")
        print("="*80)
        
        # Display first few rows
        print("\nFirst 10 rows:")
        print("-" * 80)
        
        # Format the display
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.float_format', '{:.2f}'.format)
        
        # Select columns to display
        display_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        preview_data = data[display_columns].head(num_rows).copy()
        
        # Format date column
        preview_data['date'] = preview_data['date'].dt.strftime('%Y-%m-%d')
        
        # Format volume column
        preview_data['volume'] = preview_data['volume'].apply(lambda x: f"{x:,}")
        
        print(preview_data.to_string(index=False))
        
        # Display last few rows
        print("\nLast 10 rows:")
        print("-" * 80)
        last_data = data[display_columns].tail(num_rows).copy()
        last_data['date'] = last_data['date'].dt.strftime('%Y-%m-%d')
        last_data['volume'] = last_data['volume'].apply(lambda x: f"{x:,}")
        print(last_data.to_string(index=False))
        
        # Summary statistics
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        
        price_columns = ['open', 'high', 'low', 'close']
        summary_stats = data[price_columns].describe()
        print("\nPrice Statistics:")
        print(summary_stats)
        
        print(f"\nVolume Statistics:")
        volume_stats = data['volume'].describe()
        print(volume_stats)
        
        # Calculate some key metrics
        print("\nKey Metrics:")
        print(f"  Total trading days: {len(data):,}")
        print(f"  Average daily volume: {data['volume'].mean():,.0f}")
        print(f"  Highest price: ${data['high'].max():.2f}")
        print(f"  Lowest price: ${data['low'].min():.2f}")
        print(f"  Price range: ${data['high'].max() - data['low'].min():.2f}")
        
        # Calculate returns
        data['daily_return'] = data['close'].pct_change()
        print(f"  Average daily return: {data['daily_return'].mean():.4f}")
        print(f"  Daily return volatility: {data['daily_return'].std():.4f}")
        
        print("\n" + "="*80)
        print("DATA PREVIEW COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"Error previewing data: {str(e)}")

if __name__ == "__main__":
    print("Step 2: Data Preview")
    print("="*80)
    
    # Preview the downloaded data
    preview_stock_data() 