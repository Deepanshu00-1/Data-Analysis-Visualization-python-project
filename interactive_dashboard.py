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

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load data
data = load_data()

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("📈 AAPL Stock Analysis Dashboard", 
                   className="text-center text-primary mb-4"),
            html.Hr()
        ])
    ]),
    
    # Key Metrics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💰 Current Price", className="card-title"),
                    html.H2(f"${data['close'].iloc[-1]:.2f}", className="text-success")
                ])
            ], className="mb-3")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Total Return", className="card-title"),
                    total_return = (data['close'].iloc[-1] / data['close'].iloc[0] - 1) * 100,
                    html.H2(f"{total_return:.1f}%", className="text-success")
                ])
            ], className="mb-3")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("⚡ Sharpe Ratio", className="card-title"),
                    sharpe_ratio = data['daily_return'].mean() / data['daily_return'].std() * np.sqrt(252),
                    html.H2(f"{sharpe_ratio:.3f}", className="text-info")
                ])
            ], className="mb-3")
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📉 Max Drawdown", className="card-title"),
                    cumulative_returns = data['cumulative_return'],
                    running_max = cumulative_returns.expanding().max(),
                    drawdown = (cumulative_returns - running_max) / running_max * 100,
                    max_drawdown = drawdown.min(),
                    html.H2(f"{max_drawdown:.1f}%", className="text-danger")
                ])
            ], className="mb-3")
        ], width=3)
    ]),
    
    # Main Charts
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📈 Price Chart with Moving Averages", className="card-title")
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='price-chart',
                        style={'height': '500px'}
                    )
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    # Secondary Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📊 Volume Analysis", className="card-title")
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='volume-chart',
                        style={'height': '400px'}
                    )
                ])
            ], className="mb-4")
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📈 Returns Distribution", className="card-title")
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='returns-chart',
                        style={'height': '400px'}
                    )
                ])
            ], className="mb-4")
        ], width=6)
    ]),
    
    # Technical Indicators Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("🔧 Technical Indicators", className="card-title")
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='technical-chart',
                        style={'height': '500px'}
                    )
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    # Controls Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("⚙️ Chart Controls", className="card-title")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Date Range:"),
                            dcc.DatePickerRange(
                                id='date-picker',
                                start_date=data.index.min().date(),
                                end_date=data.index.max().date(),
                                display_format='YYYY-MM-DD'
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Show Moving Averages:"),
                            dcc.Checklist(
                                id='ma-checklist',
                                options=[
                                    {'label': '50-day MA', 'value': 'MA_50'},
                                    {'label': '200-day MA', 'value': 'MA_200'}
                                ],
                                value=['MA_50', 'MA_200'],
                                inline=True
                            )
                        ], width=6)
                    ])
                ])
            ], className="mb-4")
        ], width=12)
    ])
], fluid=True)

# Callback for the main price chart
@app.callback(
    Output('price-chart', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date'),
     Input('ma-checklist', 'value')]
)
def update_price_chart(start_date, end_date, ma_values):
    """Update the price chart with moving averages."""
    
    # Filter data based on date range
    if start_date and end_date:
        mask = (data.index >= start_date) & (data.index <= end_date)
        filtered_data = data.loc[mask]
    else:
        filtered_data = data
    
    # Create the figure
    fig = go.Figure()
    
    # Add close price line
    fig.add_trace(go.Scatter(
        x=filtered_data.index,
        y=filtered_data['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#1f77b4', width=2),
        hovertemplate='<b>Date:</b> %{x}<br>' +
                     '<b>Close:</b> $%{y:.2f}<br>' +
                     '<extra></extra>'
    ))
    
    # Add moving averages if selected
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
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'AAPL Stock Price with Moving Averages',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Date',
        yaxis_title='Price ($)',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
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
    print("Starting Interactive Dashboard...")
    print("Dashboard will be available at: http://localhost:8050")
    print("Press Ctrl+C to stop the server")
    
    app.run_server(debug=True, host='0.0.0.0', port=8050) 