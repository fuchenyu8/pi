# -*- coding: utf-8 -*-
"""
国赛B题: 问题二详细代码 - 决策优化模型
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class ProductionDecisionOptimizer:
    """生产决策优化器"""
    
    def __init__(self, params):
        self.params = params
    
    def calculate_profit(self, d1, d2, df, dd):
        """计算期望利润"""
        p = self.params
        
        # 零件合格率
        p_good1 = 1.0 if d1 else (1 - p['defect_rate_part1'])
        p_good2 = 1.0 if d2 else (1 - p['defect_rate_part2'])
        
        # 成品合格率
        q = p_good1 * p_good2 * (1 - p['final_product_defect_rate'])
        
        # 成本计算
        part1_cost = p['purchase_price_part1'] / (1 - p['defect_rate_part1']) if d1 else p['purchase_price_part1']
        part2_cost = p['purchase_price_part2'] / (1 - p['defect_rate_part2']) if d2 else p['purchase_price_part2']
        part1_inspect = p['inspection_cost_part1'] / (1 - p['defect_rate_part1']) if d1 else 0
        part2_inspect = p['inspection_cost_part2'] / (1 - p['defect_rate_part2']) if d2 else 0
        final_inspect = p['final_product_assembly_cost'] if df else 0
        
        C_unit = part1_cost + part2_cost + part1_inspect + part2_inspect + p['assembly_cost'] + final_inspect
        
        recycle = (p['purchase_price_part1'] + p['purchase_price_part2']) if dd else 0
        disassembly = p['disassembly_cost'] if dd else 0
        
        if df:
            V = (C_unit + (1 - q) * (disassembly - recycle)) / q
        else:
            V = (C_unit + (1 - q) * (p['return_loss'] + disassembly - recycle)) / q
        
        profit = p['market_price'] - V
        return profit, q, V
    
    def find_optimal(self):
        """寻找最优决策"""
        best_profit = -float('inf')
        best_decision = None
        
        for d1, d2, df, dd in product([0, 1], repeat=4):
            profit, q, V = self.calculate_profit(d1, d2, df, dd)
            if profit > best_profit:
                best_profit = profit
                best_decision = (d1, d2, df, dd)
                best_q = q
                best_V = V
        
        return best_decision, best_profit, best_q, best_V
    
    def sensitivity_analysis(self, param_name, values):
        """敏感性分析"""
        profits = []
        original_value = self.params[param_name]
        
        for value in values:
            self.params[param_name] = value
            _, profit, _, _ = self.find_optimal()
            profits.append(profit)
        
        self.params[param_name] = original_value
        
        plt.figure(figsize=(8, 5))
        plt.plot(values, profits, 'bo-')
        plt.xlabel(param_name)
        plt.ylabel('期望利润')
        plt.title(f'{param_name}敏感性分析')
        plt.grid(alpha=0.3)
        plt.savefig(f'敏感性分析_{param_name}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return profits

# 示例参数
params_example = {
    'defect_rate_part1': 0.1, 'purchase_price_part1': 4, 'inspection_cost_part1': 2,
    'defect_rate_part2': 0.1, 'purchase_price_part2': 18, 'inspection_cost_part2': 3,
    'assembly_cost': 6, 'final_product_defect_rate': 0.1,
    'final_product_assembly_cost': 3, 'market_price': 56,
    'return_loss': 6, 'disassembly_cost': 5
}

# 运行优化
optimizer = ProductionDecisionOptimizer(params_example)
decision, profit, q, V = optimizer.find_optimal()
print(f"最优决策: {decision}")
print(f"期望利润: {profit:.2f}")
print(f"合格率: {q*100:.1f}%")
