import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# 过去五年的数据
years = [2019, 2020, 2021, 2022, 2023]
production_values = [440.7, 727.3, 1554, 1508, 2793]  # 生产总值 (人民币亿元)
export_values_rmb = [154.1, 9.8, 12.2, 24.7, 39.6]  # 人民币计价的出口值
exchange_rate = 6.9066  # 人民币与美元汇率
export_values = [value / exchange_rate if i == 0 else value for i, value in enumerate(export_values_rmb)]

# GDP增长率和宠物数量假设
cat_dog_population = [11692, 11934, 12271, 12573, 13155]  # 猫狗数量（万只）
gdp_growth = [6.0, 2.2, 8.1, 3.0, 5.5]  # GDP增长率 (%)
global_demand = [50, 70, 90, 110, 130]  # 假设的全球市场需求 (USD Billion)

# 数据整理
data = pd.DataFrame({
    'Cat and Dog Population': cat_dog_population,
    'GDP Growth': gdp_growth,
    'Global Demand': global_demand
})

# 未来假设数据
future_data = pd.DataFrame({
    'Cat and Dog Population': [15000, 15500, 16000],  # 假设猫狗数量
    'GDP Growth': [5.4, 5.6, 5.8],  # 假设GDP增长率
    'Global Demand': [160, 180, 200]  # 假设全球需求
})

# 特征和目标变量
X = data
y_production = production_values
y_export = export_values

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # 标准化特征变量
future_data_scaled = scaler.transform(future_data)  # 标准化未来数据

# 1. 支持向量回归 (SVR)
model_svr_prod = SVR(kernel='rbf')
model_svr_prod.fit(X_scaled, y_production)
predicted_production_svr = model_svr_prod.predict(future_data_scaled)

model_svr_exp = SVR(kernel='rbf')
model_svr_exp.fit(X_scaled, y_export)
predicted_export_svr = model_svr_exp.predict(future_data_scaled)

# 2. 随机森林回归 (Random Forest)
model_rf_prod = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf_prod.fit(X, y_production)
predicted_production_rf = model_rf_prod.predict(future_data)

model_rf_exp = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf_exp.fit(X, y_export)
predicted_export_rf = model_rf_exp.predict(future_data)

# 可视化
plt.figure(figsize=(14, 6))

# 生产总值预测对比
plt.subplot(1, 2, 1)
plt.plot(years, production_values, label="Historical Production Value", marker='o', color='blue')
plt.plot([2024, 2025, 2026], predicted_production_svr, label="SVR Predicted Production", linestyle='--', marker='x', color='red')
plt.plot([2024, 2025, 2026], predicted_production_rf, label="RF Predicted Production", linestyle='-.', marker='s', color='purple')
plt.xlabel("Year")
plt.ylabel("Production Value (Billion RMB)")
plt.title("Production Value Prediction Comparison")
plt.legend()

# 出口总值预测对比
plt.subplot(1, 2, 2)
plt.plot(years, export_values, label="Historical Export Value", marker='o', color='green')
plt.plot([2024, 2025, 2026], predicted_export_svr, label="SVR Predicted Export", linestyle='--', marker='x', color='orange')
plt.plot([2024, 2025, 2026], predicted_export_rf, label="RF Predicted Export", linestyle='-.', marker='s', color='purple')
plt.xlabel("Year")
plt.ylabel("Export Value (Billion USD)")
plt.title("Export Value Prediction Comparison")
plt.legend()

plt.tight_layout()
plt.show()

# 误差计算
mse_svr_prod = mean_squared_error(y_production, model_svr_prod.predict(X_scaled))
mse_rf_prod = mean_squared_error(y_production, model_rf_prod.predict(X))

mse_svr_exp = mean_squared_error(y_export, model_svr_exp.predict(X_scaled))
mse_rf_exp = mean_squared_error(y_export, model_rf_exp.predict(X))

print(f"SVR Production MSE: {mse_svr_prod:.2f}")
print(f"RF Production MSE: {mse_rf_prod:.2f}")
print(f"SVR Export MSE: {mse_svr_exp:.2f}")
print(f"RF Export MSE: {mse_rf_exp:.2f}")
