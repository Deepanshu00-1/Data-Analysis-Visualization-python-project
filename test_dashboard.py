import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def test_dashboard_data():
    """
    Test the dashboard data loading and basic functionality.
    """
    try:
        print("Testing Dashboard Data Loading...")
        print("="*50)
        
        # Test loading the analysis data
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        
        print(f"✅ Data loaded successfully!")
        print(f"   Shape: {data.shape}")
        print(f"   Date range: {data.index.min()} to {data.index.max()}")
        print(f"   Columns: {list(data.columns)}")
        
        # Test moving averages
        print(f"\n✅ Moving Averages:")
        print(f"   MA_50 available: {'MA_50' in data.columns}")
        print(f"   MA_200 available: {'MA_200' in data.columns}")
        print(f"   Current MA_50: ${data['MA_50'].iloc[-1]:.2f}")
        print(f"   Current MA_200: ${data['MA_200'].iloc[-1]:.2f}")
        
        # Test technical indicators
        print(f"\n✅ Technical Indicators:")
        print(f"   RSI available: {'RSI' in data.columns}")
        print(f"   Volatility available: {'volatility_20d' in data.columns}")
        print(f"   Current RSI: {data['RSI'].iloc[-1]:.2f}")
        print(f"   Current Volatility: {data['volatility_20d'].iloc[-1]:.4f}")
        
        # Test price data
        print(f"\n✅ Price Data:")
        print(f"   Current Price: ${data['close'].iloc[-1]:.2f}")
        print(f"   Highest Price: ${data['high'].max():.2f}")
        print(f"   Lowest Price: ${data['low'].min():.2f}")
        
        # Test volume data
        print(f"\n✅ Volume Data:")
        print(f"   Average Volume: {data['volume'].mean():,.0f}")
        print(f"   Current Volume: {data['volume'].iloc[-1]:,.0f}")
        
        print("\n" + "="*50)
        print("✅ All data tests passed!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard data: {str(e)}")
        return False

def test_plotly_charts():
    """
    Test creating a simple Plotly chart.
    """
    try:
        print("\nTesting Plotly Chart Creation...")
        print("="*50)
        
        # Load data
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        
        # Create a simple test chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data.index[-50:],  # Last 50 days
            y=data['close'].iloc[-50:],
            mode='lines',
            name='Close Price (Last 50 days)',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title='Test Chart - AAPL Last 50 Days',
            xaxis_title='Date',
            yaxis_title='Price ($)',
            height=400
        )
        
        # Save test chart
        fig.write_html('test_chart.html')
        print("✅ Test chart created and saved to: test_chart.html")
        
        print("\n" + "="*50)
        print("✅ Plotly chart test passed!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Plotly charts: {str(e)}")
        return False

def display_dashboard_instructions():
    """
    Display instructions for running the dashboard.
    """
    print("\n" + "="*60)
    print("📊 INTERACTIVE DASHBOARD INSTRUCTIONS")
    print("="*60)
    
    print("\n🎯 To run the interactive dashboard:")
    print("   1. Open a terminal/command prompt")
    print("   2. Navigate to this directory")
    print("   3. Run: python interactive_dashboard.py")
    print("   4. Open your web browser")
    print("   5. Go to: http://localhost:8050")
    print("   6. Press Ctrl+C to stop the server")
    
    print("\n📈 To view individual charts:")
    print("   1. Open any of these HTML files in your browser:")
    print("      - interactive_price_chart.html")
    print("      - volume_chart.html")
    print("      - returns_distribution.html")
    print("      - rsi_chart.html")
    
    print("\n🔧 Dashboard Features:")
    print("   ✅ Interactive price chart with moving averages")
    print("   ✅ Volume analysis with moving average")
    print("   ✅ Returns distribution and cumulative returns")
    print("   ✅ Technical indicators (RSI, Volatility)")
    print("   ✅ Date range selector")
    print("   ✅ Moving average toggles")
    print("   ✅ Key metrics cards")
    print("   ✅ Responsive design")
    
    print("\n📊 Chart Features:")
    print("   ✅ Hover tooltips with detailed information")
    print("   ✅ Zoom and pan capabilities")
    print("   ✅ Download as PNG functionality")
    print("   ✅ Legend toggles")
    print("   ✅ Unified hover mode")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("Step 5: Testing Interactive Dashboard")
    print("="*60)
    
    # Test data loading
    data_test = test_dashboard_data()
    
    # Test chart creation
    chart_test = test_plotly_charts()
    
    # Display instructions
    display_dashboard_instructions()
    
    if data_test and chart_test:
        print("\n✅ All tests passed! Dashboard is ready to run.")
    else:
        print("\n❌ Some tests failed. Please check the data files.") 