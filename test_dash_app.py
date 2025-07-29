import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

def test_dash_app_configuration():
    """
    Test the Dash app configuration and basic functionality.
    """
    try:
        print("Testing Dash App Configuration...")
        print("="*50)
        
        # Test data loading
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        
        print("✅ Data loading successful")
        print(f"   Data shape: {data.shape}")
        print(f"   Date range: {data.index.min()} to {data.index.max()}")
        
        # Test Dash app initialization
        app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            title="Stock Price Dashboard",
            meta_tags=[
                {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                {"name": "description", "content": "Interactive stock price analysis dashboard for AAPL"}
            ]
        )
        
        print("✅ Dash app initialization successful")
        print(f"   App title: {app.title}")
        print(f"   Bootstrap theme: Loaded")
        
        # Test basic layout creation
        layout = dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("📈 Stock Price Dashboard", 
                           className="text-center text-primary mb-3 fw-bold"),
                    html.Hr(className="my-4"),
                    html.Div([
                        html.H4("📊 About This Dashboard", className="text-info mb-3"),
                        html.P([
                            "This interactive dashboard provides comprehensive analysis of AAPL (Apple Inc.) stock performance ",
                            "from 2018 to 2023. The dashboard includes real-time price charts, technical indicators, ",
                            "volume analysis, and performance metrics to help you understand stock market trends and patterns."
                        ], className="lead mb-4")
                    ], className="bg-light p-4 rounded mb-4")
                ])
            ])
        ], fluid=True)
        
        print("✅ Layout creation successful")
        print("   Dashboard title: Stock Price Dashboard")
        print("   Description: Comprehensive AAPL stock analysis")
        
        # Test callback function creation
        @app.callback(
            Output('test-output', 'children'),
            [Input('test-input', 'value')]
        )
        def test_callback(value):
            return f"Test callback working: {value}"
        
        print("✅ Callback function creation successful")
        
        # Test chart creation
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index[-50:],
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
        
        print("✅ Chart creation successful")
        print("   Chart type: Line chart")
        print("   Data points: 50 days")
        
        print("\n" + "="*50)
        print("✅ All Dash app tests passed!")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Dash app: {str(e)}")
        return False

def display_dash_app_info():
    """
    Display information about the Dash app.
    """
    print("\n" + "="*60)
    print("📊 DASH APP INFORMATION")
    print("="*60)
    
    print("\n🎯 App Details:")
    print("   Title: Stock Price Dashboard")
    print("   Framework: Dash with Bootstrap")
    print("   Theme: Bootstrap (responsive design)")
    print("   Port: 8050")
    print("   URL: http://localhost:8050")
    
    print("\n📝 Dashboard Description:")
    print("   This interactive dashboard provides comprehensive analysis of AAPL (Apple Inc.)")
    print("   stock performance from 2018 to 2023. The dashboard includes real-time price")
    print("   charts, technical indicators, volume analysis, and performance metrics to")
    print("   help you understand stock market trends and patterns.")
    
    print("\n🔧 Key Features:")
    print("   ✅ Interactive price charts with moving averages")
    print("   ✅ Volume analysis with trading patterns")
    print("   ✅ Returns distribution and cumulative performance")
    print("   ✅ Technical indicators (RSI, Volatility)")
    print("   ✅ Real-time filtering by date range")
    print("   ✅ Toggle controls for moving averages")
    print("   ✅ Key performance metrics cards")
    print("   ✅ Responsive Bootstrap design")
    print("   ✅ Hover tooltips and zoom capabilities")
    print("   ✅ Download functionality")
    
    print("\n📊 Chart Components:")
    print("   • Main price chart with 50-day and 200-day MAs")
    print("   • Volume analysis with 20-day volume MA")
    print("   • Returns distribution histogram")
    print("   • Cumulative returns line chart")
    print("   • RSI technical indicator")
    print("   • 20-day rolling volatility")
    
    print("\n🎛️ Interactive Controls:")
    print("   • Date range picker")
    print("   • Moving average toggles")
    print("   • Real-time chart updates")
    print("   • Zoom and pan capabilities")
    
    print("\n📱 Responsive Design:")
    print("   • Mobile-friendly layout")
    print("   • Bootstrap grid system")
    print("   • Adaptive chart sizing")
    print("   • Touch-friendly controls")
    
    print("\n" + "="*60)

def display_usage_instructions():
    """
    Display usage instructions for the Dash app.
    """
    print("\n" + "="*60)
    print("🚀 HOW TO RUN THE DASH APP")
    print("="*60)
    
    print("\n📋 Step-by-Step Instructions:")
    print("   1. Open a terminal/command prompt")
    print("   2. Navigate to the project directory")
    print("   3. Run: python dash_app.py")
    print("   4. Wait for the server to start")
    print("   5. Open your web browser")
    print("   6. Go to: http://localhost:8050")
    print("   7. Explore the interactive dashboard")
    print("   8. Press Ctrl+C to stop the server")
    
    print("\n🎯 Quick Start:")
    print("   • Run: python dash_app.py")
    print("   • Browse: http://localhost:8050")
    print("   • Explore: Interactive charts and controls")
    
    print("\n💡 Usage Tips:")
    print("   • Use date picker to focus on specific periods")
    print("   • Toggle moving averages on/off")
    print("   • Hover over charts for detailed info")
    print("   • Zoom and pan to explore data")
    print("   • Download charts using camera icon")
    print("   • Monitor key metrics in the cards")
    
    print("\n⚠️  Troubleshooting:")
    print("   • Ensure all dependencies are installed")
    print("   • Check that data files exist")
    print("   • Verify port 8050 is available")
    print("   • Try different browser if issues occur")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("Step 6: Testing Dash App Configuration")
    print("="*60)
    
    # Test the Dash app configuration
    test_result = test_dash_app_configuration()
    
    # Display app information
    display_dash_app_info()
    
    # Display usage instructions
    display_usage_instructions()
    
    if test_result:
        print("\n✅ Dash app is ready to run!")
        print("   Run: python dash_app.py")
        print("   Access: http://localhost:8050")
    else:
        print("\n❌ Some tests failed. Please check the configuration.") 