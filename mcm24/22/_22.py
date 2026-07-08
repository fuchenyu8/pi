import matplotlib.pyplot as plt
import numpy as np

# Initial data
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
market_sizes = [836.2, 886.1, 940.6, 1057, 1172, 1360, 1437]  # in hundreds of millions
pet_counts = [8180, 8378, 9378, 9612, 9852, 10197, 10360]    # in ten thousand pets

# Annual growth rates (calculated previously)
annual_growth_rate_pets = 0.025  # Pet quantity growth rate
annual_growth_rate_consumption = 0.04  # Per capita consumption growth rate

# Calculate per capita consumption for 2023
last_market_size = market_sizes[-1]
last_pet_count = pet_counts[-1]
last_per_capita_consumption = last_market_size * 10**8 / (last_pet_count * 10**4)

# Predict data for the next three years
future_years = [2024, 2025, 2026]
future_pet_counts = []  # Pet quantities
future_per_capita_consumption = []  # Per capita consumption
future_market_sizes = []  # Market sizes

for i in range(3):
    # Predict pet quantity
    new_pet_count = last_pet_count * (1 + annual_growth_rate_pets)
    future_pet_counts.append(new_pet_count)
    
    # Predict per capita consumption
    new_per_capita_consumption = last_per_capita_consumption * (1 + annual_growth_rate_consumption)
    future_per_capita_consumption.append(new_per_capita_consumption)
    
    # Predict market size
    new_market_size = new_pet_count * new_per_capita_consumption * 10**4 / 10**8  # Convert to hundred millions
    future_market_sizes.append(new_market_size)
    
    # Update data for the next year
    last_pet_count = new_pet_count
    last_per_capita_consumption = new_per_capita_consumption

# Combine historical data and forecast data
all_years = years + future_years
all_market_sizes = market_sizes + future_market_sizes

# Visualization
plt.figure(figsize=(10, 6))

# Plot market size data
plt.plot(all_years, all_market_sizes, marker='o', color='b', label='Market Size (hundred millions)')

# Set title and labels
plt.title('Global Pet Food Market Size (2017-2026)')
plt.xlabel('Year')
plt.ylabel('Market Size (hundred millions)')

# Set x-axis ticks
plt.xticks(all_years)

# Show grid
plt.grid(True)

# Show legend
plt.legend()

# Display the plot
plt.tight_layout()  # Adjust layout automatically
plt.show()
