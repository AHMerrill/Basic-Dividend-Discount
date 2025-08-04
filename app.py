import streamlit as st
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Dividend Discount Model Calculator",
    page_icon="📈",
    layout="wide"
)

# Initialize session state
if 'custom_cf' not in st.session_state:
    st.session_state.custom_cf = True
if 'custom_growth' not in st.session_state:
    st.session_state.custom_growth = True
if 'custom_lt_growth' not in st.session_state:
    st.session_state.custom_lt_growth = True
if 'custom_ke' not in st.session_state:
    st.session_state.custom_ke = True

# Title and description
st.title("📈 Dividend Discount Model Calculator")
st.markdown("**5-Year Dividend Discount Model for Equity Valuation**")
st.markdown("*This tool assumes annual fiscal year end and dividend payment date of 31 December*")

# Sidebar for inputs
st.sidebar.header("📊 Model Parameters")
st.sidebar.markdown("*Adjust the parameters below to customize the model*")

def perpetuity_pv(cash_flow, growth_rate, discount_rate):    
    perpetuity_pv = cash_flow*(1+growth_rate) / (discount_rate - growth_rate)
    return perpetuity_pv

def get_stock_data(ticker):
    try:
        ticker_find = yf.Ticker(ticker)
        info = ticker_find.info

        def safe_timestamp(ts):
            return datetime.fromtimestamp(ts) if ts else None

        book = info.get('bookValue')
        shares = info.get('sharesOutstanding')

        data = {
            "Company Name": info.get('longName'), 
            "Next Dividend Date (datetime)": safe_timestamp(info.get('dividendDate')),
            "Net Income (last FY)": info.get('netIncomeToCommon'),
            "Book Value per Share": book,
            "Shares Outstanding": shares,
            "Total Book Value (equity est.)": book * shares if book and shares else None,
            "Dividend Per Share (forward)": info.get('dividendRate'),
            "Dividend Per Share (trailing)": info.get('trailingAnnualDividendRate'),
            "Beta": info.get('beta'),
            "Return on Equity (ROE)": info.get('returnOnEquity'),
            "Dividend Payout Ratio": info.get('payoutRatio'),
            "Last Stock Price": info.get('currentPrice')
        }
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return None

def get_risk_free_rate():
    try:
        tnx = yf.Ticker("^TNX")
        hist = tnx.history(period="5d")
        latest_raw = hist['Close'].iloc[-1]
        latest_yield = latest_raw / 100
        return latest_yield
    except:
        return 0.0422  # Default fallback

def get_equity_returns():
    try:
        one_year = timedelta(days=365, hours=5, minutes=49, seconds=12)
        sp500 = yf.Ticker("^SP500TR")
        hist = sp500.history(period="max")
        
        end_close = hist['Close'].iloc[-1]
        start_close = hist['Close'].iloc[0]

        cagr = ((end_close / start_close) ** (1/((hist.index[-1] - hist.index[0])/one_year)))-1
        return cagr
    except:
        return 0.1119  # Default fallback

def adjustment_for_partial_year(ticker):
    today = datetime.today()
    year = today.year
    
    try:
        ticker_find = yf.Ticker(ticker)
        info = ticker_find.info
        
        def safe_timestamp(ts):
            return datetime.fromtimestamp(ts) if ts else None

        end = datetime(year, 12, 31)
        one_year = timedelta(days=365, hours=5, minutes=49, seconds=12)
        
        try:
            year_frac = (end-today)/one_year
        except TypeError:
            return None, None
        
        return year_frac, end
    except:
        return 0.5, datetime(year, 12, 31)  # Default fallback

