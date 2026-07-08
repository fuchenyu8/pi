import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === 灵敏度分析 ===
# 参数变化范围
tariff_range = np.linspace(0.05, 0.3, 10)  # 关税变化范围
exchange_rate_range = np.linspace(-0.05, 0.05, 10)  # 汇率变化范围
substitution_rate_range = np.linspace(0.3, 0.7, 10)  # 国内替代率范围

# 初始值
base_size = 120  # 初始市场规模 (百亿美元)
beta = 0.2  # 初始需求弹性
alpha = 0.25  # 关税对供给影响
gamma = -0.15  # 汇率对供给影响

# 敏感性分析结果存储
sensitivity_results = []

for tariff in tariff_range:
    for exchange_rate in exchange_rate_range:
        for substitution_rate in substitution_rate_range:
            # 调整后的市场规模
            adjusted_demand = base_size * np.exp(-beta * tariff)
            international_supply = base_size * (1 + alpha * tariff + gamma * exchange_rate)
            domestic_supply = substitution_rate * (base_size - international_supply)
            adjusted_supply = international_supply + domestic_supply
            
            # 最终市场规模
            market_size = min(adjusted_demand, adjusted_supply)
            sensitivity_results.append({
                'Tariff': tariff,
                'Exchange Rate': exchange_rate,
                'Substitution Rate': substitution_rate,
                'Market Size': market_size
            })

# 转为 DataFrame
df_sensitivity = pd.DataFrame(sensitivity_results)

# 绘制热力图（灵敏度分析）
import seaborn as sns

plt.figure(figsize=(10, 8))
heatmap_data = df_sensitivity.pivot_table(index='Tariff', columns='Exchange Rate', values='Market Size')
sns.heatmap(heatmap_data, cmap="coolwarm", annot=False)
plt.title("Market Size Sensitivity to Tariff and Exchange Rate", fontsize=14)
plt.xlabel("Exchange Rate Change")
plt.ylabel("Tariff Change")
plt.show()

# === 鲁棒性分析 ===
# 扰动模拟
np.random.seed(42)
noise_std = [0.01, 0.05, 0.1]  # 噪声标准差范围
robustness_results = []

for std in noise_std:
    for _ in range(100):  # 模拟100次
        noise_demand = np.random.normal(0, std * base_size)
        noise_supply = np.random.normal(0, std * base_size)
        
        adjusted_demand = base_size * np.exp(-beta * tariff_range.mean()) + noise_demand
        adjusted_supply = base_size * (1 + alpha * tariff_range.mean() + gamma * exchange_rate_range.mean()) + noise_supply
        
        market_size = min(adjusted_demand, adjusted_supply)
        robustness_results.append({
            'Noise Std': std,
            'Market Size': market_size
        })

# 转为 DataFrame
df_robustness = pd.DataFrame(robustness_results)

# 绘制箱线图（鲁棒性分析）
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_robustness, x='Noise Std', y='Market Size', palette="Set3")
plt.title("Robustness Analysis: Market Size Under Different Noise Levels", fontsize=14)
plt.xlabel("Noise Standard Deviation")
plt.ylabel("Market Size (Billion USD)")
plt.show()
