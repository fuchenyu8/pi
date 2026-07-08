# -*- coding: utf-8 -*-
"""
国赛B题: 企业生产决策优化
代码文件
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm, binom, chi2
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==================== 问题一：抽样检测方案 ====================

def sprt_detection(p0, p1, alpha=0.05, beta=0.20):
    """SPRT序贯概率比检验"""
    A = (1 - beta) / alpha
    B = beta / (1 - alpha)
    
    n = 0
    x = 0
    decisions = []
    
    while True:
        n += 1
        sample = np.random.random() < p1
        x += sample
        
        likelihood_ratio = (p1 / p0) ** x * ((1 - p1) / (1 - p0)) ** (n - x)
        
        if likelihood_ratio > A:
            decisions.append((n, "拒绝零假设"))
            break
        elif likelihood_ratio < B:
            decisions.append((n, "接受零假设"))
            break
    
    return n, decisions[-1][1]

# 情境1：次品率15%
print("=== 情境1 - SPRT检测（次品率15%）===")
n1, decision1 = sprt_detection(0.10, 0.15)
print(f"经过 {n1} 个样本后: {decision1}")

# 情境2：次品率5%
print("\n=== 情境2 - SPRT检测（次品率5%）===")
n2, decision2 = sprt_detection(0.10, 0.05)
print(f"经过 {n2} 个样本后: {decision2}")

# 样本量计算
def calculate_sample_size(p0, p1, alpha=0.05, beta=0.20):
    """计算所需样本量"""
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(1 - beta)
    n = ((z_alpha * np.sqrt(p0 * (1 - p0)) + z_beta * np.sqrt(p1 * (1 - p1))) / (p1 - p0)) ** 2
    return int(np.ceil(n))

n_required = calculate_sample_size(0.10, 0.15)
print(f"\n所需样本量：{n_required}")

# ==================== 问题二：生产决策优化 ====================

def calculate_expected_profit(params, d1, d2, df, dd):
    """计算给定决策下的期望利润"""
    # 计算实际进入装配的零件合格率
    p_good1 = 1.0 if d1 else (1 - params['defect_rate_part1'])
    p_good2 = 1.0 if d2 else (1 - params['defect_rate_part2'])
    
    # q = P(零件1合格) * P(零件2合格) * P(装配过程合格)
    q = p_good1 * p_good2 * (1 - params['final_product_defect_rate'])
    
    # 计算单位成品的基础成本
    part1_purchase = params['purchase_price_part1'] / (1 - params['defect_rate_part1']) if d1 else params['purchase_price_part1']
    part2_purchase = params['purchase_price_part2'] / (1 - params['defect_rate_part2']) if d2 else params['purchase_price_part2']
    part1_inspect = params['inspection_cost_part1'] / (1 - params['defect_rate_part1']) if d1 else 0
    part2_inspect = params['inspection_cost_part2'] / (1 - params['defect_rate_part2']) if d2 else 0
    final_inspect = params['final_product_assembly_cost'] if df else 0
    assembly_cost = params['assembly_cost']
    
    C_unit = part1_purchase + part2_purchase + part1_inspect + part2_inspect + assembly_cost + final_inspect
    
    recycle_value = (params['purchase_price_part1'] + params['purchase_price_part2']) if dd else 0
    disassembly_cost = params['disassembly_cost'] if dd else 0
    
    # V（生产一个最终被接受产品的总成本）
    if df == 1:
        V = (C_unit + (1 - q) * (disassembly_cost - recycle_value)) / q
    else:
        V = (C_unit + (1 - q) * (params['return_loss'] + disassembly_cost - recycle_value)) / q
    
    expected_profit = params['market_price'] - V
    return expected_profit, q, V, recycle_value

def find_optimal_decision(params):
    """寻找最优决策"""
    best_profit = -float('inf')
    best_decision = (0, 0, 0, 0)
    best_q = 0
    best_V = 0
    best_recycle = 0
    
    for d1 in [0, 1]:
        for d2 in [0, 1]:
            for df in [0, 1]:
                for dd in [0, 1]:
                    profit, q, V, recycle = calculate_expected_profit(params, d1, d2, df, dd)
                    if profit > best_profit:
                        best_profit = profit
                        best_decision = (d1, d2, df, dd)
                        best_q = q
                        best_V = V
                        best_recycle = recycle
    
    return best_decision, best_profit, best_q, best_V, best_recycle

def get_decision_description(decision):
    """获取决策描述"""
    d1, d2, df, dd = decision
    desc = []
    desc.append("检测零件1" if d1 else "不检测零件1")
    desc.append("检测零件2" if d2 else "不检测零件2")
    desc.append("检测成品" if df else "不检测成品")
    desc.append("拆解不合格品" if dd else "不拆解不合格品")
    return ", ".join(desc)

# 六种情况的参数
situations = [
    {  # 情况1
        'defect_rate_part1': 0.1, 'purchase_price_part1': 4, 'inspection_cost_part1': 2,
        'defect_rate_part2': 0.1, 'purchase_price_part2': 18, 'inspection_cost_part2': 3,
        'assembly_cost': 6, 'final_product_defect_rate': 0.1,
        'final_product_assembly_cost': 3, 'market_price': 56,
        'return_loss': 6, 'disassembly_cost': 5
    },
    {  # 情况2
        'defect_rate_part1': 0.2, 'purchase_price_part1': 4, 'inspection_cost_part1': 2,
        'defect_rate_part2': 0.2, 'purchase_price_part2': 18, 'inspection_cost_part2': 3,
        'assembly_cost': 6, 'final_product_defect_rate': 0.2,
        'final_product_assembly_cost': 3, 'market_price': 56,
        'return_loss': 6, 'disassembly_cost': 5
    },
    {  # 情况3
        'defect_rate_part1': 0.1, 'purchase_price_part1': 4, 'inspection_cost_part1': 2,
        'defect_rate_part2': 0.1, 'purchase_price_part2': 18, 'inspection_cost_part2': 3,
        'assembly_cost': 6, 'final_product_defect_rate': 0.1,
        'final_product_assembly_cost': 3, 'market_price': 56,
        'return_loss': 30, 'disassembly_cost': 5
    },
    {  # 情况4
        'defect_rate_part1': 0.2, 'purchase_price_part1': 4, 'inspection_cost_part1': 1,
        'defect_rate_part2': 0.2, 'purchase_price_part2': 18, 'inspection_cost_part2': 1,
        'assembly_cost': 6, 'final_product_defect_rate': 0.2,
        'final_product_assembly_cost': 2, 'market_price': 56,
        'return_loss': 30, 'disassembly_cost': 5
    },
    {  # 情况5
        'defect_rate_part1': 0.1, 'purchase_price_part1': 4, 'inspection_cost_part1': 8,
        'defect_rate_part2': 0.2, 'purchase_price_part2': 18, 'inspection_cost_part2': 1,
        'assembly_cost': 6, 'final_product_defect_rate': 0.1,
        'final_product_assembly_cost': 2, 'market_price': 56,
        'return_loss': 10, 'disassembly_cost': 5
    },
    {  # 情况6
        'defect_rate_part1': 0.05, 'purchase_price_part1': 4, 'inspection_cost_part1': 2,
        'defect_rate_part2': 0.05, 'purchase_price_part2': 18, 'inspection_cost_part2': 3,
        'assembly_cost': 6, 'final_product_defect_rate': 0.05,
        'final_product_assembly_cost': 3, 'market_price': 56,
        'return_loss': 10, 'disassembly_cost': 40
    }
]

print("\n=== 问题二：六种情况决策结果 ===")
results = []
for i, params in enumerate(situations, 1):
    decision, profit, q, V, recycle = find_optimal_decision(params)
    decision_desc = get_decision_description(decision)
    results.append({
        'situation': i,
        'decision': decision_desc,
        'profit': profit,
        'quality': q * 100,
        'cost': V,
        'recycle': recycle
    })
    print(f"\n情况{i}: {decision_desc}")
    print(f"  期望利润: {profit:.2f}, 合格率: {q*100:.1f}%, 回收价值: {recycle:.2f}")

# ==================== 问题三：多层决策优化 ====================

def calculate_multilayer_profit(params, decisions):
    """计算多层决策的期望利润"""
    d1, d2, d3, d4, d5, d6, d7, d8 = decisions
    
    # 零配件合格率
    p1 = 1 - params['part1_defect'] if d1 else 1
    p2 = 1 - params['part2_defect'] if d2 else 1
    p3 = 1 - params['part3_defect'] if d3 else 1
    p4 = 1 - params['part4_defect'] if d4 else 1
    p5 = 1 - params['part5_defect'] if d5 else 1
    p6 = 1 - params['part6_defect'] if d6 else 1
    
    # 半成品合格率
    semi1 = p1 * p2 * p3 * (1 - params['semi1_defect'])
    semi2 = p4 * p5 * p6 * (1 - params['semi2_defect'])
    
    # 成品合格率
    final_q = semi1 * semi2 * (1 - params['final_defect'])
    
    # 成本计算
    total_cost = 0
    for i, (p_defect, p_price, i_cost) in enumerate([
        (params['part1_defect'], params['part1_price'], params['part1_inspect']),
        (params['part2_defect'], params['part2_price'], params['part2_inspect']),
        (params['part3_defect'], params['part3_price'], params['part3_inspect']),
        (params['part4_defect'], params['part4_price'], params['part4_inspect']),
        (params['part5_defect'], params['part5_price'], params['part5_inspect']),
        (params['part6_defect'], params['part6_price'], params['part6_inspect'])
    ]):
        if decisions[i]:
            total_cost += p_price / (1 - p_defect) + i_cost / (1 - p_defect)
        else:
            total_cost += p_price
    
    total_cost += params['assembly_cost']
    
    if d7:  # 检测成品
        total_cost += params['final_inspect']
    
    # 期望利润
    revenue = params['market_price'] * final_q
    loss = (1 - final_q) * (params['return_loss'] + (params['disassembly_cost'] if d8 else 0))
    
    profit = revenue - total_cost - loss
    return profit

# ==================== 问题四：贝叶斯更新 ====================

def bayesian_update(prior_alpha, prior_beta, successes, trials):
    """贝叶斯参数更新"""
    posterior_alpha = prior_alpha + successes
    posterior_beta = prior_beta + trials - successes
    updated_rate = posterior_alpha / (posterior_alpha + posterior_beta)
    return updated_rate

# 示例：先验Beta(2,2)，观测到30个样本中有3个次品
prior_alpha, prior_beta = 2, 2
successes, trials = 3, 30
updated_rate = bayesian_update(prior_alpha, prior_beta, successes, trials)
print(f"\n=== 问题四：贝叶斯更新 ===")
print(f"先验: Beta({prior_alpha}, {prior_beta})")
print(f"观测: {successes}/{trials} 次品")
print(f"后验次品率: {updated_rate:.4f}")

# ==================== 可视化 ====================

def plot_results(results):
    """绘制结果可视化"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 利润对比
    ax1 = axes[0, 0]
    situations = [f"情况{i}" for i in range(1, 7)]
    profits = [r['profit'] for r in results]
    ax1.bar(situations, profits, color=['#2ecc71' if p > 15 else '#e74c3c' for p in profits])
    ax1.set_title('各情况期望利润对比')
    ax1.set_ylabel('期望利润')
    ax1.grid(axis='y', alpha=0.3)
    
    # 合格率对比
    ax2 = axes[0, 1]
    qualities = [r['quality'] for r in results]
    ax2.bar(situations, qualities, color='#3498db')
    ax2.set_title('各情况产品合格率对比')
    ax2.set_ylabel('合格率(%)')
    ax2.grid(axis='y', alpha=0.3)
    
    # 成本构成
    ax3 = axes[1, 0]
    costs = [r['cost'] for r in results]
    ax3.bar(situations, costs, color='#9b59b6')
    ax3.set_title('各情况总成本对比')
    ax3.set_ylabel('总成本')
    ax3.grid(axis='y', alpha=0.3)
    
    # 利润vs合格率
    ax4 = axes[1, 1]
    ax4.scatter(qualities, profits, s=100, c=range(6), cmap='viridis')
    for i, (q, p) in enumerate(zip(qualities, profits)):
        ax4.annotate(f'情况{i+1}', (q, p), textcoords="offset points", xytext=(0,5))
    ax4.set_xlabel('合格率(%)')
    ax4.set_ylabel('期望利润')
    ax4.set_title('利润与合格率关系')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('决策优化结果.png', dpi=300, bbox_inches='tight')
    plt.show()

plot_results(results)
