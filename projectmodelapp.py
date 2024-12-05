# %%
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define functions for risk calculation (reuse your existing functions)
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
        score += 0
    elif -0.15 <= var <= -0.35:
        score += 1
    elif -0.35 <= var < -0.5:
        score += 2
    else:
        score += 3

    if beta < 0.5:
        score += 0.5
    elif 0.5 <= beta <= 1:
        score += 1
    elif 1 <= beta <= 1.3:
        score += 1.5
    else:
        score += 2

    if score <= 2:
        return "Very Low Risk"
    elif score <= 4:
        return "Low Risk"
    elif score <= 5.5:
        return "Moderate Risk"
    else:
        return "High Risk"

# Streamlit App Interface
st.title("Stock Risk Assessment Tool")

# User input
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
        metrics = {}
        risk_assessment = {}
        for ticker in tickers:
            var = calculate_var(daily_returns[ticker]) * 100
            beta = calculate_beta(daily_returns[ticker], market_returns)
            metrics[ticker] = {"VaR (95%)": var, "Beta": beta}
            risk_assessment[ticker] = assign_risk_level(var, beta)

        st.subheader("Metrics")
        st.write(pd.DataFrame(metrics).T)

        st.subheader("Risk Assessment")
        st.write(pd.DataFrame.from_dict(risk_assessment, orient="index", columns=["Risk Level"]))
    else:
        st.error("Please enter valid tickers.")

# %%



