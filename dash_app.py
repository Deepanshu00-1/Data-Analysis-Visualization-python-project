import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import dash_bootstrap_components as dbc

# Load the analysis data
def load_data():
    """Load the analysis data for the dashboard."""
    try:
        data = pd.read_csv('analysis/AAPL_analysis_results.csv')
        data['date'] = pd.to_datetime(data['date'], utc=True)
        data = data.set_index('date')
        return data
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Stock Price Dashboard",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": "Interactive stock price analysis dashboard for AAPL"}
    ]
)

# Load data
data = load_data()

# Define the layout with comprehensive description
app.layout = dbc.Container([
    # Header Section
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
                ], className="lead mb-4"),
                html.Div([
                    html.H5("🔧 Dashboard Features:", className="text-success mb-2"),
                    html.Ul([
                        html.Li("Interactive price charts with 50-day and 200-day moving averages"),
                        html.Li("Volume analysis with trading volume patterns"),
                        html.Li("Returns distribution and cumulative performance"),
                        html.Li("Technical indicators including RSI and volatility"),
                        html.Li("Real-time filtering by date range"),
                        html.Li("Toggle controls for moving averages"),
                        html.Li("Key performance metrics and statistics")
                    ], className="mb-4")
                ])
            ], className="bg-light p-4 rounded mb-4")
        ])
    ]),
    
    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💰 Current Price", className="card-title text-center"),
                    html.H2(f"${data['close'].iloc[-1]:.2f}", className="text-success text-center fw-bold")
                ])
            ], className="mb-3 shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Total Return", className="card-title text-center"),
                    html.H2(f"{(data['close'].iloc[-1] / data['close'].iloc[0] - 1) * 100:.1f}%", className="text-success text-center fw-bold")
                ])
            ], className="mb-3 shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("⚡ Sharpe Ratio", className="card-title text-center"),
                    html.H2(f"{data['daily_return'].mean() / data['daily_return'].std() * np.sqrt(252):.3f}", className="text-info text-center fw-bold")
                ])
            ], className="mb-3 shadow-sm")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📉 Max Drawdown", className="card-title text-center"),
                    html.H2(f"{((data['cumulative_return'] - data['cumulative_return'].expanding().max()) / data['cumulative_return'].expanding().max() * 100).min():.1f}%", className="text-danger text-center fw-bold")
                ])
            ], className="mb-3 shadow-sm")
        ], width=3)
    ]),
    
    # Data Period Info
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.H5("📅 Analysis Period", className="alert-heading"),
                html.P([
                    f"Data covers from {data.index.min().strftime('%B %d, %Y')} to {data.index.max().strftime('%B %d, %Y')} ",
                    f"({len(data):,} trading days). This represents a comprehensive view of AAPL's performance ",
                    "during a period of significant market growth and volatility."
                ])
            ], color="info", className="mb-4")
        ])
    ]),
    
    # Main Price Chart with Plotly Integration
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📈 Interactive Price Chart with Moving Averages", className="card-title mb-0")
                ], className="bg-primary text-white"),
                dbc.CardBody([
                    html.P([
                        "This interactive Plotly chart displays AAPL's closing price along with 50-day and 200-day moving averages. ",
                        "The chart is fully interactive with zoom, pan, hover tooltips, and download capabilities. ",
                        "Use the controls below to customize your view and explore different time periods."
                    ], className="text-muted mb-3"),
                    dcc.Graph(
                        id='price-chart',
                        style={'height': '500px'},
                        config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                            'toImageButtonOptions': {
                                'format': 'png',
                                'filename': 'aapl_price_chart',
                                'height': 600,
                                'width': 1000,
                                'scale': 2
                            }
                        }
                    )
                ])
            ], className="mb-4 shadow")
        ], width=12)
    ]),
    
    # Additional Plotly Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📊 Advanced Plotly Visualizations", className="card-title mb-0")
                ], className="bg-success text-white"),
                dbc.CardBody([
                    html.P([
                        "Enhanced Plotly charts with advanced features including subplots, annotations, ",
                        "and interactive elements. These charts provide deeper insights into stock performance."
                    ], className="text-muted mb-3"),
                    dcc.Graph(
                        id='advanced-chart',
                        style={'height': '600px'},
                        config={
                            'displayModeBar': True,
                            'displaylogo': False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                            'toImageButtonOptions': {
                                'format': 'png',
                                'filename': 'aapl_advanced_analysis',
                                'height': 800,
                                'width': 1200,
                                'scale': 2
                            }
                        }
                    )
                ])
            ], className="mb-4 shadow")
        ], width=12)
    ]),
    
    # Secondary Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📊 Volume Analysis", className="card-title mb-0")
                ], className="bg-success text-white"),
                dbc.CardBody([
                    html.P([
                        "Trading volume analysis shows market activity and liquidity. ",
                        "High volume often accompanies significant price movements."
                    ], className="text-muted mb-3"),
                    dcc.Graph(
                        id='volume-chart',
                        style={'height': '400px'}
                    )
                ])
            ], className="mb-4 shadow")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📈 Returns Distribution", className="card-title mb-0")
                ], className="bg-warning text-dark"),
                dbc.CardBody([
                    html.P([
                        "Returns distribution shows the frequency of daily price changes. ",
                        "Cumulative returns track overall performance over time."
                    ], className="text-muted mb-3"),
                    dcc.Graph(
                        id='returns-chart',
                        style={'height': '400px'}
                    )
                ])
            ], className="mb-4 shadow")
        ], width=6)
    ]),
    
    # Technical Indicators Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("🔧 Technical Indicators", className="card-title mb-0")
                ], className="bg-info text-white"),
                dbc.CardBody([
                    html.P([
                        "RSI (Relative Strength Index) measures momentum and identifies overbought/oversold conditions. ",
                        "Volatility shows the degree of price variation over time."
                    ], className="text-muted mb-3"),
                    dcc.Graph(
                        id='technical-chart',
                        style={'height': '500px'}
                    )
                ])
            ], className="mb-4 shadow")
        ], width=12)
    ]),
    
    # Controls Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("⚙️ Chart Controls", className="card-title mb-0")
                ], className="bg-secondary text-white"),
                dbc.CardBody([
                    html.P([
                        "Customize your analysis by selecting date ranges and toggling moving averages. ",
                        "All charts will update automatically based on your selections."
                    ], className="text-muted mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("📅 Date Range:", className="fw-bold"),
                            dcc.DatePickerRange(
                                id='date-picker',
                                start_date=data.index.min().date(),
                                end_date=data.index.max().date(),
                                display_format='YYYY-MM-DD',
                                className="mb-3"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("📊 Show Moving Averages:", className="fw-bold"),
                            dcc.Checklist(
                                id='ma-checklist',
                                options=[
                                    {'label': '50-day MA', 'value': 'MA_50'},
                                    {'label': '200-day MA', 'value': 'MA_200'}
                                ],
                                value=['MA_50', 'MA_200'],
                                inline=True,
                                className="mb-3"
                            )
                        ], width=6)
                    ])
                ])
            ], className="mb-4 shadow")
        ], width=12)
    ]),
    
    # Footer Section
    dbc.Row([
        dbc.Col([
            html.Hr(className="my-4"),
            html.Div([
                html.H5("📚 How to Use This Dashboard", className="text-primary mb-3"),
                html.Ol([
                    html.Li("Use the date picker to focus on specific time periods"),
                    html.Li("Toggle moving averages on/off to simplify the view"),
                    html.Li("Hover over charts for detailed information"),
                    html.Li("Zoom and pan to explore specific data points"),
                    html.Li("Download charts as images using the camera icon"),
                    html.Li("Monitor key metrics in the cards at the top")
                ], className="mb-4"),
                html.Div([
                    html.H6("💡 Key Insights:", className="text-success mb-2"),
                    html.P([
                        "• Strong uptrends typically show price above both moving averages",
                        html.Br(),
                        "• High volume often confirms significant price movements",
                        html.Br(),
                        "• RSI above 70 indicates overbought conditions",
                        html.Br(),
                        "• RSI below 30 indicates oversold conditions"
                    ], className="text-muted")
                ])
            ], className="bg-light p-4 rounded")
        ])
    ])
    
], fluid=True, className="py-4")

