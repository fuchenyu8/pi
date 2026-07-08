import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Pet number data for different countries (2019-2023)
years = np.array([2019, 2020, 2021, 2022, 2023])
us_cat_data = np.array([9420, 6500, 9420, 7380, 7380])  # US cat pet numbers
us_dog_data = np.array([8970, 8500, 8970, 8970, 8010])  # US dog pet numbers

france_cat_data = np.array([1300, 1490, 1510, 1490, 1660])  # France cat pet numbers
france_dog_data = np.array([740, 775, 750, 760, 990])  # France dog pet numbers

germany_cat_data = np.array([1470, 1570, 1670, 1520, 1570])  # Germany cat pet numbers
germany_dog_data = np.array([1010, 1070, 1030, 1060, 1050])  # Germany dog pet numbers

# ARIMA model for forecasting
def arima_forecast(data, forecast_years=3):
    model = ARIMA(data, order=(2, 1, 2))  # ARIMA model (p=2, d=1, q=2)
    fit_model = model.fit()  # Fit the model
    forecast = fit_model.forecast(steps=forecast_years)  # Forecast the next years
    return forecast

# Forecasting pet numbers for each country
us_cat_forecast = arima_forecast(us_cat_data, forecast_years=3)  # US cat forecast
us_dog_forecast = arima_forecast(us_dog_data, forecast_years=3)  # US dog forecast

france_cat_forecast = arima_forecast(france_cat_data, forecast_years=3)  # France cat forecast
france_dog_forecast = arima_forecast(france_dog_data, forecast_years=3)  # France dog forecast

germany_cat_forecast = arima_forecast(germany_cat_data, forecast_years=3)  # Germany cat forecast
germany_dog_forecast = arima_forecast(germany_dog_data, forecast_years=3)  # Germany dog forecast

# Future years for prediction
years_future = np.array([2024, 2025, 2026])  # Future years

# Set font to ensure correct display of text in the chart
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei to display Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Fix issue with negative signs

# Plotting the forecast results
plt.figure(figsize=(18, 12))  # Adjust figure size

# US cat pet number forecast
plt.subplot(2, 3, 1)
plt.plot(years, us_cat_data, 'o-', label="Historical Data", color='blue')
plt.plot(years_future, us_cat_forecast, 's--', label="Forecast Data", color='orange')
plt.title("US Pet Cat Number Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number (10k cats)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid()

# US dog pet number forecast
plt.subplot(2, 3, 2)
plt.plot(years, us_dog_data, 'o-', label="Historical Data", color='green')
plt.plot(years_future, us_dog_forecast, 's--', label="Forecast Data", color='red')
plt.title("US Pet Dog Number Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number (10k dogs)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid()

# France cat pet number forecast
plt.subplot(2, 3, 3)
plt.plot(years, france_cat_data, 'o-', label="Historical Data", color='purple')
plt.plot(years_future, france_cat_forecast, 's--', label="Forecast Data", color='orange')
plt.title("France Pet Cat Number Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number (10k cats)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid()

# France dog pet number forecast
plt.subplot(2, 3, 4)
plt.plot(years, france_dog_data, 'o-', label="Historical Data", color='cyan')
plt.plot(years_future, france_dog_forecast, 's--', label="Forecast Data", color='red')
plt.title("France Pet Dog Number Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number (10k dogs)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid()

# Germany cat pet number forecast
plt.subplot(2, 3, 5)
plt.plot(years, germany_cat_data, 'o-', label="Historical Data", color='darkblue')
plt.plot(years_future, germany_cat_forecast, 's--', label="Forecast Data", color='orange')
plt.title("Germany Pet Cat Number Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number (10k cats)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid()

# Germany dog pet number forecast
plt.subplot(2, 3, 6)
plt.plot(years, germany_dog_data, 'o-', label="Historical Data", color='yellow')
plt.plot(years_future, germany_dog_forecast, 's--', label="Forecast Data", color='red')
plt.title("Germany Pet Dog Number Forecast", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number (10k dogs)", fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=10)
plt.grid()


# Adjust layout to avoid overlapping
plt.tight_layout()
plt.show()

# Print forecast results
print("US Pet Cat Number Forecast (10k cats):", us_cat_forecast)
print("US Pet Dog Number Forecast (10k dogs):", us_dog_forecast)
print("France Pet Cat Number Forecast (10k cats):", france_cat_forecast)
print("France Pet Dog Number Forecast (10k dogs):", france_dog_forecast)
print("Germany Pet Cat Number Forecast (10k cats):", germany_cat_forecast)
print("Germany Pet Dog Number Forecast (10k dogs):", germany_dog_forecast)
