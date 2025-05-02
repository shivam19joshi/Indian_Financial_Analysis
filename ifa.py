import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page settings
st.set_page_config(page_title="Indian Stock Visualizer", layout="wide")

st.title("📊 Indian Stock Price Viewer")

# Date range
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2025, 5, 1)

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
        df = yf.download(symbol, start=start_date, end=end_date)
        if not df.empty:
            df.columns = df.columns.get_level_values(0)  # flatten columns
            df = df.reset_index()
            df['Symbol'] = name
            all_data.append(df)
    
    return pd.concat(all_data, axis=0) if all_data else pd.DataFrame()

# Load stock data
df = load_data()

if df.empty:
    st.error("Failed to load stock data. Please check your internet connection or try again later.")
else:
    # Sidebar for stock selection
    stock_list = df['Symbol'].unique().tolist()
    selected_stock = st.sidebar.selectbox("Select a Stock", stock_list)

    stk = df[df['Symbol'] == selected_stock]

    st.subheader(f"📈 Closing Price for {selected_stock}")

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=stk, x='Date', y='Close', ax=ax)
    plt.xlabel("Date")
    plt.ylabel("Closing Price (INR)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