# Callback for the main price chart with enhanced Plotly features
@app.callback(
    Output('price-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('ma-checklist', 'value')]
)
def update_price_chart(start_date, end_date, ma_values):
    """Update the price chart with moving averages and enhanced Plotly features."""
    
    # Filter data based on date range
    if start_date and end_date:
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask]
    else:
        filtered_data = data
    
    # Create the figure with enhanced styling
    fig = go.Figure()
    
    # Add Close Price line with enhanced styling
    fig.add_trace(go.Scatter(
        x=filtered_data.index,
        y=filtered_data['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1f77b4', width=3),
        hovertemplate='<b>Date:</b> %{x}<br>' +
                     '<b>Close Price:</b> $%{y:.2f}<br>' +
                     '<b>Volume:</b> %{customdata:,.0f}<br>' +
                     '<extra></extra>',
        customdata=filtered_data['volume']
    ))
    
    # Add moving averages if selected with enhanced styling
    if 'MA_50' in ma_values:
        fig.add_trace(go.Scatter(
            x=filtered_data.index,
            y=filtered_data['MA_50'],
            mode='lines',
            name='50-day MA',
            line=dict(color='#ff7f0e', width=2, dash='dash'),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>50-day MA:</b> $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
    
    if 'MA_200' in ma_values:
        fig.add_trace(go.Scatter(
            x=filtered_data.index,
            y=filtered_data['MA_200'],
            mode='lines',
            name='200-day MA',
            line=dict(color='#2ca02c', width=2, dash='dot'),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>200-day MA:</b> $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
    
    # Add volume as bars in secondary y-axis
    fig.add_trace(go.Bar(
        x=filtered_data.index,
        y=filtered_data['volume'],
        name='Volume',
        yaxis='y2',
        marker_color='rgba(0,0,255,0.1)',
        opacity=0.3,
        hovertemplate='<b>Date:</b> %{x}<br>' +
                     '<b>Volume:</b> %{y:,.0f}<br>' +
                     '<extra></extra>'
    ))
    
    # Enhanced layout with dual y-axes and annotations
    fig.update_layout(
        title={
            'text': 'AAPL Stock Price with Moving Averages and Volume',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 22, 'color': '#2c3e50'}
        },
        xaxis_title='Date',
        yaxis_title='Price ($)',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        hovermode='x unified',
        template='plotly_white',
        height=500,
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
    
    # Add annotations for key statistics
    current_price = filtered_data['close'].iloc[-1]
    ma50_current = filtered_data['MA_50'].iloc[-1] if 'MA_50' in ma_values else None
    ma200_current = filtered_data['MA_200'].iloc[-1] if 'MA_200' in ma_values else None
    
    # Add current price annotation
    fig.add_annotation(
        x=filtered_data.index[-1],
        y=current_price,
        text=f"Current: ${current_price:.2f}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor='#1f77b4',
        ax=40,
        ay=-40,
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#1f77b4',
        borderwidth=1
    )
    
    return fig

# Callback for advanced Plotly chart
@app.callback(
    Output('advanced-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_advanced_chart(start_date, end_date):
    """Create an advanced Plotly chart with multiple subplots and features."""
    
    # Filter data based on date range
    if start_date and end_date:
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask]
    else:
        filtered_data = data
    
    # Create subplots: price, volume, RSI, and volatility
    fig = make_subplots(
        rows=4, cols=1,
        subplot_titles=('Price & Moving Averages', 'Volume', 'RSI', 'Volatility'),
        vertical_spacing=0.08,
        row_heights=[0.4, 0.2, 0.2, 0.2]
    )
    
    # Price chart
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#1f77b4', width=2)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['MA_50'],
            mode='lines',
            name='50-day MA',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['MA_200'],
            mode='lines',
            name='200-day MA',
            line=dict(color='#2ca02c', width=2, dash='dot')
        ),
        row=1, col=1
    )
    
    # Volume chart
    fig.add_trace(
        go.Bar(
            x=filtered_data.index,
            y=filtered_data['volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.7
        ),
        row=2, col=1
    )
    
    # RSI chart
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['RSI'],
            name='RSI',
            line=dict(color='purple', width=2)
        ),
        row=3, col=1
    )
    
    # Add RSI overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Overbought (70)", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="Oversold (30)", row=3, col=1)
    
    # Volatility chart
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['volatility_20d'],
            name='20-day Volatility',
            line=dict(color='red', width=2),
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.1)'
        ),
        row=4, col=1
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Comprehensive AAPL Analysis Dashboard',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        height=600,
        showlegend=True,
        hovermode='x unified',
        template='plotly_white'
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Date", row=4, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    fig.update_yaxes(title_text="Volatility", row=4, col=1)
    
    return fig

