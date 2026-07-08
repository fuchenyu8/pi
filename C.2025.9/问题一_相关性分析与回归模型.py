# -*- coding: utf-8 -*-
"""
国赛C题: NIPT检测的时点优化与胎儿染色体异常判定的研究
代码文件
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 问题一代码 ====================

# 读取数据
df = pd.read_excel("附件.xlsx", sheet_name="男胎检测数据")
df_male = df[df["Y染色体浓度"].notna()].copy()

# 孕周转换函数
def convert_gestational_week(week_str):
    if pd.isna(week_str):
        return np.nan
    week_str = str(week_str).strip().lower()
    if "w+" in week_str:
        w_part, d_part = week_str.split("w+")
        w_part = ''.join(filter(str.isdigit, w_part))
        d_part = ''.join(filter(str.isdigit, d_part))
        if w_part and d_part:
            return int(w_part) + int(d_part)/7
        else:
            return np.nan
    elif "w" in week_str:
        w_part = ''.join(filter(str.isdigit, week_str.replace("w", "")))
        if w_part:
            return int(w_part)
        else:
            return np.nan
    else:
        try:
            return float(''.join(filter(lambda x: x.isdigit() or x == '.', week_str)))
        except:
            return np.nan

df_male["孕周_小数"] = df_male["检测孕周"].apply(convert_gestational_week)

# 清洗数据
df_clean = df_male[
    (df_male["孕妇BMI"] >= 18) & (df_male["孕妇BMI"] <= 50) &
    (df_male["孕周_小数"].notna())
].copy()

X_week = df_clean["孕周_小数"].values.reshape(-1, 1)
X_bmi = df_clean["孕妇BMI"].values.reshape(-1, 1)
X_combined = df_clean[["孕周_小数", "孕妇BMI"]].values
y = df_clean["Y染色体浓度"].values

print(f"有效样本数：{len(df_clean)}")
print(f"孕周范围：{df_clean['孕周_小数'].min():.2f}~{df_clean['孕周_小数'].max():.2f}")
print(f"BMI范围：{df_clean['孕妇BMI'].min():.2f}~{df_clean['孕妇BMI'].max():.2f}")

# Spearman相关分析
print("\n=== 相关性分析结果（Spearman等级相关）===")
corr_week_spear, p_week_spear = stats.spearmanr(df_clean["孕周_小数"], y)
print(f"Y染色体浓度与孕周的Spearman相关系数：{corr_week_spear:.4f}，P值：{p_week_spear:.6f}")
corr_bmi_spear, p_bmi_spear = stats.spearmanr(df_clean["孕妇BMI"], y)
print(f"Y染色体浓度与BMI的Spearman相关系数：{corr_bmi_spear:.4f}，P值：{p_bmi_spear:.6f}")

# 相关性可视化
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.scatter(df_clean["孕周_小数"], y, alpha=0.6, s=30)
ax1.set_xlabel("孕周（周）")
ax1.set_ylabel("Y染色体浓度")
ax1.set_title(f"孕周与Y染色体浓度关系\n（Spearman r={corr_week_spear:.4f}，p={p_week_spear:.6f}）")
ax1.grid(alpha=0.3)
ax2.scatter(df_clean["孕妇BMI"], y, alpha=0.6, s=30, color="orange")
ax2.set_xlabel("BMI")
ax2.set_ylabel("Y染色体浓度")
ax2.set_title(f"BMI与Y染色体浓度关系\n（Spearman r={corr_bmi_spear:.4f}，p={p_bmi_spear:.6f}）")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("相关性分析_Spearman.png", dpi=300, bbox_inches="tight")
plt.close()

# 回归模型
print("\n=== 回归模型结果 ===")
model1 = LinearRegression()
model1.fit(X_week, y)
y_pred1 = model1.predict(X_week)
r2_1 = r2_score(y, y_pred1)
X_week_sm = sm.add_constant(X_week)
model1_sm = sm.OLS(y, X_week_sm).fit()
print("\n【模型1：Y浓度 = β0 + β1×孕周】")
print(f"回归方程：Y浓度 = {model1.intercept_:.6f} + {model1.coef_[0]:.6f}×孕周")
print(f"R²：{r2_1:.4f}")

model2 = LinearRegression()
model2.fit(X_bmi, y)
y_pred2 = model2.predict(X_bmi)
r2_2 = r2_score(y, y_pred2)
print("\n【模型2：Y浓度 = β0 + β1×BMI】")
print(f"回归方程：Y浓度 = {model2.intercept_:.6f} + {model2.coef_[0]:.6f}×BMI")
print(f"R²：{r2_2:.4f}")

model3 = LinearRegression()
model3.fit(X_combined, y)
y_pred3 = model3.predict(X_combined)
r2_3 = r2_score(y, y_pred3)
X_combined_sm = sm.add_constant(X_combined)
model3_sm = sm.OLS(y, X_combined_sm).fit()
print("\n【模型3：Y浓度 = β0 + β1×孕周 + β2×BMI】")
print(f"回归方程：Y浓度 = {model3.intercept_:.6f} + {model3.coef_[0]:.6f}×孕周 + {model3.coef_[1]:.6f}×BMI")
print(f"R²：{r2_3:.4f}，调整后R²：{model3_sm.rsquared_adj:.4f}")

# 混合效应模型
print("\n=== 混合效应模型结果 ===")
group_var = "孕妇代码"
model_me1 = smf.mixedlm(
    "Y染色体浓度~ 孕周_小数 + 孕妇BMI",
    data=df_clean,
    groups=df_clean[group_var]
)
result_me1 = model_me1.fit(reml=True)
print("\n【混合效应模型：随机截距模型】")
print(f"随机效应方差：{result_me1.cov_re.iloc[0,0]:.6f}")

model_me2 = smf.mixedlm(
    "Y染色体浓度~ 孕周_小数 + 孕妇BMI",
    data=df_clean,
    groups=df_clean[group_var],
    re_formula="~孕周_小数"
)
result_me2 = model_me2.fit(reml=True)
print("\n【混合效应模型：随机截距+随机斜率模型】")
print(result_me2.summary().tables[1])

# 似然比检验
from scipy.stats import chi2
lr_stat = 2 * (result_me2.llf - result_me1.llf)
df_diff = result_me2.df_re - result_me1.df_re
p_value = chi2.sf(lr_stat, df_diff)
print(f"\n似然比统计量：{lr_stat:.4f}，P值：{p_value:.6f}")

# ==================== 问题二代码 ====================

# K-Means聚类
scaler = StandardScaler()
bmi_scaled = scaler.fit_transform(df_clean[["孕妇BMI"]])
kmeans = KMeans(n_clusters=4, random_state=42)
df_clean["BMI聚类"] = kmeans.fit_predict(bmi_scaled)

# 计算各组达标时点
def calc_reach_time(group):
    y_values = group["Y染色体浓度"].values
    threshold = 0.04
    for i, val in enumerate(y_values):
        if val >= threshold:
            return group.iloc[i]["孕周_小数"]
    return group["孕周_小数"].max()

cluster_results = df_clean.groupby("BMI聚类").apply(calc_reach_time).reset_index()
cluster_results.columns = ["聚类", "达标时点"]

print("\n=== 问题二：K-Means聚类结果 ===")
print(cluster_results)

# 期望效用模型
def expected_utility(reach_time, beta=0.7):
    if reach_time <= 12:
        return 1.0
    elif reach_time <= 17:
        return 0.9
    elif reach_time <= 28:
        return 0.7
    else:
        return 0.5

cluster_results["期望效用"] = cluster_results["达标时点"].apply(expected_utility)
print("\n各组期望效用：")
print(cluster_results)

# ==================== 问题三代码 ====================

# DBSCAN聚类
dbscan = DBSCAN(eps=0.5, min_samples=5)
df_clean["DBSCAN聚类"] = dbscan.fit_predict(bmi_scaled)

print("\n=== 问题三：DBSCAN聚类结果 ===")
print(f"聚类数量：{len(set(df_clean['DBSCAN聚类'])) - (1 if -1 in df_clean['DBSCAN聚类'].values else 0)}")
print(f"噪声点数量：{(df_clean['DBSCAN聚类'] == -1).sum()}")

# ==================== 问题四代码 ====================

# XGBoost模型（使用逻辑回归代替演示）
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import resample

# 特征构建
features = ["孕妇BMI", "孕周_小数", "年龄", "身高", "体重"]
X = df_clean[features].fillna(df_clean[features].mean())
y_binary = (df_clean["Y染色体浓度"] < 0.04).astype(int)  # 异常标签

# 数据平衡（ADASYN替代：过采样少数类）
X_normal = X[y_binary == 0]
X_abnormal = X[y_binary == 1]
X_abnormal_upsampled = resample(X_abnormal, replace=True, n_samples=len(X_normal), random_state=42)
X_balanced = pd.concat([X_normal, X_abnormal_upsampled])
y_balanced = np.array([0]*len(X_normal) + [1]*len(X_abnormal_upsampled))

# 训练逻辑回归模型
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

print("\n=== 问题四：分类模型结果 ===")
print("分类报告：")
print(classification_report(y_test, y_pred))
print("混淆矩阵：")
print(confusion_matrix(y_test, y_pred))
