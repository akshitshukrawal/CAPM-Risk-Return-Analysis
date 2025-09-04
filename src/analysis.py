# src/analysis.py

import numpy as np
import pandas as pd
import statsmodels.api as sm

def calculate_monthly_returns(price_data):
    """Calculates monthly log returns from price data."""
    # Resample to monthly frequency, taking the last price of the month
    monthly_prices = price_data.resample('ME').last()
    # Calculate log returns
    monthly_returns = np.log(monthly_prices / monthly_prices.shift(1))
    return monthly_returns.dropna()

def calculate_beta_alpha(stock_returns, market_returns):
    """
    Calculates the beta and alpha of a stock using linear regression.
    """
    # Add a constant to the independent variable (market returns) for the regression intercept
    X = sm.add_constant(market_returns)
    # The dependent variable is the stock returns
    y = stock_returns
    
    # Fit the Ordinary Least Squares (OLS) model
    model = sm.OLS(y, X).fit()
    
    # The intercept is alpha, the coefficient is beta
    alpha, beta = model.params
    
    return alpha, beta

def run_capm_analysis(returns_df, market_ticker, risk_free_rate):
    """
    Performs the full CAPM analysis for all stocks.

    Args:
        returns_df (pd.DataFrame): DataFrame of monthly returns for stocks and the market.
        market_ticker (str): The ticker for the market index.
        risk_free_rate (float): The annual risk-free rate.

    Returns:
        pd.DataFrame: A DataFrame with results (Beta, Actual Return, Expected Return).
    """
    # Get the market returns
    market_returns = returns_df[market_ticker]
    # Get the stock returns (all columns except the market)
    stock_returns_df = returns_df.drop(columns=market_ticker)
    
    # Convert annual risk-free rate to monthly
    monthly_risk_free_rate = (1 + risk_free_rate)**(1/12) - 1
    
    # Calculate average annualized market return
    avg_annual_market_return = market_returns.mean() * 12
    
    results = []
    
    for stock_ticker in stock_returns_df.columns:
        stock_returns = stock_returns_df[stock_ticker]
        
        # Calculate beta and alpha for the stock
        alpha, beta = calculate_beta_alpha(stock_returns, market_returns)
        
        # Calculate expected return using CAPM
        expected_return_annual = risk_free_rate + beta * (avg_annual_market_return - risk_free_rate)
        
        # Calculate actual annualized return for the stock
        actual_return_annual = stock_returns.mean() * 12
        
        results.append({
            'Stock': stock_ticker,
            'Beta': beta,
            'Alpha (Annualized)': alpha * 12,
            'Actual Return (Annualized)': actual_return_annual,
            'Expected Return (CAPM)': expected_return_annual
        })
        
    return pd.DataFrame(results)