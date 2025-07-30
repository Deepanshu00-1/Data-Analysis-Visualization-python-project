# 📊 Stock Price Analysis Dashboard

A comprehensive Python-based dashboard for stock market analysis and visualization using Dash, Plotly, and yfinance. This project provides interactive stock analysis tools with real-time data visualization capabilities.

## 🚀 Features

- **Real-time Stock Data**: Live stock data visualization using yfinance API
- **Interactive Dashboards**: Dynamic charts and graphs with Plotly
- **Advanced Analytics**: Technical indicators, moving averages, and volatility analysis
- **Data Processing**: Advanced data manipulation with Pandas and NumPy
- **Web Interface**: Modern responsive web dashboard using Dash
- **Multiple Chart Types**: Price charts, volume analysis, RSI, returns distribution
- **Interactive Controls**: Date range picker, moving average toggles

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🛠️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd python-project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Dashboard
```bash
python dash_app.py
```

You should see output like:
```
🚀 Starting Stock Price Dashboard...
============================================================
📊 Dashboard Title: Stock Price Dashboard
📝 Description: Interactive stock analysis dashboard for AAPL
🌐 Access URL: http://localhost:8050
⏹️  Stop Server: Press Ctrl+C
============================================================
 * Serving Flask app 'dash_app'
 * Debug mode: on
 * Running on http://0.0.0.0:8050
```

### Step 4: Access the Dashboard
Open your web browser and navigate to:
```
http://localhost:8050
```
or
```
http://127.0.0.1:8050
```

## 📊 Dashboard Features

### 🎛️ Interactive Controls
- **Date Range Picker**: Select specific time periods to analyze
- **Moving Average Toggles**: Show/hide 50-day and 200-day moving averages
- **Real-time Updates**: All charts update automatically when you change settings

### 📈 Chart Types
1. **Main Price Chart**: AAPL stock price with moving averages and volume
2. **Advanced Analysis**: Multi-subplot chart with price, volume, RSI, and volatility
3. **Volume Analysis**: Trading volume patterns and price range analysis
4. **Returns Distribution**: Daily returns histogram and cumulative performance
5. **Technical Indicators**: RSI and volatility analysis

### 📊 Key Metrics Cards
- **Current Price**: Latest AAPL stock price
- **Total Return**: Overall performance percentage
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Worst historical decline

## 🔧 How to Use the Dashboard

### 1. Date Filtering
- Use the date picker in the "Chart Controls" section
- Select start and end dates to focus on specific periods
- All charts will update automatically

### 2. Moving Averages
- Check/uncheck the moving average options
- 50-day MA: Short-term trend indicator
- 200-day MA: Long-term trend indicator

### 3. Chart Interactions
- **Hover**: Get detailed information on data points
- **Zoom**: Click and drag to zoom into specific areas
- **Pan**: Click and drag to move around when zoomed
- **Download**: Use the camera icon to save charts as images

### 4. Key Insights
- **Strong Uptrends**: Price above both moving averages
- **High Volume**: Often confirms significant price movements
- **RSI > 70**: Overbought conditions
- **RSI < 30**: Oversold conditions

## 📁 Project Structure

```
python-project/
├── dash_app.py              # Main dashboard application
├── requirements.txt          # Python dependencies
├── README.md               # Project documentation
├── data/                   # Data files
│   ├── AAPL_historical_data.csv
│   ├── AAPL_cleaned_data.csv
│   └── sample_data.csv
├── analysis/               # Analysis results
│   ├── AAPL_analysis_results.csv
│   └── performance_summary.txt
├── plots/                  # Static visualizations
│   ├── correlation_heatmap.png
│   ├── price_with_moving_averages.png
│   ├── returns_analysis.png
│   ├── technical_indicators.png
│   ├── volatility_analysis.png
│   └── volume_analysis.png
├── data_loader.py          # Data loading utilities
├── data_cleaner.py         # Data cleaning functions
├── eda_analysis.py         # Exploratory data analysis
├── plotly_chart.py         # Plotly chart generation
├── interactive_dashboard.py # Interactive dashboard components
└── *.html                  # Generated HTML visualizations
```

## 📚 Libraries Used

- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Dash**: Web application framework
- **yfinance**: Yahoo Finance API wrapper
- **Matplotlib**: Static plotting
- **Seaborn**: Statistical data visualization
- **scikit-learn**: Machine learning tools

## 🛠️ Troubleshooting

### If the app doesn't start:

1. **Check Python installation**:
   ```bash
   python --version
   ```

2. **Verify dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Check if port 8050 is available**:
   - If you get a port error, the dashboard might already be running
   - Try accessing http://localhost:8050 in your browser

### If the dashboard loads but charts are empty:

1. **Check data files**:
   - Ensure `analysis/AAPL_analysis_results.csv` exists
   - Run the data processing scripts if needed

2. **Check browser console**:
   - Press F12 to open developer tools
   - Look for any JavaScript errors

## 📱 Access from Other Devices

If you want to access the dashboard from other devices on your network:

1. **Find your IP address**:
   ```bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   ```

2. **Access via IP**:
   ```
   http://YOUR_IP_ADDRESS:8050
   ```

## 🛑 Stopping the Dashboard

To stop the dashboard server:
- Press `Ctrl+C` in the terminal where the app is running
- Or close the terminal window

## 🎯 Success Indicators

You'll know everything is working when you see:

✅ **Server running**: Terminal shows "Running on http://0.0.0.0:8050"
✅ **Dashboard loads**: Browser shows the Stock Price Dashboard
✅ **Interactive charts**: You can hover, zoom, and interact with charts
✅ **Date picker works**: Selecting dates updates all charts
✅ **Moving averages toggle**: Checkboxes show/hide trend lines

## 💡 Tips for Best Experience

- **Use a modern browser** (Chrome, Firefox, Safari, Edge)
- **Allow pop-ups** if you want to download charts
- **Try different screen sizes** - the dashboard is responsive
- **Bookmark the URL** for quick access
- **Check the console** (F12) if you encounter issues

## 🚀 Next Steps

Once your dashboard is running successfully, you can:

1. **Explore different time periods** using the date picker
2. **Analyze specific market events** by zooming into relevant periods
3. **Compare technical indicators** across different timeframes
4. **Export charts** for presentations or reports
5. **Customize the analysis** by modifying the code

## 📄 License

MIT License

---

**🎯 Your dashboard is now ready for professional stock analysis!** 