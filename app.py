import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="India Crypto Scanner", layout="wide")
st.title("🇮🇳 Delta India & CoinDCX Funding Scanner")

def get_delta_india_rates():
    try:
        # Delta India Public API Ticker endpoint
        url = "https://api.delta.exchange/v2/tickers"
        response = requests.get(url).json()
        data = []
        for item in response['result']:
            if 'funding_rate' in item and item['funding_rate'] is not None:
                data.append({
                    "Symbol": item['symbol'],
                    "Exchange": "Delta India",
                    "Funding Rate %": float(item['funding_rate']) * 100,
                    "Mark Price": item['mark_price']
                })
        return data
    except:
        return []

def get_coindcx_rates():
    try:
        # CoinDCX public futures info
        url = "https://api.coindcx.com/exchange/v1/derivatives/futures/data"
        response = requests.get(url).json()
        data = []
        for item in response:
            data.append({
                "Symbol": item['pair'],
                "Exchange": "CoinDCX",
                "Funding Rate %": float(item['funding_rate']) * 100,
                "Mark Price": item['last_price']
            })
        return data
    except:
        return []

# Dashboard UI
if st.button('Manual Refresh'):
    st.rerun()

all_data = get_delta_india_rates() + get_coindcx_rates()

if all_data:
    df = pd.DataFrame(all_data)
    # Highlight high funding
    def color_high_funding(val):
        color = 'red' if abs(val) > 0.05 else 'white'
        return f'color: {color}'

    st.dataframe(df.style.applymap(color_high_funding, subset=['Funding Rate %']))
else:
    st.error("Data fetch nahi ho raha. Check API status.")

st.info("Note: Delta India funding har 8 ghante mein update hoti hai.")
