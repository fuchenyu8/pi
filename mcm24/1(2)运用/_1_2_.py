import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from statsmodels.tsa.arima.model import ARIMA

# Set font for Chinese and prevent issues with negative signs
rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei to display Chinese
rcParams['axes.unicode_minus'] = False   # Properly display negative signs

# Data input, including 2018 data
years = np.array([2018, 2019, 2020, 2021, 2022, 2023])
cat_data = np.array([4064, 4412, 4862, 5806, 6536, 6980])  # Including 2018 data
dog_data = np.array([5085, 5503, 5222, 5429, 5119, 5175])  # Including 2018 data

# ARIMA model forecasting
def arima_forecast(data, forecast_years=3):
    model = ARIMA(data, order=(2, 1, 2))  # Select (2, 1, 2) for ARIMA model parameters
    fit_model = model.fit()
    forecast = fit_model.forecast(steps=forecast_years)
    return np.concatenate((fit_model.fittedvalues, forecast)), fit_model

# Forecast the next three years
cat_predictions, cat_fit_model = arima_forecast(cat_data, forecast_years=3)
dog_predictions, dog_fit_model = arima_forecast(dog_data, forecast_years=3)

# Define future years
future_years = np.array([2024, 2025, 2026])
all_years = np.concatenate((years, future_years))

# Plotting
plt.figure(figsize=(12, 6))

# Pet cat
plt.subplot(1, 2, 1)
plt.plot(years, cat_data, 'o-', label="Historical Data", color='blue')
plt.plot(all_years, cat_predictions, 's--', label="Forecast Data", color='orange')
plt.title("Pet Cat Quantity Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Quantity (in ten thousand)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend()
plt.grid()

# Pet dog
plt.subplot(1, 2, 2)
plt.plot(years, dog_data, 'o-', label="Historical Data", color='green')
plt.plot(all_years, dog_predictions, 's--', label="Forecast Data", color='red')
plt.title("Pet Dog Quantity Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Quantity (in ten thousand)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend()
plt.grid()

# Display the plot
plt.tight_layout()
plt.show()

# Print the results
print("Forecast for the next three years for pet cats:", cat_predictions[-3:])
print("Forecast for the next three years for pet dogs:", dog_predictions[-3:])
