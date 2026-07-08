import numpy as np
import matplotlib.pyplot as plt

# Historical data
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
market_sizes = [836.2, 886.1, 940.6, 1057, 1172, 1360, 1437]  # in hundred millions
pet_counts = [8180, 8378, 9378, 9612, 9852, 10197, 10360]  # in ten thousand pets

# Annual growth rates (calculated previously)
annual_growth_rate_pets = 0.025  # Pet quantity growth rate
annual_growth_rate_consumption = 0.04  # Per capita consumption growth rate

# Define segmented growth rates
growth_rate_main_food = 0.03  # Main food (dry) growth rate
growth_rate_snacks = 0.05  # Snacks growth rate
growth_rate_nutrition = 0.06  # Nutrition products growth rate
growth_rate_wet_food = 0.04  # Wet food growth rate

# GDP growth rates for 2024-2026
GDP_growth_rates = {
    2024: 0.03,  # 3%
    2025: 0.025,  # 2.5%
    2026: 0.02   # 2%
}

# Calculate per capita consumption for 2023
last_market_size = market_sizes[-1]
last_pet_count = pet_counts[-1]
last_per_capita_consumption = last_market_size * 10**8 / (last_pet_count * 10**4)

# Predict future data
future_years = [2024, 2025, 2026]
future_pet_counts = []  # Pet quantities
future_per_capita_consumption = []  # Per capita consumption
future_market_sizes = []  # Market sizes
future_main_food = []  # Main food market
future_snacks = []  # Snacks market
future_nutrition = []  # Nutrition products market
future_wet_food = []  # Wet food market

for i in range(3):
    year = future_years[i]
    # Predict pet quantity
    new_pet_count = last_pet_count * (1 + annual_growth_rate_pets)
    future_pet_counts.append(new_pet_count)
    
    # Adjust growth rate for per capita consumption based on GDP growth
    adjusted_growth_rate_consumption = annual_growth_rate_consumption + GDP_growth_rates[year]  # Adjusting consumption growth rate
    new_per_capita_consumption = last_per_capita_consumption * (1 + adjusted_growth_rate_consumption)
    future_per_capita_consumption.append(new_per_capita_consumption)
    
    # Predict overall market size
    new_market_size = new_pet_count * new_per_capita_consumption * 10**4 / 10**8  # Convert to hundred millions
    future_market_sizes.append(new_market_size)

    # Adjust segmented market sizes based on the GDP growth rate
    adjusted_growth_rate_main_food = growth_rate_main_food + GDP_growth_rates[year]  # Main food
    adjusted_growth_rate_snacks = growth_rate_snacks + GDP_growth_rates[year]  # Snacks
    adjusted_growth_rate_nutrition = growth_rate_nutrition + GDP_growth_rates[year]  # Nutrition
    adjusted_growth_rate_wet_food = growth_rate_wet_food + GDP_growth_rates[year]  # Wet food

    main_food_size = new_market_size * 0.6951 * (1 + adjusted_growth_rate_main_food)
    snacks_size = new_market_size * 0.2699 * (1 + adjusted_growth_rate_snacks)
    nutrition_size = new_market_size * 0.035 * (1 + adjusted_growth_rate_nutrition)
    wet_food_size = new_market_size * 0.253 * (1 + adjusted_growth_rate_wet_food)

    future_main_food.append(main_food_size)
    future_snacks.append(snacks_size)
    future_nutrition.append(nutrition_size)
    future_wet_food.append(wet_food_size)
    
    # Update for the next year
    last_pet_count = new_pet_count
    last_per_capita_consumption = new_per_capita_consumption

# Combine historical data and forecast data
all_years = years + future_years
all_market_sizes = market_sizes + future_market_sizes
all_main_food = [market_sizes[i] * 0.6951 for i in range(len(market_sizes))] + future_main_food
all_snacks = [market_sizes[i] * 0.2699 for i in range(len(market_sizes))] + future_snacks
all_nutrition = [market_sizes[i] * 0.035 for i in range(len(market_sizes))] + future_nutrition
all_wet_food = [market_sizes[i] * 0.253 for i in range(len(market_sizes))] + future_wet_food

# Plot the future prediction of pet food demand by segment
plt.figure(figsize=(12, 8))

# Plot segmented markets
plt.plot(all_years, all_main_food, marker='o', color='b', label='Main Food (Dry)')
plt.plot(all_years, all_snacks, marker='o', color='g', label='Snacks')
plt.plot(all_years, all_nutrition, marker='o', color='r', label='Nutrition Products')
plt.plot(all_years, all_wet_food, marker='o', color='c', label='Wet Food')

# Set title and labels
plt.title('Global Pet Food Market Demand by Segment (2017-2026) with GDP Growth Impact')
plt.xlabel('Year')
plt.ylabel('Market Demand (Hundred Millions USD)')

# Set x-axis ticks
plt.xticks(all_years)

# Show grid
plt.grid(True)

# Show legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Historical data
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
market_sizes = [836.2, 886.1, 940.6, 1057, 1172, 1360, 1437]  # in hundred millions
pet_counts = [8180, 8378, 9378, 9612, 9852, 10197, 10360]  # in ten thousand pets

