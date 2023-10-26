import streamlit as st
from streamlit_option_menu import option_menu
import requests
from bs4 import BeautifulSoup
from alpha_vantage.timeseries import TimeSeries
import plotly.graph_objs as go
import plotly.express as px

# Set page width and background color
st.markdown(
    """
    <style>
    .stApp {
        max-width: auto;
        background-color: #f8f8f8;
    }
    .stSelectbox {
        background-color: #2e2e2e;
        color: white;
    }
    .stButton {
        background-color: #0074cc;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and subtitle
st.title("Stock Market Predictor")
st.write("Analyze stock prices, get stock information, compare stocks, and receive stock suggestions.")

# Create a horizontal menu bar
selected_page = option_menu("Select an Option", ["Information", "Stock Price Analysis", "Compare Stocks", "Stock Suggestions"],
                            icons=['info-circle', 'chart-line', 'chart-bar', 'lightbulb'], orientation="horizontal")

# ... (rest of your code)

def get_stock_info(ticker):
    api_key = "DE1FQJ7LMFCUKVWC"  # Replace with your Alpha Vantage API key
    base_url = f"https://www.alphavantage.co/query"
    
    params = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": api_key,
    }
    response = requests.get(base_url, params=params)
    company_info = response.json()
    
    return company_info

# Page 1: Information
if selected_page == "Information":
    st.subheader("Stock Information")

    stock_info_ticker = st.text_input("Enter a Stock Ticker Symbol (e.g., AAPL):")

    if stock_info_ticker:
        stock_info = get_stock_info(stock_info_ticker)
        
        st.write("Company Info:")
        st.json(stock_info)

# Page 2: Stock Price Analysis
elif selected_page == "Stock Price Analysis":
    st.subheader("Stock Price Analysis")
    
    st.write("Analyze historical stock prices:")
    stock_price_ticker = st.text_input("Enter a Stock Ticker Symbol (e.g., AAPL):")

    if stock_price_ticker:
        try:
            api_key = "DE1FQJ7LMFCUKVWC"  # Replace with your actual API key
            ts = TimeSeries(key=api_key, output_format="pandas")
            data, meta_data = ts.get_daily(symbol=stock_price_ticker, outputsize="full")

            if not data.empty:
                fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['1. open'],
                    high=data['2. high'],
                    low=data['3. low'],
                    close=data['4. close'],
                    increasing_line_color='green', decreasing_line_color='red')])

                st.plotly_chart(fig)

            else:
                st.warning("No data available for the selected stock.")

        except Exception as e:
            st.error(f"Error retrieving data: {str(e)}")

# Page 3: Compare Stocks
elif selected_page == "Compare Stocks":
    st.subheader("Compare Stock Prices")

    stock1 = st.text_input("Enter the first Stock Ticker Symbol (e.g., AAPL):")
    stock2 = st.text_input("Enter the second Stock Ticker Symbol (e.g., GOOGL):")

    color_options = st.radio("Select Graph Color:", ("Red/Green", "Blue/Orange"))
    if color_options == "Red/Green":
        color1, color2 = "green", "red"
    else:
        color1, color2 = "blue", "orange"

    chart_options = st.radio("Select Chart Type:", ["Line Chart", "Candlestick Chart", "Bar Chart", "OHLC Chart", "3D Scatter Plot"])

    if stock1 and stock2:
        try:
            api_key = "DE1FQJ7LMFCUKVWC"  # Replace with your actual API key
            ts = TimeSeries(key=api_key, output_format="pandas")
            data1, _ = ts.get_daily(symbol=stock1, outputsize="full")
            data2, _ = ts.get_daily(symbol=stock2, outputsize="full")

            if not data1.empty and not data2.empty:
                if chart_options == "Line Chart":
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=data1.index, y=data1['4. close'], name=stock1, mode="lines", line=dict(color=color1)))
                    fig.add_trace(go.Scatter(x=data2.index, y=data2['4. close'], name=stock2, mode="lines", line=dict(color=color2)))
                elif chart_options == "Candlestick Chart":
                    fig = go.Figure(data=[go.Candlestick(x=data1.index,
                        open=data1['1. open'],
                        high=data1['2. high'],
                        low=data1['3. low'],
                        close=data1['4. close'],
                        increasing_line_color=color1, decreasing_line_color=color2)])
                    fig.add_trace(go.Candlestick(x=data2.index,
                        open=data2['1. open'],
                        high=data2['2. high'],
                        low=data2['3. low'],
                        close=data2['4. close'],
                        increasing_line_color=color2, decreasing_line_color=color1))
                elif chart_options == "Bar Chart":
                    fig = px.bar(data1, x=data1.index, y='4. close', title=f"{stock1} vs. {stock2}", labels={'4. close': 'Stock Price'}, height=400)
                    fig.add_bar(x=data2.index, y=data2['4. close'], name=stock2)
                elif chart_options == "OHLC Chart":
                    fig = go.Figure(data=go.Ohlc(x=data1.index,
                        open=data1['1. open'],
                        high=data1['2. high'],
                        low=data1['3. low'],
                        close=data1['4. close']))
                    fig.add_trace(go.Ohlc(x=data2.index,
                        open=data2['1. open'],
                        high=data2['2. high'],
                        low=data2['3. low'],
                        close=data2['4. close']))
                elif chart_options == "3D Scatter Plot":
                    fig = px.scatter_3d(data1, x=data1.index, y=data1['4. close'], z=data2['4. close'], title=f"{stock1} vs. {stock2}")
                    fig.update_traces(marker=dict(size=5))
                    fig.update_layout(scene=dict(xaxis_title='Date', yaxis_title=f'{stock1} Stock Price', zaxis_title=f'{stock2} Stock Price'))
                fig.update_layout(title="Stock Price Comparison")
                st.plotly_chart(fig)

            else:
                st.warning("No data available for the selected stocks.")

        except Exception as e:
            st.error(f"Error retrieving data: {str(e)}")

# Page 4: Stock Suggestions
elif selected_page == "Stock Suggestions":
    st.subheader("Stock Suggestions")

    stock_title = st.text_input("Enter a Stock Ticker Symbol (e.g., AAPL):")

    if stock_title:
        st.info(f"Suggestion: Here's a title suggestion for {stock_title}.")

        try:
            api_key = "DE1FQJ7LMFCUKVWC"  # Replace with your actual API key
            ts = TimeSeries(key=api_key, output_format="pandas")
            data, _ = ts.get_daily(symbol=stock_title, outputsize="compact")

            if not data.empty:
                last_close = data['4. close'].iloc[-1]
                if last_close > data['4. close'].iloc[-2]:
                    st.success(f"Suggestion: Consider buying {stock_title}.")
                else:
                    st.warning(f"Suggestion: Consider selling {stock_title}.")
            else:
                st.warning("No data available for the selected stock.")

        except Exception as e:
            st.error(f"Error retrieving stock price")
