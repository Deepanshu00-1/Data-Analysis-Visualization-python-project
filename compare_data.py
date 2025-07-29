import pandas as pd
import numpy as np

def compare_original_and_cleaned_data():
    """
    Compare the original and cleaned data to verify the cleaning process.
    """
    try:
        print("="*80)
        print("COMPARING ORIGINAL vs CLEANED DATA")
        print("="*80)
        
        # Load original data
        print("Loading original data...")
        original_data = pd.read_csv('data/AAPL_historical_data.csv')
        original_data['date'] = pd.to_datetime(original_data['date'], utc=True)
        original_data = original_data.set_index('date')
        
        # Load cleaned data
        print("Loading cleaned data...")
        cleaned_data = pd.read_csv('data/AAPL_cleaned_data.csv')
        cleaned_data['date'] = pd.to_datetime(cleaned_data['date'], utc=True)
        cleaned_data = cleaned_data.set_index('date')
        
        print(f"\nOriginal data shape: {original_data.shape}")
        print(f"Cleaned data shape: {cleaned_data.shape}")
        
        # Compare basic statistics
        print("\n" + "="*80)
        print("BASIC COMPARISON")
        print("="*80)
        
        price_columns = ['open', 'high', 'low', 'close']
        
        print("Price Statistics Comparison:")
        print("-" * 40)
        
        for col in price_columns:
            orig_mean = original_data[col].mean()
            clean_mean = cleaned_data[col].mean()
            orig_std = original_data[col].std()
            clean_std = cleaned_data[col].std()
            
            print(f"{col.upper()}:")
            print(f"  Original - Mean: ${orig_mean:.2f}, Std: ${orig_std:.2f}")
            print(f"  Cleaned  - Mean: ${clean_mean:.2f}, Std: ${clean_std:.2f}")
            print(f"  Difference - Mean: ${clean_mean - orig_mean:.6f}, Std: ${clean_std - orig_std:.6f}")
            print()
        
        # Volume comparison
        orig_vol_mean = original_data['volume'].mean()
        clean_vol_mean = cleaned_data['volume'].mean()
        orig_vol_std = original_data['volume'].std()
        clean_vol_std = cleaned_data['volume'].std()
        
        print("Volume Statistics:")
        print(f"  Original - Mean: {orig_vol_mean:,.0f}, Std: {orig_vol_std:,.0f}")
        print(f"  Cleaned  - Mean: {clean_vol_mean:,.0f}, Std: {clean_vol_std:,.0f}")
        print(f"  Difference - Mean: {clean_vol_mean - orig_vol_mean:,.0f}, Std: {clean_vol_std - orig_vol_std:,.0f}")
        
        # Check for missing values
        print("\n" + "="*80)
        print("MISSING VALUES COMPARISON")
        print("="*80)
        
        orig_missing = original_data.isnull().sum()
        clean_missing = cleaned_data.isnull().sum()
        
        print("Missing values by column:")
        for col in original_data.columns:
            orig_count = orig_missing[col]
            clean_count = clean_missing[col]
            print(f"  {col}: Original={orig_count}, Cleaned={clean_count}")
        
        # Date range comparison
        print("\n" + "="*80)
        print("DATE RANGE COMPARISON")
        print("="*80)
        
        print(f"Original date range: {original_data.index.min()} to {original_data.index.max()}")
        print(f"Cleaned date range: {cleaned_data.index.min()} to {cleaned_data.index.max()}")
        print(f"Original trading days: {len(original_data)}")
        print(f"Cleaned trading days: {len(cleaned_data)}")
        
        # Data quality checks
        print("\n" + "="*80)
        print("DATA QUALITY COMPARISON")
        print("="*80)
        
        # Check for negative prices
        orig_negative = (original_data[price_columns] <= 0).any().any()
        clean_negative = (cleaned_data[price_columns] <= 0).any().any()
        print(f"Negative prices - Original: {'Yes' if orig_negative else 'No'}, Cleaned: {'Yes' if clean_negative else 'No'}")
        
        # Check for zero volume
        orig_zero_vol = (original_data['volume'] <= 0).any()
        clean_zero_vol = (cleaned_data['volume'] <= 0).any()
        print(f"Zero volume - Original: {'Yes' if orig_zero_vol else 'No'}, Cleaned: {'Yes' if clean_zero_vol else 'No'}")
        
        # Check data consistency
        orig_consistent = (original_data['high'] >= original_data['low']).all()
        clean_consistent = (cleaned_data['high'] >= cleaned_data['low']).all()
        print(f"High >= Low - Original: {'Yes' if orig_consistent else 'No'}, Cleaned: {'Yes' if clean_consistent else 'No'}")
        
        # Check for duplicate dates
        orig_duplicates = original_data.index.duplicated().any()
        clean_duplicates = cleaned_data.index.duplicated().any()
        print(f"Duplicate dates - Original: {'Yes' if orig_duplicates else 'No'}, Cleaned: {'Yes' if clean_duplicates else 'No'}")
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        if len(original_data) == len(cleaned_data):
            print("✅ Data length preserved during cleaning")
        else:
            print(f"⚠️ Data length changed: {len(original_data)} → {len(cleaned_data)}")
        
        if clean_missing.sum() == 0:
            print("✅ All missing values successfully handled")
        else:
            print(f"⚠️ {clean_missing.sum()} missing values remain")
        
        if not clean_negative and not clean_zero_vol and clean_consistent and not clean_duplicates:
            print("✅ All data quality checks passed for cleaned data")
        else:
            print("⚠️ Some data quality issues remain in cleaned data")
        
        print("\n" + "="*80)
        print("COMPARISON COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"Error comparing data: {str(e)}")

if __name__ == "__main__":
    print("Step 3: Data Comparison")
    print("="*80)
    
    # Compare original and cleaned data
    compare_original_and_cleaned_data() 