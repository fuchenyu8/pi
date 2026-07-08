import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Input data (2012-2023)
years = np.array([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
market_size = np.array([600.6, 633.1, 710.2, 714.5, 798.4, 836.2, 886.1, 940.6, 1057, 1172, 1360, 1437])

# Convert to pandas Series for time series analysis
data = pd.Series(market_size, index=years)

# Step 1: Check stationarity using ADF test
adf_test = adfuller(data)
print("ADF Test Statistic:", adf_test[0])
print("p-value:", adf_test[1])
if adf_test[1] > 0.05:
    print("Data is non-stationary. Differencing is required.")
    data_diff = data.diff().dropna()  # First-order differencing
else:
    print("Data is stationary. Proceed without differencing.")
    data_diff = data

# Step 2: Fit ARIMA model
# Using ARIMA(1, 1, 0) based on visual inspection of the data trend
model = ARIMA(data, order=(1, 1, 0))
model_fit = model.fit()

# Step 3: Forecast future values
forecast_years = [2024, 2025, 2026]
forecast = model_fit.forecast(steps=len(forecast_years))
forecast_values = forecast.values

# Combine historical and forecasted data
all_years = np.concatenate((years, forecast_years))
all_market_size = np.concatenate((market_size, forecast_values))

# Step 4: Plot results
plt.figure(figsize=(10, 6))
plt.plot(years, market_size, 'o-', label="Historical Data", color="blue")
plt.plot(all_years, all_market_size, 's--', label="Forecast", color="orange")
plt.title("Global Pet Food Market Forecast (2012-2026)")
plt.xlabel("Year")
plt.ylabel("Market Size (Billion USD)")
plt.legend()
plt.grid()
plt.show()

# Print forecast results
print("Forecast for 2024-2026 (Billion USD):")
for year, value in zip(forecast_years, forecast_values):
    print(f"{year}: {value:.1f}")


