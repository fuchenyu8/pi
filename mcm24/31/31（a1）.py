import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Data from the past 5 years (corrected 2019 data)
years = [2019, 2020, 2021, 2022, 2023]
production_values = [440.7, 727.3, 1554, 1508, 2793]  # Production value (100 million RMB)
export_values_rmb = [154.1, 9.8, 12.2, 24.7, 39.6]  # Export value (RMB)
exchange_rate = 6.9066  # Exchange rate from RMB to USD
GDP = [99.089, 101.598, 104.895, 106.343, 108.921]  # GDP data (in trillion RMB)

# Calculate the export values for 2019 (RMB to USD)
export_values = [value / exchange_rate if i == 0 else value for i, value in enumerate(export_values_rmb)]

# Calculate GDP growth rate
GDP_growth_rate = [(GDP[i] - GDP[i-1]) / GDP[i-1] * 100 if i != 0 else 0 for i in range(len(GDP))]

# Convert data into a Pandas DataFrame
data = pd.DataFrame({
    'Year': years,
    'Production Value': production_values,
    'Export Value': export_values,
    'GDP Growth Rate': GDP_growth_rate
})

# Set year as the index for the time series
data.set_index('Year', inplace=True)

# Use ARIMAX model for predicting production value
# ARIMAX model requires one-dimensional time series data and uses GDP growth rate as an exogenous variable
# ARIMAX model for production value (optimized by AIC or BIC parameters)
model_prod = ARIMA(data['Production Value'], exog=data['GDP Growth Rate'], order=(1, 1, 1))  # ARIMAX(p,d,q)
model_prod_fit = model_prod.fit()

# ARIMAX model for predicting export value (optimized by AIC or BIC parameters)
model_export = ARIMA(data['Export Value'], exog=data['GDP Growth Rate'], order=(1, 1, 1))
model_export_fit = model_export.fit()

# Forecast for the next three years
future_GDP_growth_rate = [2.2, 2.1, 2.0]  # Assumed GDP growth rate for the next three years (percentage)
future_years = [2024, 2025, 2026]

# Pair future GDP growth rate with years and convert it to an array
future_data = np.array(future_GDP_growth_rate).reshape(-1, 1)

# Predict production value and export value
forecast_prod = model_prod_fit.forecast(steps=3, exog=future_data)
forecast_export = model_export_fit.forecast(steps=3, exog=future_data)

# Print the forecast results
print(f"Predicted Production Values for 2024, 2025, 2026: {forecast_prod}")
print(f"Predicted Export Values for 2024, 2025, 2026: {forecast_export}")

# Visualize the historical data and forecast results
plt.figure(figsize=(12, 6))

# Production value plot
plt.subplot(1, 2, 1)
plt.plot(data.index, data['Production Value'], label="Historical Data (Production Value)", marker='o', color='blue')
plt.plot(future_years, forecast_prod, label="Forecasted Data (Production Value)", linestyle='--', marker='x', color='red')
plt.xlabel("Year")
plt.ylabel("Production Value (100 million RMB)")
plt.title("China Pet Food Production Value with GDP Growth Rate")
plt.legend()

# Export value plot
plt.subplot(1, 2, 2)
plt.plot(data.index, data['Export Value'], label="Historical Data (Export Value)", marker='o', color='green')
plt.plot(future_years, forecast_export, label="Forecasted Data (Export Value)", linestyle='--', marker='x', color='orange')
plt.xlabel("Year")
plt.ylabel("Export Value (Billion USD)")
plt.title("China Pet Food Export Value with GDP Growth Rate")
plt.legend()

plt.tight_layout()
plt.show()
