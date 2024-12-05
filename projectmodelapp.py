# %%
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Global styles for "money green" theme
st.markdown(
    """
    <style>
    body {
        color: #4CAF50 !important;  /* Money green text for everything */
    }
    .stTextInput > div > div > input {
        color: #4CAF50;  /* Input field text */
    }
    .stButton > button {
        background-color: #4CAF50 !important;  /* Green button background */
        color: black !important;  /* Black button text for contrast */
    }
    h1, h2, h3, h4, h5, h6 {
        color: #4CAF50 !important;  /* Green for all headers */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define functions for risk calculation
def calculate_var(daily_returns, confidence_level=0.6):
    var = daily_returns.quantile(1 - confidence_level)
    return var

def calculate_beta(ticker_returns, market_returns):
    covariance = ticker_returns.cov(market_returns)
    market_variance = market_returns.var()
    beta = covariance / market_variance
    return beta

def assign_risk_level(var, beta):
    score = 0
    if var > -0.15:
        score += 1
    elif -0.15 <= var <= -0.35:
        score += 2
    elif -0.35 <= var < -0.5:
        score += 3
    else:
        score += 4

    if abs(beta) < 0.5:
        score += 0.5
    elif 0.5 <= abs(beta) <= 1:
        score += 1
    elif 1 <= abs(beta) <= 1.3:
        score += 1.5
    else:
        score += 2

    if score <= 2:
        return "Very Low Risk", score
    elif score <= 4:
        return "Low Risk", score
    elif score <= 5.5:
        return "Moderate Risk", score
    else:
        return "High Risk", score

# Initialize session state to persist results across interactions
if "risk_assessment" not in st.session_state:
    st.session_state.risk_assessment = {}
    st.session_state.metrics = {}
    st.session_state.tickers = []
    st.session_state.sorted_tickers = []

# Streamlit App Interface
st.title("Stock Performance And Risk Tool for Analysis (SPARTA)")

# User input for stock tickers
tickers = st.text_input("Enter stock tickers (comma-separated):")

if st.button("Analyze"):
    if tickers:
        tickers = [ticker.strip().upper() for ticker in tickers.split(",")]

        # Fetch data for past 2 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2 * 365)

        data = {}
        for ticker in tickers:
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            data[ticker] = stock_data['Adj Close']

        df = pd.DataFrame(data)
        df.fillna(method='ffill', inplace=True)
        df.dropna(inplace=True)

        daily_returns = df.pct_change().dropna()
        sp500_data = yf.download('^GSPC', start=start_date, end=end_date)['Adj Close']
        market_returns = sp500_data.pct_change().dropna()

        # Risk assessment
        risk_assessment = {}
        for ticker in tickers:
            var = calculate_var(daily_returns[ticker]) * 100
            beta = calculate_beta(daily_returns[ticker], market_returns)
            risk_level, score = assign_risk_level(var, beta)
            risk_assessment[ticker] = {"level": risk_level, "score": score}

        # Store results in session state
        st.session_state.risk_assessment = risk_assessment
        st.session_state.tickers = tickers

# Ensure risk assessment persists after sorting
if st.session_state.risk_assessment:
    # Sort options
    sort_order = st.radio(
        "Sort the tickers based on:",
        options=["Input Order", "Low Risk to High Risk", "High Risk to Low Risk"],
        key="sort_order"
    )

    # Sorting logic
    risk_assessment = st.session_state.risk_assessment
    if sort_order == "Low Risk to High Risk":
        st.session_state.sorted_tickers = sorted(risk_assessment.items(), key=lambda x: x[1]["score"])
    elif sort_order == "High Risk to Low Risk":
        st.session_state.sorted_tickers = sorted(risk_assessment.items(), key=lambda x: x[1]["score"], reverse=True)
    else:
        st.session_state.sorted_tickers = [(ticker, risk_assessment[ticker]) for ticker in st.session_state.tickers]

    # Dynamic styling for risk levels
    color_map = {
        "Very Low Risk": "#4CAF50",  # Money green
        "Low Risk": "#FFFF00",       # Yellow
        "Moderate Risk": "#FFA500",  # Orange
        "High Risk": "#FF0000"       # Red
    }

    st.subheader("Risk Assessment (Sorted)")
    for ticker, details in st.session_state.sorted_tickers:
        risk_level = details["level"]
        risk_color = color_map[risk_level]
        st.markdown(
            f"""
            <p style='font-size:20px;'>
            <span style='color:#4CAF50;'><b>{ticker}</b></span> 
            <span style='color:#4CAF50;'>-</span> 
            <span style='color:{risk_color};'>{risk_level}</span>
            </p>
            """,
            unsafe_allow_html=True
        )


# %%



