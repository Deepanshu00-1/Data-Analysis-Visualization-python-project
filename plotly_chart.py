import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

def create_interactive_price_chart():
    """
    Create an interactive line chart using Plotly that plots the 'Close' price, 
    50-day moving average, and 200-day moving average over time.
    """
    try:
        # Load the analysis data
        print("Loading analysis data...")
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        
        print(f"Data loaded successfully! Shape: {data.shape}")
        print(f"Date range: {data.index.min()} to {data.index.max()}")
        
        # Create the interactive line chart
        fig = go.Figure()
        
        # Add Close Price line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>Close Price:</b> $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add 50-day Moving Average
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA_50'],
            mode='lines',
            name='50-day Moving Average',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>50-day MA:</b> $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Add 200-day Moving Average
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA_200'],
            mode='lines',
            name='200-day Moving Average',
            line=dict(color='#2ca02c', width=2, dash='dot'),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>200-day MA:</b> $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
        
        # Update layout with proper labels and title
        fig.update_layout(
            title={
                'text': 'AAPL Stock Price with Moving Averages',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#2c3e50'}
            },
            xaxis_title='Date',
            yaxis_title='Price ($)',
            hovermode='x unified',
            template='plotly_white',
            height=600,
            width=1000,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.1)',
                borderwidth=1
            ),
            margin=dict(l=60, r=60, t=80, b=60),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(
            title_font=dict(size=14, color='#2c3e50'),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        )
        
        fig.update_yaxes(
            title_font=dict(size=14, color='#2c3e50'),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True,
            tickformat='$.2f'
        )
        
        # Add some annotations for key statistics
        current_price = data['close'].iloc[-1]
        ma50_current = data['MA_50'].iloc[-1]
        ma200_current = data['MA_200'].iloc[-1]
        
        # Add annotation for current price
        fig.add_annotation(
            x=data.index[-1],
            y=current_price,
            text=f"Current: ${current_price:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='#1f77b4',
            ax=40,
            ay=-40,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#1f77b4',
            borderwidth=1
        )
        
        # Add annotation for 50-day MA
        fig.add_annotation(
            x=data.index[-1],
            y=ma50_current,
            text=f"50-day MA: ${ma50_current:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='#ff7f0e',
            ax=40,
            ay=40,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#ff7f0e',
            borderwidth=1
        )
        
        # Add annotation for 200-day MA
        fig.add_annotation(
            x=data.index[-1],
            y=ma200_current,
            text=f"200-day MA: ${ma200_current:.2f}",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='#2ca02c',
            ax=40,
            ay=80,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#2ca02c',
            borderwidth=1
        )
        
        # Save the chart as HTML file
        output_file = 'interactive_price_chart.html'
        fig.write_html(output_file, include_plotlyjs=True)
        print(f"Interactive chart saved to: {output_file}")
        
        # Display some statistics
        print("\n" + "="*60)
        print("CHART STATISTICS")
        print("="*60)
        print(f"Current Price: ${current_price:.2f}")
        print(f"50-day MA: ${ma50_current:.2f}")
        print(f"200-day MA: ${ma200_current:.2f}")
        print(f"Price vs 50-day MA: {((current_price - ma50_current) / ma50_current * 100):.2f}%")
        print(f"Price vs 200-day MA: {((current_price - ma200_current) / ma200_current * 100):.2f}%")
        
        # Determine trend
        if current_price > ma50_current > ma200_current:
            trend = "Strong Uptrend"
        elif current_price > ma50_current and ma50_current < ma200_current:
            trend = "Weak Uptrend"
        elif current_price < ma50_current < ma200_current:
            trend = "Strong Downtrend"
        elif current_price < ma50_current and ma50_current > ma200_current:
            trend = "Weak Downtrend"
        else:
            trend = "Sideways"
        
        print(f"Market Trend: {trend}")
        
        print("\n" + "="*60)
        print("✅ Interactive chart created successfully!")
        print("="*60)
        
        return fig
        
    except Exception as e:
        print(f"Error creating interactive chart: {str(e)}")
        return None

def create_additional_charts():
    """
    Create additional interactive charts for comprehensive analysis.
    """
    try:
        # Load data
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        
        # 1. Volume Chart
        fig_volume = go.Figure()
        
        fig_volume.add_trace(go.Bar(
            x=data.index,
            y=data['volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        fig_volume.add_trace(go.Scatter(
            x=data.index,
            y=data['volume_ma_20'],
            name='20-day Volume MA',
            line=dict(color='red', width=2)
        ))
        
        fig_volume.update_layout(
            title='AAPL Trading Volume with Moving Average',
            xaxis_title='Date',
            yaxis_title='Volume',
            height=400,
            template='plotly_white'
        )
        
        fig_volume.write_html('volume_chart.html')
        print("Volume chart saved to: volume_chart.html")
        
        # 2. Returns Distribution
        fig_returns = go.Figure()
        
        fig_returns.add_trace(go.Histogram(
            x=data['daily_return'].dropna(),
            nbinsx=50,
            name='Daily Returns',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        fig_returns.update_layout(
            title='Distribution of Daily Returns',
            xaxis_title='Daily Return',
            yaxis_title='Frequency',
            height=400,
            template='plotly_white'
        )
        
        fig_returns.write_html('returns_distribution.html')
        print("Returns distribution chart saved to: returns_distribution.html")
        
        # 3. RSI Chart
        fig_rsi = go.Figure()
        
        fig_rsi.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            name='RSI',
            line=dict(color='purple', width=2)
        ))
        
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", 
                         annotation_text="Overbought (70)")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", 
                         annotation_text="Oversold (30)")
        
        fig_rsi.update_layout(
            title='Relative Strength Index (RSI)',
            xaxis_title='Date',
            yaxis_title='RSI',
            height=400,
            template='plotly_white'
        )
        
        fig_rsi.write_html('rsi_chart.html')
        print("RSI chart saved to: rsi_chart.html")
        
        print("\n" + "="*60)
        print("✅ All additional charts created successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"Error creating additional charts: {str(e)}")

if __name__ == "__main__":
    print("Step 5: Creating Interactive Visualizations")
    print("="*60)
    
    # Create the main interactive price chart
    main_chart = create_interactive_price_chart()
    
    # Create additional charts
    create_additional_charts()
    
    print("\nFiles created:")
    print("  - interactive_price_chart.html (Main price chart with moving averages)")
    print("  - volume_chart.html (Volume analysis)")
    print("  - returns_distribution.html (Returns distribution)")
    print("  - rsi_chart.html (RSI technical indicator)")
    
    print("\nTo view the charts:")
    print("  1. Open the HTML files in your web browser")
    print("  2. Or run the dashboard: python interactive_dashboard.py") 