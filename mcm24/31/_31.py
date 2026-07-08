import matplotlib.pyplot as plt
import numpy as np

# Data for the past 5 years (corrected 2019 data)
years = [2019, 2020, 2021, 2022, 2023]
production_values = [440.7, 727.3, 1554, 1508, 2793]
# Export values in RMB for 2019 converted to USD
export_values_rmb = [154.1, 9.8, 12.2, 24.7, 39.6]  # RMB data
exchange_rate = 6.9066  # Exchange rate for RMB to USD

# Calculate the export value for 2019 (convert RMB to USD)
export_values = [value / exchange_rate if i == 0 else value for i, value in enumerate(export_values_rmb)]

# Use a linear regression model for predictions
from sklearn.linear_model import LinearRegression

years_for_prediction = np.array([2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)
future_years = np.array([2024, 2025, 2026]).reshape(-1, 1)

# Production value prediction
model_prod = LinearRegression()
model_prod.fit(years_for_prediction, production_values)
predicted_production = model_prod.predict(future_years)

# Export value prediction
model_export = LinearRegression()
model_export.fit(years_for_prediction, export_values)
predicted_export = model_export.predict(future_years)

# Visualize historical data and predictions
plt.figure(figsize=(10, 6))

# Production value plot
plt.subplot(1, 2, 1)
plt.plot(years, production_values, label="Historical Data (Production Value)", marker='o', color='blue')
plt.plot([2024, 2025, 2026], predicted_production, label="Predicted Data (Production Value)", linestyle='--', marker='x', color='red')
plt.xlabel("Year")
plt.ylabel("Production Value (Billion RMB)")
plt.title("China Pet Food Production Value")
plt.legend()

# Export value plot
plt.subplot(1, 2, 2)
plt.plot(years, export_values, label="Historical Data (Export Value)", marker='o', color='green')
plt.plot([2024, 2025, 2026], predicted_export, label="Predicted Data (Export Value)", linestyle='--', marker='x', color='orange')
plt.xlabel("Year")
plt.ylabel("Export Value (Billion USD)")
plt.title("China Pet Food Export Value")
plt.legend()

plt.tight_layout()
plt.show()
