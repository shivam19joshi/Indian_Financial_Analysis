import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import seaborn as sb
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Stock Price Viewer", layout="wide")

# Title
st.title("📈 Indian Stock Price Visualizer")

# Date range
s = datetime.datetime(2023, 1, 1)
e = datetime.datetime(2025, 5, 1)

@st.cache_data
def load_data():
    tickers = {
        'WIPRO': 'WIPRO.NS',
        'TCS': 'TCS.NS',
        'IRFC': 'IRFC.NS',
        'IRCTC': 'IRCTC.NS',
        'MRF': 'MRF.NS',
        'HDFC': 'HDFCBANK.NS'
    }

    all_data = []
    for name, symbol in tickers.items():
        df = yf.download(symbol, start=s, end=e)
        df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        df['Symbol'] = name
        all_data.append(df)

    return pd.concat(all_data, axis=0)

df = load_data()

# Stock selection
stock_options = df['Symbol'].unique().tolist()
st.sidebar.title("Select a Stock")
selected_stock = st.sidebar.selectbox("Choose a stock to visualize:", stock_options)

# Filtered data
stk = df[df['Symbol'] == selected_stock]

# Plotting
st.subheader(f"Closing Price Trend for {selected_stock}")
fig, ax = plt.subplots(figsize=(12, 5))
sb.lineplot(x='Date', y='Close', data=stk, ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Closing Price (INR)")
st.pyplot(fig)
