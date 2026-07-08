import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# Historical data
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
market_sizes = [836.2, 886.1, 940.6, 1057, 1172, 1360, 1437]  # in hundred millions
pet_counts = [8180, 8378, 9378, 9612, 9852, 10197, 10360]  # in ten thousand pets
per_capita_consumption = [102.1, 105.0, 110.4, 112.5, 116.1, 120.4, 122.6]  # example per capita consumption in USD
GDP_growth = [0.03, 0.025, 0.02, 0.02, 0.025, 0.03, 0.02]  # example GDP growth for each year

# Combine the data into a DataFrame
data = pd.DataFrame({
    'Year': years,
    'Pet Count': pet_counts,
    'Per Capita Consumption': per_capita_consumption,
    'GDP Growth': GDP_growth,
    'Market Size': market_sizes
})

# 1. 对GDP增长率做归一化处理
scaler = MinMaxScaler()
data['GDP Growth'] = scaler.fit_transform(data[['GDP Growth']])

# 2. 对消费数据进行对数变换
data['Per Capita Consumption'] = np.log(data['Per Capita Consumption'])

# Define dependent and independent variables
X = data[['Pet Count', 'Per Capita Consumption', 'GDP Growth']]  # independent variables
y = data['Market Size']  # dependent variable (Market Size)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

# Output the results
print("Regression Coefficients:", model.coef_)
print("Intercept:", model.intercept_)
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

# Plot the predictions vs actual values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', label='Predictions')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Ideal Fit')
plt.xlabel('Actual Market Size')
plt.ylabel('Predicted Market Size')
plt.title('Actual vs Predicted Market Size (Test Data)')
plt.legend()
plt.show()
