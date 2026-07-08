# -*- coding: utf-8 -*-
"""
问题四：模拟退火算法框架代码
"""

import random
import math


# 定义目标函数
def objective_function(x):
    """
    计算总人天数（目标函数）
    TODO: 填充总人天数计算逻辑
    """
    # 示例：计算x中所有元素的和
    return sum(x)


# 定义约束条件函数
def constraint_function(x):
    """
    约束条件检查
    TODO: 出勤率、连续上班、货量约束校验
    返回True表示满足约束，False表示不满足
    """
    # 示例约束：所有值必须非负
    return all(val >= 0 for val in x)


# 生成新解的函数
def generate_new_solution(current_solution):
    """
    生成邻域解
    TODO: 随机调整员工班次生成邻域解
    """
    new_solution = current_solution.copy()
    # 随机选择一个位置进行调整
    idx = random.randint(0, len(new_solution) - 1)
    # 随机增减1
    new_solution[idx] += random.choice([-1, 1])
    # 确保非负
    new_solution[idx] = max(0, new_solution[idx])
    return new_solution


# 计算接受新解的概率
def acceptance_probability(current_cost, new_cost, temperature):
    """
    计算Metropolis准则的接受概率
    """
    if new_cost < current_cost:
        return 1.0
    return math.exp((current_cost - new_cost) / temperature)


# 定义模拟退火算法
def simulated_annealing(initial_solution, temperature, cooling_rate, num_iterations):
    """
    模拟退火算法主函数

    参数:
        initial_solution: 初始解
        temperature: 初始温度
        cooling_rate: 冷却速率 (0 < cooling_rate < 1)
        num_iterations: 迭代次数

    返回:
        best_solution: 最优解
    """
    current_solution = initial_solution
    best_solution = initial_solution

    current_cost = objective_function(current_solution)
    best_cost = current_cost

    for i in range(num_iterations):
        # 生成新解
        new_solution = generate_new_solution(current_solution)

        # 检查约束
        if not constraint_function(new_solution):
            continue

        # 计算新解的代价
        new_cost = objective_function(new_solution)

        # 判断是否接受新解
        if new_cost < current_cost:
            current_solution = new_solution
            current_cost = new_cost

            # 更新最优解
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost
        else:
            # 以一定概率接受较差的解
            probability = acceptance_probability(current_cost, new_cost, temperature)
            if random.random() < probability:
                current_solution = new_solution
                current_cost = new_cost

        # 降低温度
        temperature *= cooling_rate

        # 打印进度（可选）
        if (i + 1) % 100 == 0:
            print(f"迭代 {i+1}/{num_iterations}, 当前温度: {temperature:.4f}, 当前最优: {best_cost:.2f}")

    return best_solution


# 主程序
if __name__ == "__main__":
    # 设置随机种子以保证可重复性
    random.seed(42)

    # 定义初始解（示例：4个变量）
    initial_solution = [10, 15, 8, 12]

    # 模拟退火参数
    initial_temperature = 100
    cooling_rate = 0.99
    num_iterations = 1000

    print("=" * 50)
    print("模拟退火算法求解")
    print("=" * 50)
    print(f"初始解: {initial_solution}")
    print(f"初始目标值: {objective_function(initial_solution):.2f}")
    print()

    # 调用模拟退火算法求解问题
    best_solution = simulated_annealing(
        initial_solution,
        temperature=initial_temperature,
        cooling_rate=cooling_rate,
        num_iterations=num_iterations
    )

    # 输出最优解
    print()
    print("=" * 50)
    print("求解完成")
    print("=" * 50)
    print(f"最优解: {best_solution}")
    print(f"最优目标值: {objective_function(best_solution):.2f}")
