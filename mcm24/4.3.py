import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === 数据输入 ===
years = np.array([2024, 2025, 2026])
base_demand = np.array([123, 130, 137])  # 基准需求（亿美元）
base_supply = base_demand * 0.95  # 初始供需平衡

# 模拟政策参数
tariff_changes = np.array([0.10, 0.15, 0.20])  # 关税变化（假设10%-20%）
exchange_rate_changes = np.array([0.02, 0.03, 0.04])  # 汇率变化（2%-4%）
price_elasticity = 0.8  # 需求价格弹性
domestic_substitution_rate = 0.5  # 起始国内替代率
substitution_growth = 0.05  # 替代率年增长

# 结果存储
results = []

# === 动态模拟计算 ===
for i, year in enumerate(years):
    # 价格调整
    delta_price = tariff_changes[i] + exchange_rate_changes[i]
    adjusted_demand = base_demand[i] * (1 - price_elasticity * delta_price)

    # 国内替代率动态增长
    rho_domestic = min(1.0, domestic_substitution_rate + substitution_growth * i)
    adjusted_supply = base_supply[i] * (1 - rho_domestic)

    # 供需平衡
    final_market_size = min(adjusted_demand, adjusted_supply)
    results.append({
        "Year": year,
        "Adjusted Demand (Billion USD)": adjusted_demand,
        "Adjusted Supply (Billion USD)": adjusted_supply,
        "Final Market Size (Billion USD)": final_market_size
    })

# 转换为 DataFrame
df_results = pd.DataFrame(results)

# === 绘图 ===
plt.figure(figsize=(10, 6))
x = np.arange(len(years))

# 绘制调整后的需求和供给
plt.bar(x - 0.2, df_results["Adjusted Demand (Billion USD)"], width=0.4, label="Adjusted Demand", color='skyblue')
plt.bar(x + 0.2, df_results["Adjusted Supply (Billion USD)"], width=0.4, label="Adjusted Supply", color='orange')

# 标注最终市场规模
for i, size in enumerate(df_results["Final Market Size (Billion USD)"]):
    plt.text(i, size + 1, f"{size:.1f}", ha='center', va='bottom', fontsize=10, color='black')

# 美化图表
plt.xticks(x, labels=years)
plt.title("Impact of Foreign Policies on China's Pet Food Market (2024-2026)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Market Size (Billion USD)", fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# 展示图表
plt.show()

# 输出结果表格
print(df_results)
