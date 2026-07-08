# -*- coding: utf-8 -*-
"""
国赛C题: 问题四详细代码 - XGBoost分类模型
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.utils import resample
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.mean_minus'] = False

def build_features(df):
    """构建特征"""
    features = ["孕妇BMI", "孕周_小数", "年龄", "身高", "体重"]
    
    # BMI衍生特征
    df["BMI_平方"] = df["孕妇BMI"] ** 2
    df["BMI_孕周交互"] = df["孕妇BMI"] * df["孕周_小数"]
    
    features.extend(["BMI_平方", "BMI_孕周交互"])
    
    return df, features

def handle_imbalanced_data(X, y, method='oversample'):
    """处理不平衡数据"""
    X_normal = X[y == 0]
    X_abnormal = X[y == 1]
    
    if method == 'oversample':
        X_abnormal_up = resample(X_abnormal, replace=True, n_samples=len(X_normal), random_state=42)
        X_balanced = pd.concat([X_normal, X_abnormal_up])
        y_balanced = np.array([0]*len(X_normal) + [1]*len(X_abnormal_up))
    elif method == 'class_weight':
        return X, y, 'balanced'
    
    return X_balanced, y_balanced, None

def train_and_evaluate(X_train, X_test, y_train, y_test):
    """训练和评估模型"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 逻辑回归模型
    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]
    
    print("分类报告：")
    print(classification_report(y_test, y_pred))
    
    # ROC曲线
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'ROC曲线 (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.title('ROC曲线')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('ROC曲线.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return model, roc_auc

# 代码保存完成
