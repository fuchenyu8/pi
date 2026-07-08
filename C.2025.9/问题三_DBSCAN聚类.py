# -*- coding: utf-8 -*-
"""
国赛C题: 问题三详细代码 - DBSCAN聚类
"""

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def determine_eps(X, k=5):
    """通过K近邻法确定eps参数"""
    neigh = NearestNeighbors(n_neighbors=k)
    neigh.fit(X)
    distances, indices = neigh.kneighbors(X)
    
    # 取第k个距离并排序
    k_distances = np.sort(distances[:, k-1])
    
    plt.figure(figsize=(10, 5))
    plt.plot(k_distances)
    plt.xlabel('样本点')
    plt.ylabel(f'第{k}近邻距离')
    plt.title('K近邻距离图（确定eps）')
    plt.grid(alpha=0.3)
    plt.savefig('K近邻距离图.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return k_distances

def dbscan_clustering(df, eps=0.5, min_samples=5):
    """DBSCAN聚类"""
    scaler = StandardScaler()
    bmi_scaled = scaler.fit_transform(df[["孕妇BMI"]])
    
    # 确定eps
    k_distances = determine_eps(bmi_scaled, k=min_samples)
    
    # 执行DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    df["DBSCAN聚类"] = dbscan.fit_predict(bmi_scaled)
    
    # 统计结果
    n_clusters = len(set(df["DBSCAN聚类"])) - (1 if -1 in df["DBSCAN聚类"].values else 0)
    n_noise = (df["DBSCAN聚类"] == -1).sum()
    
    print(f"聚类数量: {n_clusters}")
    print(f"噪声点数量: {n_noise}")
    
    # 各聚类统计
    cluster_stats = df.groupby("DBSCAN聚类").agg({
        "孕妇BMI": ["mean", "min", "max", "count"],
        "Y染色体浓度": "mean"
    }).round(4)
    
    return df, cluster_stats

# 代码保存完成