# Annual growth rates (calculated previously)
annual_growth_rate_pets = 0.025  # Pet quantity growth rate
annual_growth_rate_consumption = 0.04  # Per capita consumption growth rate

# Define segmented growth rates with adjusted randomness (simulating fluctuation)
growth_rate_main_food = 0.03  # Main food (dry) growth rate
growth_rate_snacks = 0.05  # Snacks growth rate
growth_rate_nutrition = 0.06  # Nutrition products growth rate
growth_rate_wet_food = 0.04  # Wet food growth rate

# GDP growth rates for 2024-2026
GDP_growth_rates = {
    2024: 0.02, 
    2025: 0.024,  
    2026: 0.022  
}

# Calculate per capita consumption for 2023
last_market_size = market_sizes[-1]
last_pet_count = pet_counts[-1]
last_per_capita_consumption = last_market_size * 10**8 / (last_pet_count * 10**4)

# Predict future data
future_years = [2024, 2025, 2026]
future_pet_counts = []  # Pet quantities
future_per_capita_consumption = []  # Per capita consumption
future_market_sizes = []  # Market sizes
future_main_food = []  # Main food market
future_snacks = []  # Snacks market
future_nutrition = []  # Nutrition products market
future_wet_food = []  # Wet food market

for i in range(3):
    year = future_years[i]
    # Predict pet quantity with some random fluctuation
    pet_growth_fluctuation = np.random.normal(loc=annual_growth_rate_pets, scale=0.005)  # Random fluctuation
    new_pet_count = last_pet_count * (1 + pet_growth_fluctuation)
    future_pet_counts.append(new_pet_count)
    
    # Adjust growth rate for per capita consumption with random fluctuation
    consumption_growth_fluctuation = np.random.normal(loc=annual_growth_rate_consumption, scale=0.005)
    adjusted_growth_rate_consumption = annual_growth_rate_consumption + GDP_growth_rates[year] + consumption_growth_fluctuation
    new_per_capita_consumption = last_per_capita_consumption * (1 + adjusted_growth_rate_consumption)
    future_per_capita_consumption.append(new_per_capita_consumption)
    
    # Predict overall market size with possible negative fluctuations
    market_growth_fluctuation = np.random.normal(loc=1, scale=0.02)  # Adding some randomness to market growth
    new_market_size = new_pet_count * new_per_capita_consumption * 10**4 / 10**8  # Convert to hundred millions
    new_market_size *= market_growth_fluctuation
    future_market_sizes.append(new_market_size)

    # Adjust segmented market sizes with fluctuations
    adjusted_growth_rate_main_food = growth_rate_main_food + GDP_growth_rates[year] + np.random.normal(0, 0.005)
    adjusted_growth_rate_snacks = growth_rate_snacks + GDP_growth_rates[year] + np.random.normal(0, 0.005)
    adjusted_growth_rate_nutrition = growth_rate_nutrition + GDP_growth_rates[year] + np.random.normal(0, 0.005)
    adjusted_growth_rate_wet_food = growth_rate_wet_food + GDP_growth_rates[year] + np.random.normal(0, 0.005)

    main_food_size = new_market_size * 0.6951 * (1 + adjusted_growth_rate_main_food)
    snacks_size = new_market_size * 0.2699 * (1 + adjusted_growth_rate_snacks)
    nutrition_size = new_market_size * 0.035 * (1 + adjusted_growth_rate_nutrition)
    wet_food_size = new_market_size * 0.253 * (1 + adjusted_growth_rate_wet_food)

    future_main_food.append(main_food_size)
    future_snacks.append(snacks_size)
    future_nutrition.append(nutrition_size)
    future_wet_food.append(wet_food_size)
    
    # Update for the next year
    last_pet_count = new_pet_count
    last_per_capita_consumption = new_per_capita_consumption

# Combine historical data and forecast data
all_years = years + future_years
all_market_sizes = market_sizes + future_market_sizes
all_main_food = [market_sizes[i] * 0.6951 for i in range(len(market_sizes))] + future_main_food
all_snacks = [market_sizes[i] * 0.2699 for i in range(len(market_sizes))] + future_snacks
all_nutrition = [market_sizes[i] * 0.035 for i in range(len(market_sizes))] + future_nutrition
all_wet_food = [market_sizes[i] * 0.253 for i in range(len(market_sizes))] + future_wet_food

# Plot the future prediction of pet food demand by segment
plt.figure(figsize=(12, 8))

# Plot segmented markets
plt.plot(all_years, all_main_food, marker='o', color='b', label='Main Food (Dry)')
plt.plot(all_years, all_snacks, marker='o', color='g', label='Snacks')
plt.plot(all_years, all_nutrition, marker='o', color='r', label='Nutrition Products')
plt.plot(all_years, all_wet_food, marker='o', color='c', label='Wet Food')

# Set title and labels
plt.title('Global Pet Food Market Demand by Segment (2017-2026) with Economic Fluctuations')
plt.xlabel('Year')
plt.ylabel('Market Demand (Hundred Millions USD)')

# Set x-axis ticks
plt.xticks(all_years)

# Show grid
plt.grid(True)

# Show legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()
