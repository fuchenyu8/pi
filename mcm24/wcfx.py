import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === Data Definition ===
years = np.array([2024, 2025, 2026])  # Predicted years
pet_count = np.array([10400, 10650, 10900])  # Predicted pet population
per_capita = np.array([123.0, 125.0, 127.0])  # Predicted per capita spending
base_market_size = pet_count * per_capita / 10000  # Initial market size (billion USD)

# Dynamic elasticity function
def beta_function(year, base_beta=0.2, beta_growth=0.05, start_year=2024):
    return base_beta + beta_growth * (year - start_year)

# Demand function
def demand_function(base_demand, tariff, beta, noise=0):
    return base_demand * np.exp(-beta * tariff) + noise

# Supply function
def supply_function(base_supply, tariff, exchange_rate, alpha, gamma, rho, noise=0):
    international_supply = base_supply * (1 + alpha * tariff + gamma * exchange_rate)  # International supply
    domestic_supply = rho * (base_supply - international_supply)  # Domestic substitution
    return international_supply + domestic_supply + noise

# === Mean and standard deviation of input parameters ===
tariff_mean, tariff_std = 0.2, 0.05  # Mean and standard deviation of tariff changes
exchange_rate_mean, exchange_rate_std = -0.01, 0.02  # Mean and standard deviation of exchange rate changes
substitution_rate = 0.5  # Domestic substitution rate

# Number of simulations
num_simulations = 1000

# Store simulation results
simulated_market_sizes = []

# Monte Carlo simulation
for _ in range(num_simulations):
    tariffs = np.random.normal(tariff_mean, tariff_std, len(years))
    exchange_rates = np.random.normal(exchange_rate_mean, exchange_rate_std, len(years))
    
    market_size_simulation = []
    for year, base_size in zip(years, base_market_size):
        tariff = tariffs[years.tolist().index(year)]
        exchange_rate = exchange_rates[years.tolist().index(year)]
        
        # Dynamic demand and supply
        beta = beta_function(year)
        adjusted_demand = demand_function(base_size, tariff, beta)
        adjusted_supply = supply_function(base_size, tariff, exchange_rate, 0.3, -0.15, substitution_rate)
        market_size_simulation.append(min(adjusted_demand, adjusted_supply))
    
    simulated_market_sizes.append(market_size_simulation)

# Convert to DataFrame
simulated_df = pd.DataFrame(simulated_market_sizes, columns=years)

# Calculate error ranges
mean_market_size = simulated_df.mean()
std_market_size = simulated_df.std()

# === Visualization of error ranges ===
plt.figure(figsize=(10, 6))
plt.plot(years, mean_market_size, label="Predicted Market Size", color='blue')
plt.fill_between(years, mean_market_size - std_market_size, mean_market_size + std_market_size, color='blue', alpha=0.2, label="Error Range")
plt.title("Market Size Prediction with Error Range", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Market Size (Billion USD)", fontsize=12)
plt.legend()
plt.grid()
plt.show()