# Callback for volume chart
@app.callback(
    Output('volume-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_volume_chart(start_date, end_date):
    """Update the volume chart."""
    
    # Filter data based on date range
    if start_date and end_date:
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask]
    else:
        filtered_data = data
    
    # Create subplot for volume and price range
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Trading Volume', 'Daily Price Range (%)'),
        vertical_spacing=0.1,
        row_heights=[0.6, 0.4]
    )
    
    # Volume chart
    fig.add_trace(
        go.Bar(
            x=filtered_data.index,
            y=filtered_data['volume'],
            name='Volume',
            marker_color='lightblue',
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # Volume moving average
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['volume_ma_20'],
            name='20-day Volume MA',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )
    
    # Price range chart
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['price_range_pct'],
            name='Price Range %',
            line=dict(color='green', width=2),
            fill='tonexty',
            fillcolor='rgba(0,255,0,0.1)'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Volume and Price Range Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        height=400,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Volume", row=1, col=1)
    fig.update_yaxes(title_text="Price Range (%)", row=2, col=1)
    
    return fig

# Callback for returns chart
@app.callback(
    Output('returns-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_returns_chart(start_date, end_date):
    """Update the returns distribution chart."""
    
    # Filter data based on date range
    if start_date and end_date:
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask]
    else:
        filtered_data = data
    
    # Create subplot for histogram and cumulative returns
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Daily Returns Distribution', 'Cumulative Returns'),
        specs=[[{"type": "histogram"}, {"type": "scatter"}]]
    )
    
    # Histogram of returns
    fig.add_trace(
        go.Histogram(
            x=filtered_data['daily_return'].dropna(),
            nbinsx=50,
            name='Daily Returns',
            marker_color='lightblue',
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # Cumulative returns
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['cumulative_return'],
            name='Cumulative Returns',
            line=dict(color='green', width=2)
        ),
        row=1, col=2
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Returns Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Daily Return", row=1, col=1)
    fig.update_yaxes(title_text="Frequency", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=2)
    fig.update_yaxes(title_text="Cumulative Return", row=1, col=2)
    
    return fig

# Callback for technical indicators chart
@app.callback(
    Output('technical-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_technical_chart(start_date, end_date):
    """Update the technical indicators chart."""
    
    # Filter data based on date range
    if start_date and end_date:
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask]
    else:
        filtered_data = data
    
    # Create subplot for RSI and volatility
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Relative Strength Index (RSI)', '20-day Rolling Volatility'),
        vertical_spacing=0.1
    )
    
    # RSI
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['RSI'],
            name='RSI',
            line=dict(color='purple', width=2)
        ),
        row=1, col=1
    )
    
    # Add RSI overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red", 
                  annotation_text="Overbought (70)", row=1, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", 
                  annotation_text="Oversold (30)", row=1, col=1)
    
    # Volatility
    fig.add_trace(
        go.Scatter(
            x=filtered_data.index,
            y=filtered_data['volatility_20d'],
            name='20-day Volatility',
            line=dict(color='red', width=2),
            fill='tonexty',
            fillcolor='rgba(255,0,0,0.1)'
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Technical Indicators',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        height=500,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=1, col=1)
    fig.update_yaxes(title_text="Volatility", row=2, col=1)
    
    return fig

# Run the app
if __name__ == '__main__':
    print("🚀 Starting Stock Price Dashboard...")
    print("="*60)
    print("📊 Dashboard Title: Stock Price Dashboard")
    print("📝 Description: Interactive stock analysis dashboard for AAPL")
    print("🌐 Access URL: http://localhost:8050")
    print("⏹️  Stop Server: Press Ctrl+C")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=8050) 