# 📊 Stock Performance And Risk Tool for Analysis (SPARTA)

**SPARTA** is a Python-based data science application that analyzes the performance and risk profile of stock tickers using historical market data. It calculates risk using a custom point system based on Value at Risk (VaR) and Beta, then classifies stocks into clear, color-coded risk levels. The tool is presented through an interactive web interface built with Streamlit.

---

## 🧠 Project Overview

This tool was developed as part of a data science project focused on stock risk modeling and team collaboration. The app allows users to input multiple stock tickers and receive an intuitive breakdown of each stock’s risk level, based on financial statistics derived from Yahoo Finance.

- 📅 Timeline: August 2024 – December 2024  
- 👥 Team: 4 members | Role: **Team Lead**  
- 🌐 Interface: Streamlit  
- 🧮 Key Metrics: Value at Risk (VaR), Beta  
- 💻 Tools: `Python`, `yfinance`, `pandas`, `numpy`, `Streamlit`

---

## 🚀 Features

- 🔍 Pulls live historical data for multiple stock tickers
- 📉 Computes:
  - **Value at Risk (VaR)** at 60% confidence level
  - **Beta** compared to the S&P 500
- 🎯 Uses a custom scoring algorithm to assign risk levels:
  - Very Low Risk
  - Low Risk
  - Moderate Risk
  - High Risk
- 🧠 Sorts results by input order or by risk level
- 🌈 Color-coded, interactive UI with a clean "money green" theme

---

## 🛠️ How to Use

1. **Clone this repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SPARTA.git
   cd SPARTA
2. **Install required packages**
3. **Run Streamlit App:** 
   streamlit run projectmodelapp.py


**Sample Input:**
Analyzing: AAPL, TSLA, NVDA

AAPL - Moderate Risk
TSLA - High Risk
NVDA - Low Risk