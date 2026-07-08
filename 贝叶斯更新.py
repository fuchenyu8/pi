# -*- coding: utf-8 -*-
"""
国赛B题: 问题四详细代码 - 贝叶斯更新
"""

import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class BayesianUpdater:
    """贝叶斯参数更新器"""
    
    def __init__(self, prior_alpha=2, prior_beta=2):
        """
        先验分布: Beta(prior_alpha, prior_beta)
        """
        self.prior_alpha = prior_alpha
        self.prior_beta = prior_beta
        self.posterior_alpha = prior_alpha
        self.posterior_beta = prior_beta
    
    def update(self, successes, trials):
        """贝叶斯更新"""
        self.posterior_alpha = self.prior_alpha + successes
        self.posterior_beta = self.prior_beta + trials - successes
        
        return self.get_posterior_mean()
    
    def get_posterior_mean(self):
        """获取后验均值"""
        return self.posterior_alpha / (self.posterior_alpha + self.posterior_beta)
    
    def get_posterior_ci(self, confidence=0.95):
        """获取后验置信区间"""
        alpha = (1 - confidence) / 2
        lower = beta.ppf(alpha, self.posterior_alpha, self.posterior_beta)
        upper = beta.ppf(1 - alpha, self.posterior_alpha, self.posterior_beta)
        return lower, upper
    
    def visualize(self, observations=None):
        """可视化先验和后验分布"""
        x = np.linspace(0, 1, 1000)
        
        prior_dist = beta.pdf(x, self.prior_alpha, self.prior_beta)
        posterior_dist = beta.pdf(x, self.posterior_alpha, self.posterior_beta)
        
        plt.figure(figsize=(10, 6))
        plt.plot(x, prior_dist, 'b--', linewidth=2, label='先验分布')
        plt.plot(x, posterior_dist, 'r-', linewidth=2, label='后验分布')
        
        if observations:
            plt.axvline(x=observations[0]/observations[1], color='g', linestyle=':', 
                       label=f'观测次品率: {observations[0]/observations[1]:.2%}')
        
        plt.xlabel('次品率')
        plt.ylabel('概率密度')
        plt.title('贝叶斯更新：先验与后验分布')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig('贝叶斯更新.png', dpi=300, bbox_inches='tight')
        plt.show()

# 示例：多次更新
if __name__ == "__main__":
    updater = BayesianUpdater(prior_alpha=2, prior_beta=2)
    
    print("=== 贝叶斯更新演示 ===")
    print(f"先验: Beta({updater.prior_alpha}, {updater.prior_beta})")
    print(f"先验均值: {updater.get_posterior_mean():.4f}")
    
    # 第一次观测：30个样本，3个次品
    mean1 = updater.update(successes=3, trials=30)
    print(f"\n第一次观测后（3/30）：后验均值 = {mean1:.4f}")
    
    # 第二次观测：50个样本，5个次品
    mean2 = updater.update(successes=5, trials=50)
    print(f"第二次观测后（5/50）：后验均值 = {mean2:.4f}")
    
    # 可视化
    updater.visualize()
