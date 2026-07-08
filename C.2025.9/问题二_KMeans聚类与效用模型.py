# -*- coding: utf-8 -*-
"""
国赛C题: 问题二详细代码 - K-Means聚类与期望效用模型
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# K-Means聚类确定BMI分组
def kmeans_bmi_clustering(df, n_clusters=4):
    scaler = StandardScaler()
    bmi_scaled = scaler.fit_transform(df[["孕妇BMI"]])
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["BMI聚类"] = kmeans.fit_predict(bmi_scaled)
    
    # 计算各组统计信息
    cluster_stats = df.groupby("BMI聚类").agg({
        "孕妇BMI": ["mean", "min", "max", "count"],
        "Y染色体浓度": "mean"
    }).round(4)
    
    return df, cluster_stats, kmeans

# 肘部法则确定最优聚类数
def elbow_method(df, max_k=10):
    scaler = StandardScaler()
    bmi_scaled = scaler.fit_transform(df[["孕妇BMI"]])
    
    inertias = []
    K_range = range(2, max_k + 1)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(bmi_scaled)
        inertias.append(kmeans.inertia_)
    
    plt.figure(figsize=(8, 5))
    plt.plot(K_range, inertias, 'bo-')
    plt.xlabel('聚类数K')
    plt.ylabel('惯性值(Inertia)')
    plt.title('肘部法则确定最优聚类数')
    plt.grid(alpha=0.3)
    plt.savefig('肘部法则.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return inertias

# 期望效用模型
class ExpectedUtilityModel:
    def __init__(self, beta=0.7):
        """
        beta: 风险权重系数
        beta > 0.5: 偏向检测成功
        beta < 0.5: 偏向诊断及时
        """
        self.beta = beta
    
    def detection_success_utility(self, reach_time, target_time=12):
        """检测成功期望效用"""
        if reach_time <= target_time:
            return 1.0
        else:
            return np.exp(-0.1 * (reach_time - target_time))
    
    def diagnosis_timeliness_utility(self, reach_time):
        """诊断及时期望效用"""
        if reach_time <= 12:
            return 1.0
        elif reach_time <= 17:
            return 0.9
        elif reach_time <= 28:
            return 0.7
        else:
            return 0.5
    
    def total_utility(self, reach_time):
        """总期望效用"""
        u_success = self.detection_success_utility(reach_time)
        u_timeliness = self.diagnosis_timeliness_utility(reach_time)
        return self.beta * u_success + (1 - self.beta) * u_timeliness
    
    def optimize_reach_time(self, bmi_range, reach_times):
        """优化检测时点"""
        utilities = [self.total_utility(t) for t in reach_times]
        optimal_idx = np.argmax(utilities)
        return reach_times[optimal_idx], utilities[optimal_idx]

# 代码保存完成
