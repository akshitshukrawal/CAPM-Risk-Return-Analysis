# main.py

import os
import pandas as pd
from src.data_fetcher import download_price_data
from src.analysis import calculate_monthly_returns, run_capm_analysis
from src.visualizer import plot_sml

def main():
    """
    Main function to run the CAPM analysis and visualization project.
    """
    # --- Project Configuration ---
    # Note: .NS suffix is for stocks listed on the National Stock Exchange of India
    STOCK_TICKERS = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'HINDUNILVR.NS', 
        'INFY.NS', 'ICICIBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS'
    ]
    MARKET_TICKER = '^NSEI'  # NIFTY 50 Index
    
    # Combine all tickers for a single download request
    ALL_TICKERS = STOCK_TICKERS + [MARKET_TICKER]
    
    START_DATE = '2020-01-01'
    END_DATE = '2024-12-31'
    
    # Annual risk-free rate (e.g., yield on a 10-year government bond)
    RISK_FREE_RATE = 0.07
    
    # --- NEW: Create data directory if it doesn't exist ---
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)

    # --- Step 1: Fetch Data ---
    price_data = download_price_data(ALL_TICKERS, START_DATE, END_DATE)
    
    if price_data is None or price_data.empty:
        print("Failed to download data. Exiting.")
        return

    # --- Step 2: Calculate Returns ---
    monthly_returns = calculate_monthly_returns(price_data)

    # --- Step 3: Run CAPM Analysis ---
    print("\nRunning CAPM analysis...")
    capm_results = run_capm_analysis(monthly_returns, MARKET_TICKER, RISK_FREE_RATE)
    
    # --- Step 4: Display and Save Results ---
    print("\n--- CAPM Analysis Results ---")
    print(capm_results.to_string())
    
    # --- NEW: Save the results DataFrame to a CSV file ---
    results_filepath = os.path.join(output_dir, 'capm_analysis_results.csv')
    capm_results.to_csv(results_filepath, index=False)
    print(f"\nResults saved to {results_filepath}")
    
    undervalued_stocks = capm_results[capm_results['Actual Return (Annualized)'] > capm_results['Expected Return (CAPM)']]
    overvalued_stocks = capm_results[capm_results['Actual Return (Annualized)'] < capm_results['Expected Return (CAPM)']]
    
    print("\nPotentially Undervalued Stocks (Positive Alpha):")
    print(undervalued_stocks['Stock'].tolist())
    
    print("\nPotentially Overvalued Stocks (Negative Alpha):")
    print(overvalued_stocks['Stock'].tolist())

    # --- Step 5: Visualize the Security Market Line ---
    avg_market_return = monthly_returns[MARKET_TICKER].mean() * 12
    plot_sml(capm_results, RISK_FREE_RATE, avg_market_return, output_dir)

if __name__ == '__main__':
    main()