# Main app logic
def main():
    # Stock ticker input
    ticker = st.text_input("Enter Stock Ticker Symbol:", value="WMT").upper()
    
    # Sidebar controls - always visible and outside button handler
    st.sidebar.subheader("Custom Parameters")
    st.sidebar.markdown("*Choose your approach and customize parameters*")
    
    # Three mutually exclusive options
    approach = st.sidebar.radio(
        "Choose your approach:",
        ["Use Default Growth (ROE × Plowback)", "Use Custom Cash Flows", "Use Custom Short-term Growth"],
        index=0
    )
    
    # Custom long-term growth and cost of equity (always available)
    st.sidebar.subheader("Other Parameters")
    
    custom_lt_growth = st.sidebar.checkbox("Use Custom Long-term Growth", value=True)
    if custom_lt_growth:
        long_term_growth = st.sidebar.number_input("Long-term Growth Rate (e.g., 0.035 for 3.5%)", 
                                                 value=0.035, format="%.4f", min_value=0.0, max_value=0.2)
    else:
        long_term_growth = 0.035
    
    custom_ke = st.sidebar.checkbox("Use Custom Cost of Equity", value=True)
    if custom_ke:
        k_e = st.sidebar.number_input("Cost of Equity (e.g., 0.10 for 10%)", 
                                     value=0.10, format="%.4f", min_value=0.0, max_value=0.5)
    else:
        k_e = 0.10  # Will be calculated later
    
    # Handle the three mutually exclusive approaches
    if approach == "Use Custom Cash Flows":
        st.sidebar.subheader("Custom Cash Flows")
        st.sidebar.markdown("*Enter your dividend projections. Growth rates will be calculated automatically.*")
        
        cf_list = []
        for i in range(1, 6):
            cf = st.sidebar.number_input(f"Year {i} Dividend ($)", 
                                       value=1.0, format="%.2f", min_value=0.0, key=f"cf_{i}")
            cf_list.append(cf)
        
        # We'll calculate growth rates later when we have the trailing dividend
        div_growth_from_prev = None  # Will be calculated later
        
    elif approach == "Use Custom Short-term Growth":
        st.sidebar.subheader("Custom Short-term Growth")
        st.sidebar.markdown("*Enter growth rate. Cash flows will be calculated automatically.*")
        
        short_term_growth = st.sidebar.number_input("Short-term Growth Rate (e.g., 0.15 for 15%)", 
                                                   value=0.15, format="%.4f", min_value=0.0, max_value=1.0)
        
        cf_list = None  # Will be calculated later
        div_growth_from_prev = None  # Will be calculated later
        
    else:  # Use Default Growth (ROE × Plowback)
        st.sidebar.subheader("Default Growth")
        st.sidebar.markdown("*Using calculated growth rate: ROE × (1 - Payout Ratio)*")
        
        cf_list = None  # Will be calculated later
        div_growth_from_prev = None  # Will be calculated later
    
    if st.button("Calculate Valuation", type="primary"):
        if ticker:
            with st.spinner("Fetching market data and calculating valuation..."):
                # Get market data
                risk_free_rate = get_risk_free_rate()
                sp500_cagr = get_equity_returns()
                market_risk_premium = sp500_cagr - risk_free_rate
                
                # Get stock data
                data = get_stock_data(ticker)
                
                if data is None:
                    st.error("Could not fetch data for this ticker. Please check the ticker symbol.")
                    return
                
                # Extract key metrics
                roe = data['Return on Equity (ROE)']
                div_payout = data['Dividend Payout Ratio']
                near_term_div_growth = roe * (1 - div_payout)
                next_date = data['Next Dividend Date (datetime)']
                latest_dividend = data["Dividend Per Share (trailing)"]
                beta = data['Beta']
                last_price = data['Last Stock Price']
                name = data['Company Name']
                
                # Use calculated cost of equity if not custom
                if not custom_ke:
                    k_e = risk_free_rate + beta * (market_risk_premium)
                
                year_fraction, div_payment_date = adjustment_for_partial_year(ticker)
                
                # Display company info
                st.header(f"📋 {name}")
                
                # Create columns for metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Current Stock Price", f"${last_price:,.2f}")
                    st.metric("Trailing Dividend", f"${latest_dividend:,.2f}")
                    st.metric("Beta", f"{beta:.3f}")
                
                with col2:
                    st.metric("ROE", f"{roe*100:.2f}%")
                    st.metric("Payout Ratio", f"{div_payout*100:.2f}%")
                    st.metric("Calculated Growth", f"{near_term_div_growth*100:.2f}%")
                
                with col3:
                    st.metric("Risk-free Rate", f"{risk_free_rate*100:.2f}%")
                    st.metric("Market Risk Premium", f"{market_risk_premium*100:.2f}%")
                    st.metric("Cost of Equity", f"{k_e*100:.2f}%")
                
                # Warning for non-dividend stocks
                if next_date is None:
                    st.warning("⚠️ This stock does not pay a dividend. Consider using a different valuation method.")
                
                # Handle cash flows based on approach
                if approach == "Use Custom Cash Flows":
                    # Use the custom cash flows entered by user
                    # Calculate growth rates from the custom cash flows
                    div_growth_from_prev = [(cf_list[0] - latest_dividend) / latest_dividend]
                    div_growth_from_prev += [(cf_list[i] - cf_list[i - 1]) / cf_list[i - 1] for i in range(1, len(cf_list))]
                    
                    # Display the calculated growth rates
                    st.sidebar.markdown("**Calculated Growth Rates:**")
                    for i, growth in enumerate(div_growth_from_prev):
                        st.sidebar.markdown(f"Year {i+1}: {growth*100:.2f}%")
                    
                elif approach == "Use Custom Short-term Growth":
                    # Calculate cash flows using the custom growth rate
                    cf_list = [latest_dividend * (1 + short_term_growth) ** i for i in range(1, 6)]
                    div_growth_from_prev = [short_term_growth] * 5
                    
                    # Display the calculated cash flows
                    st.sidebar.markdown("**Calculated Cash Flows:**")
                    for i, cf in enumerate(cf_list):
                        st.sidebar.markdown(f"Year {i+1}: ${cf:.2f}")
                        
                else:  # Use Default Growth (ROE × Plowback)
                    # Calculate cash flows using the default growth rate
                    cf_list = [latest_dividend * (1 + near_term_div_growth) ** i for i in range(1, 6)]
                    div_growth_from_prev = [near_term_div_growth] * 5
                    
                    # Display the calculated cash flows
                    st.sidebar.markdown("**Calculated Cash Flows:**")
                    for i, cf in enumerate(cf_list):
                        st.sidebar.markdown(f"Year {i+1}: ${cf:.2f}")
                
                # Calculate valuation
                periods = [1, 2, 3, 4, 5]
                adjustment_for_partial_year_list = [year_fraction, 1.0, 1.0, 1.0, 1.0]
                
                terminal_value = [0] * 5
                perp_cf = cf_list[-1]
                term_val = perpetuity_pv(perp_cf, long_term_growth, k_e)
                terminal_value[-1] = term_val
                
                dividend_dates = [div_payment_date, 
                                div_payment_date + relativedelta(years=1), 
                                div_payment_date + relativedelta(years=2), 
                                div_payment_date + relativedelta(years=3), 
                                div_payment_date + relativedelta(years=4)]
                
                periods_to_discount = [year_fraction, 1 + year_fraction, 2 + year_fraction, 3 + year_fraction, 4 + year_fraction]
                
                adjusted_cash_flows = [a*b for a, b in zip(cf_list, adjustment_for_partial_year_list)]
                in_period_sum = [sum(x) for x in zip(adjusted_cash_flows, terminal_value)]
                period_pv = [a/(1+k_e)**b for a, b in zip(in_period_sum, periods_to_discount)]
                
                # Create results dataframe
                cash_flow_table = pd.DataFrame({
                    'Periods': periods, 
                    'Dividend Date': dividend_dates, 
                    'Periods to Discount': periods_to_discount, 
                    'Dividend Cash Flows': cf_list,
                    'Dividend Growth from Previous': div_growth_from_prev,
                    'Adjustment for Partial Year': adjustment_for_partial_year_list,
                    'Adjusted Dividend Cash Flow': adjusted_cash_flows,
                    'Terminal Value': terminal_value,
                    'Period Sum': in_period_sum,
                    'Period PV': period_pv
                })
                
                cash_flow_table = cash_flow_table.set_index('Periods')
                stock_value = cash_flow_table['Period PV'].sum()
                
                # Display results
                st.header("📊 Valuation Results")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Intrinsic Value", f"${stock_value:,.2f}")
                with col2:
                    st.metric("Current Price", f"${last_price:,.2f}")
                with col3:
                    if stock_value > last_price:
                        st.metric("Recommendation", "BUY", delta="Undervalued")
                    elif stock_value < last_price:
                        st.metric("Recommendation", "SELL", delta="Overvalued", delta_color="inverse")
                    else:
                        st.metric("Recommendation", "HOLD", delta="Fair Value")
                
                # Display cash flow table - TRANSPOSED like in original code
                st.subheader("📋 Cash Flow Analysis")
                
                # Create a clean version of the table for display
                display_table = cash_flow_table.copy()
                
                # Convert dates to strings to avoid Arrow serialization issues
                display_table['Dividend Date'] = display_table['Dividend Date'].astype(str)
                
                # Round numeric columns
                numeric_columns = ['Dividend Cash Flows', 'Dividend Growth from Previous', 
                                 'Adjustment for Partial Year', 'Adjusted Dividend Cash Flow',
                                 'Terminal Value', 'Period Sum', 'Period PV']
                
                for col in numeric_columns:
                    if col in display_table.columns:
                        display_table[col] = display_table[col].round(2)
                
                # Display the transposed table
                st.dataframe(display_table.T, use_container_width=True)
                
                # Create visualization
                st.subheader("📈 Cash Flow Visualization")
                
                # Prepare data for plotting
                plot_data = cash_flow_table.reset_index()
                
                fig = go.Figure()
                
                # Add dividend cash flows
                fig.add_trace(go.Bar(
                    x=plot_data['Periods'],
                    y=plot_data['Dividend Cash Flows'],
                    name='Dividend Cash Flows',
                    marker_color='lightblue'
                ))
                
                # Add terminal value
                fig.add_trace(go.Bar(
                    x=plot_data['Periods'],
                    y=plot_data['Terminal Value'],
                    name='Terminal Value',
                    marker_color='orange'
                ))
                
                # Add present values
                fig.add_trace(go.Scatter(
                    x=plot_data['Periods'],
                    y=plot_data['Period PV'],
                    mode='lines+markers',
                    name='Present Value',
                    line=dict(color='red', width=3)
                ))
                
                fig.update_layout(
                    title="Cash Flow Breakdown by Period",
                    xaxis_title="Period",
                    yaxis_title="Value ($)",
                    barmode='stack',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary statistics
                st.subheader("📊 Summary Statistics")
                summary_stats = {
                    "Total Present Value": f"${stock_value:,.2f}",
                    "Current Market Price": f"${last_price:,.2f}",
                    "Valuation Difference": f"${stock_value - last_price:,.2f}",
                    "Valuation Ratio": f"{stock_value/last_price:.2f}",
                    "Implied Return": f"{((stock_value/last_price)**(1/5) - 1)*100:.2f}%"
                }
                
                summary_df = pd.DataFrame(list(summary_stats.items()), columns=['Metric', 'Value'])
                st.dataframe(summary_df, use_container_width=True)

if __name__ == "__main__":
    main() 