import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === 数据输入 ===
years = np.array([2024, 2025, 2026])
pet_count = np.array([10400, 10650, 10900])  # 宠物数量预测
per_capita = np.array([123.0, 125.0, 127.0])  # 人均消费预测
base_market_size = pet_count * per_capita / 10000  # 初始市场规模（百亿美元）

# === 模拟参数 ===
tariff_changes = [0.1, 0.2, 0.3]  # 假设关税变化幅度
exchange_rate_changes = [-0.03, 0.0, 0.05]  # 汇率变化幅度
random_noise_std = 0.1  # 随机波动标准差

# 供需关系假设函数（非线性调整 + 随机扰动）
def demand_function(base_demand, tariff, beta, noise=0):
    return base_demand * np.exp(-beta * tariff) + noise

def supply_function(base_supply, tariff, exchange_rate, alpha, gamma, noise=0):
    return base_supply * (1 + alpha * tariff + gamma * exchange_rate) + noise

# 模拟情景
results = []

for scenario in ["Optimistic", "Baseline", "Pessimistic"]:
    beta = 0.15 if scenario == "Optimistic" else 0.3 if scenario == "Pessimistic" else 0.2
    alpha, gamma = (0.3, -0.2) if scenario == "Optimistic" else (0.4, -0.3) if scenario == "Pessimistic" else (0.35, -0.25)
    
    for year, base_size in zip(years, base_market_size):
        for tariff in tariff_changes:
            for exchange_rate in exchange_rate_changes:
                noise_demand = np.random.normal(0, random_noise_std * base_size)
                noise_supply = np.random.normal(0, random_noise_std * base_size)
                
                adjusted_demand = demand_function(base_size, tariff, beta, noise=noise_demand)
                adjusted_supply = supply_function(base_size, tariff, exchange_rate, alpha, gamma, noise=noise_supply)
                market_size = min(adjusted_demand, adjusted_supply)
                
                results.append({
                    'Year': year,
                    'Scenario': scenario,
                    'Tariff Change (%)': tariff * 100,
                    'Exchange Rate Change (%)': exchange_rate * 100,
                    'Market Size (Billion USD)': market_size
                })

# 转为 DataFrame
df_results = pd.DataFrame(results)

# === 绘图 ===
plt.figure(figsize=(12, 8))
for scenario in ["Optimistic", "Baseline", "Pessimistic"]:
    subset = df_results[df_results['Scenario'] == scenario]
    avg_market_size = subset.groupby('Year')['Market Size (Billion USD)'].mean()
    plt.plot(years, avg_market_size, label=f"{scenario} Scenario")

plt.title("Market Size Prediction under Different Scenarios", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Market Size (Billion USD)", fontsize=12)
plt.legend(title="Scenario", fontsize=10)
plt.grid()
plt.show()
