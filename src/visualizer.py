# src/visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def plot_sml(results_df, risk_free_rate, market_return, output_dir):
    """
    Plots the Security Market Line (SML) and saves the plot to a file.
    """
    # Set plot style
    sns.set_style('whitegrid')
    
    # Get data from results
    betas = results_df['Beta']
    actual_returns = results_df['Actual Return (Annualized)']
    
    # Determine plot limits
    beta_min, beta_max = min(betas) - 0.2, max(betas) + 0.2
    return_min, return_max = min(actual_returns) - 0.05, max(actual_returns) + 0.05
    
    # Create the SML line
    sml_x = np.linspace(beta_min, beta_max, 100)
    sml_y = risk_free_rate + sml_x * (market_return - risk_free_rate)
    
    # Create the plot
    plt.figure(figsize=(12, 7))
    plt.plot(sml_x, sml_y, color='red', linestyle='--', label='Security Market Line (SML)')
    
    # Plot the stocks
    plt.scatter(betas, actual_returns, color='blue', s=50, label='Portfolio Stocks')
    
    # Annotate each point with the stock ticker
    for i, txt in enumerate(results_df['Stock']):
        plt.annotate(txt.replace('.NS', ''), (betas[i], actual_returns[i]),
                     xytext=(5, -5), textcoords='offset points')
                     
    # Add plot labels and title
    plt.title('Security Market Line (SML) vs. Portfolio Stocks', fontsize=16)
    plt.xlabel(r'Beta ($\beta$)', fontsize=12)
    plt.ylabel('Expected Return (Annualized)', fontsize=12)
    plt.xlim(beta_min, beta_max)
    plt.ylim(return_min, return_max)
    plt.legend()
    
    # --- NEW: Save the plot to a file ---
    plot_filepath = os.path.join(output_dir, 'SML_Plot.png')
    plt.savefig(plot_filepath, dpi=300, bbox_inches='tight')
    print(f"\nPlot saved to {plot_filepath}")
    
    # Show the plot
    print("Displaying the SML plot...")
    plt.show()