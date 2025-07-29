import pandas as pd
import numpy as np

def display_analysis_summary():
    """
    Display a comprehensive summary of the EDA analysis results.
    """
    try:
        print("="*80)
        print("AAPL STOCK ANALYSIS SUMMARY")
        print("="*80)
        
        # Load the analysis results
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        
        print(f"Analysis Period: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
        print(f"Total Trading Days: {len(data):,}")
        print(f"Symbol: AAPL (Apple Inc.)")
        
        print("\n" + "="*80)
        print("KEY PERFORMANCE METRICS")
        print("="*80)
        
        # Calculate key metrics
        total_return = (data['close'].iloc[-1] / data['close'].iloc[0] - 1) * 100
        annualized_return = ((data['close'].iloc[-1] / data['close'].iloc[0]) ** (252/len(data)) - 1) * 100
        sharpe_ratio = data['daily_return'].mean() / data['daily_return'].std() * np.sqrt(252)
        
        # Calculate max drawdown
        cumulative_returns = data['cumulative_return']
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        print(f"📈 Total Return: {total_return:.2f}%")
        print(f"📊 Annualized Return: {annualized_return:.2f}%")
        print(f"⚡ Sharpe Ratio: {sharpe_ratio:.4f}")
        print(f"📉 Maximum Drawdown: {max_drawdown:.2f}%")
        
        print("\n" + "="*80)
        print("PRICE ANALYSIS")
        print("="*80)
        
        print(f"💰 Starting Price: ${data['close'].iloc[0]:.2f}")
        print(f"💰 Ending Price: ${data['close'].iloc[-1]:.2f}")
        print(f"💰 Highest Price: ${data['high'].max():.2f}")
        print(f"💰 Lowest Price: ${data['low'].min():.2f}")
        print(f"💰 Average Price: ${data['close'].mean():.2f}")
        
        print("\n" + "="*80)
        print("MOVING AVERAGES ANALYSIS")
        print("="*80)
        
        current_price = data['close'].iloc[-1]
        ma50 = data['MA_50'].iloc[-1]
        ma200 = data['MA_200'].iloc[-1]
        
        print(f"📊 Current Price: ${current_price:.2f}")
        print(f"📊 50-day MA: ${ma50:.2f}")
        print(f"📊 200-day MA: ${ma200:.2f}")
        print(f"📊 Price vs MA50: {((current_price - ma50) / ma50 * 100):.2f}%")
        print(f"📊 Price vs MA200: {((current_price - ma200) / ma200 * 100):.2f}%")
        
        # Determine trend
        if current_price > ma50 > ma200:
            trend = "Strong Uptrend"
        elif current_price > ma50 and ma50 < ma200:
            trend = "Weak Uptrend"
        elif current_price < ma50 < ma200:
            trend = "Strong Downtrend"
        elif current_price < ma50 and ma50 > ma200:
            trend = "Weak Downtrend"
        else:
            trend = "Sideways"
        
        print(f"📊 Market Trend: {trend}")
        
        print("\n" + "="*80)
        print("VOLATILITY & RISK ANALYSIS")
        print("="*80)
        
        print(f"📈 Average Daily Return: {data['daily_return'].mean():.4f}")
        print(f"📈 Daily Return Volatility: {data['daily_return'].std():.4f}")
        print(f"📈 20-day Rolling Volatility: {data['volatility_20d'].mean():.4f}")
        print(f"📈 Average Daily Price Range: {data['price_range_pct'].mean():.2f}%")
        
        print("\n" + "="*80)
        print("VOLUME ANALYSIS")
        print("="*80)
        
        print(f"📊 Average Daily Volume: {data['volume'].mean():,.0f}")
        print(f"📊 Highest Daily Volume: {data['volume'].max():,.0f}")
        print(f"📊 Lowest Daily Volume: {data['volume'].min():,.0f}")
        print(f"📊 Total Volume Traded: {data['volume'].sum():,.0f}")
        
        print("\n" + "="*80)
        print("TECHNICAL INDICATORS")
        print("="*80)
        
        current_rsi = data['RSI'].iloc[-1]
        print(f"📊 Current RSI: {current_rsi:.2f}")
        
        if current_rsi > 70:
            rsi_signal = "Overbought"
        elif current_rsi < 30:
            rsi_signal = "Oversold"
        else:
            rsi_signal = "Neutral"
        
        print(f"📊 RSI Signal: {rsi_signal}")
        
        print("\n" + "="*80)
        print("CORRELATION INSIGHTS")
        print("="*80)
        
        # Calculate correlations
        price_volume_corr = data['close'].corr(data['volume'])
        returns_volume_corr = data['daily_return'].corr(data['volume'])
        
        print(f"📊 Price-Volume Correlation: {price_volume_corr:.4f}")
        print(f"📊 Returns-Volume Correlation: {returns_volume_corr:.4f}")
        
        if price_volume_corr < -0.3:
            print("📊 Volume tends to increase when prices fall (typical for stocks)")
        else:
            print("📊 Volume-price relationship is not strongly negative")
        
        print("\n" + "="*80)
        print("KEY INSIGHTS")
        print("="*80)
        
        insights = []
        
        # Performance insights
        if total_return > 100:
            insights.append("✅ Exceptional performance with over 100% total return")
        elif total_return > 50:
            insights.append("✅ Strong performance with over 50% total return")
        
        if sharpe_ratio > 1:
            insights.append("✅ Excellent risk-adjusted returns (Sharpe > 1)")
        elif sharpe_ratio > 0.5:
            insights.append("✅ Good risk-adjusted returns (Sharpe > 0.5)")
        
        if max_drawdown < -30:
            insights.append("⚠️ Significant drawdown experienced (>30%)")
        elif max_drawdown < -20:
            insights.append("⚠️ Moderate drawdown experienced (>20%)")
        
        # Technical insights
        if current_price > ma50 and ma50 > ma200:
            insights.append("📈 Strong technical uptrend (Golden Cross)")
        elif current_price < ma50 and ma50 < ma200:
            insights.append("📉 Strong technical downtrend (Death Cross)")
        
        if current_rsi > 70:
            insights.append("⚠️ RSI indicates overbought conditions")
        elif current_rsi < 30:
            insights.append("📈 RSI indicates oversold conditions")
        
        # Volatility insights
        if data['volatility_20d'].iloc[-1] > data['volatility_20d'].mean():
            insights.append("📊 Current volatility is above average")
        else:
            insights.append("📊 Current volatility is below average")
        
        for insight in insights:
            print(insight)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"Error displaying analysis summary: {str(e)}")

if __name__ == "__main__":
    print("Step 4: Analysis Summary")
    print("="*80)
    
    # Display the analysis summary
    display_analysis_summary() 