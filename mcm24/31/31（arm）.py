import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# 数据：过去五年的生产总值和出口总值
years = [2019, 2020, 2021, 2022, 2023]
production_values = [440.7, 727.3, 1554, 1508, 2793]  # 生产总值 (人民币亿元)
export_values_rmb = [154.1, 9.8, 12.2, 24.7, 39.6]  # 人民币计价的出口值
exchange_rate = 6.9066  # 人民币与美元汇率
export_values = [value / exchange_rate if i == 0 else value for i, value in enumerate(export_values_rmb)]

# 创建时间序列数据
production_series = pd.Series(production_values, index=years)
export_series = pd.Series(export_values, index=years)

# 设置未来预测年份
future_years = [2024, 2025, 2026]

# 1. 对生产总值进行时间序列建模和预测
model_prod = ARIMA(production_series, order=(1, 1, 2))  # 参数 (p, d, q)：可调整
fitted_prod = model_prod.fit()
forecast_prod = fitted_prod.forecast(steps=3)  # 预测未来3年

# 2. 对出口总值进行时间序列建模和预测
model_exp = ARIMA(export_series, order=(1, 1, 2))  # 参数 (p, d, q)：可调整
fitted_exp = model_exp.fit()
forecast_exp = fitted_exp.forecast(steps=3)  # 预测未来3年

# 可视化结果
plt.figure(figsize=(14, 6))

# 生产总值预测图
plt.subplot(1, 2, 1)
plt.plot(years, production_values, label="Historical Production Value", marker='o', color='blue')
plt.plot(future_years, forecast_prod, label="Forecasted Production Value", linestyle='--', marker='x', color='red')
plt.xlabel("Year")
plt.ylabel("Production Value (Billion RMB)")
plt.title("Production Value Prediction (ARIMA)")
plt.legend()

# 出口总值预测图
plt.subplot(1, 2, 2)
plt.plot(years, export_values, label="Historical Export Value", marker='o', color='green')
plt.plot(future_years, forecast_exp, label="Forecasted Export Value", linestyle='--', marker='x', color='orange')
plt.xlabel("Year")
plt.ylabel("Export Value (Billion USD)")
plt.title("Export Value Prediction (ARIMA)")
plt.legend()

plt.tight_layout()
plt.show()

# 打印预测值
print("Forecasted Production Values (Billion RMB):", forecast_prod.tolist())
print("Forecasted Export Values (Billion USD):", forecast_exp.tolist())
