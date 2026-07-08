# -*- coding: utf-8 -*-
"""
国赛B题: 问题一详细代码 - SPRT序贯检验
"""

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class SPRT:
    """序贯概率比检验"""
    
    def __init__(self, p0, p1, alpha=0.05, beta=0.20):
        """
        p0: 零假设次品率
        p1: 备择假设次品率
        alpha: 显著性水平
        beta: 第二类错误概率
        """
        self.p0 = p0
        self.p1 = p1
        self.alpha = alpha
        self.beta = beta
        self.A = (1 - beta) / alpha  # 拒绝阈值
        self.B = beta / (1 - alpha)  # 接受阈值
    
    def run(self, max_samples=1000):
        """执行SPRT检验"""
        n = 0
        x = 0
        log_likelihood_ratios = []
        decisions = []
        
        while n < max_samples:
            n += 1
            # 模拟抽样
            sample = np.random.random() < self.p1
            x += sample
            
            # 计算对数似然比
            llr = x * np.log(self.p1 / self.p0) + (n - x) * np.log((1 - self.p1) / (1 - self.p0))
            log_likelihood_ratios.append(llr)
            
            # 决策
            if llr > np.log(self.A):
                decisions.append("拒绝零假设")
                return n, x, decisions, log_likelihood_ratios
            elif llr < np.log(self.B):
                decisions.append("接受零假设")
                return n, x, decisions, log_likelihood_ratios
        
        return n, x, ["未决"], log_likelihood_ratios
    
    def visualize(self, log_likelihood_ratios):
        """可视化检验过程"""
        plt.figure(figsize=(10, 6))
        plt.plot(log_likelihood_ratios, 'b-', linewidth=2)
        plt.axhline(y=np.log(self.A), color='r', linestyle='--', label=f'拒绝阈值 A={self.A:.2f}')
        plt.axhline(y=np.log(self.B), color='g', linestyle='--', label=f'接受阈值 B={self.B:.2f}')
        plt.xlabel('样本序号')
        plt.ylabel('对数似然比')
        plt.title('SPRT序贯概率比检验过程')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.savefig('SPRT检验过程.png', dpi=300, bbox_inches='tight')
        plt.show()

def calculate_sample_size(p0, p1, alpha=0.05, beta=0.20):
    """计算固定样本量"""
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(1 - beta)
    
    n = ((z_alpha * np.sqrt(p0 * (1 - p0)) + z_beta * np.sqrt(p1 * (1 - p1))) / (p1 - p0)) ** 2
    
    return int(np.ceil(n))

# 示例运行
if __name__ == "__main__":
    # 情境1：次品率15%
    sprt1 = SPRT(p0=0.10, p1=0.15)
    n1, x1, decision1, llr1 = sprt1.run()
    print(f"情境1（次品率15%）：经过{n1}个样本，{decision1[-1]}")
    sprt1.visualize(llr1)
    
    # 情境2：次品率5%
    sprt2 = SPRT(p0=0.10, p1=0.05)
    n2, x2, decision2, llr2 = sprt2.run()
    print(f"情境2（次品率5%）：经过{n2}个样本，{decision2[-1]}")
    sprt2.visualize(llr2)
    
    # 计算固定样本量
    n_fixed = calculate_sample_size(0.10, 0.15)
    print(f"\n固定样本量检验所需样本数：{n_fixed}")
