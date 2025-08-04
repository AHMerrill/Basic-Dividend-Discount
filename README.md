# 📈 Dividend Discount Model Calculator

A modern, interactive web application for calculating stock valuations using the Dividend Discount Model (DDM). This tool provides a comprehensive 5-year dividend discount model analysis with real-time market data and customizable parameters.

## 🚀 Features

- **Real-time Market Data**: Fetches live stock data using Yahoo Finance API
- **Interactive Interface**: Modern Streamlit web interface with intuitive controls
- **Customizable Parameters**: Adjust growth rates, cost of equity, and cash flows
- **Visual Analytics**: Interactive charts and detailed cash flow breakdowns
- **Comprehensive Analysis**: Includes ROE, beta, payout ratios, and market risk premiums
- **Professional Recommendations**: Buy/Sell/Hold recommendations based on intrinsic value

## 📊 What is the Dividend Discount Model?

The Dividend Discount Model is a method of valuing a company's stock price based on the theory that its stock is worth the sum of all of its future dividend payments, discounted back to their present value. This tool implements a 5-year DDM with:

- **Short-term Growth**: Based on ROE × (1 - Payout Ratio)
- **Long-term Growth**: Default 3.5% (adjustable)
- **Cost of Equity**: Calculated using CAPM (Capital Asset Pricing Model)
- **Terminal Value**: Perpetuity calculation for post-5-year cash flows

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd dividend-discount-model-calculator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

### Deployment Options

#### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

#### Heroku
1. Create a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
2. Deploy using Heroku CLI or GitHub integration

#### Docker
```bash
docker build -t ddm-calculator .
docker run -p 8501:8501 ddm-calculator
```

## 📖 How to Use

1. **Enter Stock Ticker**: Input any valid stock symbol (e.g., AAPL, MSFT, WMT)
2. **Review Default Parameters**: The app automatically calculates:
   - Risk-free rate from 10-year Treasury yields
   - Market risk premium from S&P 500 historical returns
   - Company-specific metrics (ROE, beta, payout ratio)
3. **Customize Parameters** (Optional):
   - Adjust short-term growth rates
   - Modify long-term growth assumptions
   - Change cost of equity
   - Enter custom dividend cash flows
4. **Analyze Results**: View intrinsic value, recommendations, and detailed breakdowns

## 📊 Key Metrics Explained

- **Intrinsic Value**: Calculated fair value of the stock
- **Current Price**: Latest market price from Yahoo Finance
- **Valuation Ratio**: Intrinsic value / Current price
- **Implied Return**: Expected annual return if stock reaches intrinsic value
- **ROE**: Return on Equity - measures profitability
- **Beta**: Stock volatility relative to market
- **Payout Ratio**: Percentage of earnings paid as dividends

## 🔧 Technical Details

### Data Sources
- **Stock Data**: Yahoo Finance API via `yfinance`
- **Risk-free Rate**: 10-year Treasury yield (^TNX)
- **Market Returns**: S&P 500 Total Return (^SP500TR)

### Key Functions
- `get_stock_data()`: Fetches comprehensive stock information
- `get_risk_free_rate()`: Retrieves current Treasury yields
- `get_equity_returns()`: Calculates historical market returns
- `perpetuity_pv()`: Computes terminal value using perpetuity formula

### Error Handling
- Graceful fallbacks for API failures
- Input validation for all user parameters
- Warning messages for non-dividend stocks

## 📈 Example Output

The application provides:
- **Company Overview**: Key metrics and financial ratios
- **Valuation Results**: Intrinsic value vs. market price
- **Cash Flow Analysis**: Detailed 5-year projection table
- **Visual Charts**: Interactive breakdown of cash flows
- **Summary Statistics**: Key performance indicators

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Original Analysis**: Based on financial analytics coursework by Zan Merrill
- **Data Provider**: Yahoo Finance for real-time market data
- **Web Framework**: Streamlit for the interactive interface
- **Visualization**: Plotly for interactive charts

## 🔄 Conversion Credit

**Streamlit App Conversion**: This web application was converted from a Jupyter notebook by an AI assistant. The original notebook contained a comprehensive dividend discount model analysis, and this conversion maintains all the original functionality while adding:

- Modern web interface with Streamlit
- Interactive parameter controls
- Real-time data visualization
- Professional styling and layout
- Enhanced error handling and user experience

The conversion preserves the mathematical rigor and analytical depth of the original work while making it accessible as a deployable web application.

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the maintainers.

---

**Disclaimer**: This tool is for educational and analytical purposes only. It should not be considered as financial advice. Always conduct thorough research and consult with financial professionals before making investment decisions. 