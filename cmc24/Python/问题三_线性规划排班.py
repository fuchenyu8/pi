# -*- coding: utf-8 -*-
"""
问题三：线性规划排班完整代码
"""

import pulp
import pandas as pd


# 订单分配函数
def order(hourly_orders):
    """
    将每小时订单分配到各个班次
    """
    # 定义班次时间范围(每个元组表示一个班次,包括开始时间和结束时间)
    shifts = [(0, 8), (5, 13), (8, 16), (12, 20), (14, 22), (16, 24)]

    # 初始化每个班次的订单数量为0
    shift_orders = {shift: 0 for shift in shifts}

    # 遍历每小时的订单情况
    for hour, orders in enumerate(hourly_orders):
        # 查找当前小时可用的班次(即订单产生时间在班次时间范围内的班次)
        available_shifts = [shift for shift in shifts if shift[0] <= hour < shift[1]]

        # 找到当前可用班次中订单最少的班次(即当前订单数最少的班次)
        least_busy_shift = min(available_shifts, key=lambda x: shift_orders[x])

        # 将当前小时的订单分配给最少订单的班次
        shift_orders[least_busy_shift] += orders

    # 返回每个班次的订单数量列表
    return list(shift_orders.values())


# 排班函数
def opt(daily_loads):
    """
    使用线性规划进行排班优化
    """
    ls = []
    days = 1  # 天数,这里为了简化问题设为1
    shifts = 6  # 班次数量
    regular_workers = 60  # 固定员工数量
    efficiency_reg = 25  # 固定员工效率
    efficiency_temp = 20  # 临时员工效率

    # 创建线性规划问题
    prob = pulp.LpProblem("Staff_Optimization", pulp.LpMinimize)

    # 创建决策变量
    X_d = pulp.LpVariable.dicts("X_d", (range(days), range(shifts)), lowBound=0, upBound=regular_workers, cat='Integer')
    Y_d = pulp.LpVariable.dicts("Y_d", (range(days), range(shifts)), lowBound=0, cat='Integer')

    # 定义目标函数
    prob += pulp.lpSum([X_d[d][s] + Y_d[d][s] for d in range(days) for s in range(shifts)])

    # 添加约束条件:每个班次的总工作量需求必须被满足
    for d in range(days):
        for s in range(shifts):
            prob += (X_d[d][s] * efficiency_reg + Y_d[d][s] * efficiency_temp) >= daily_loads[d][s]

    # 添加约束条件:每天的固定员工数量不能超过预设值
    for d in range(days):
        prob += pulp.lpSum([X_d[d][s] for s in range(shifts)]) <= regular_workers

    # 解决线性规划问题
    prob.solve()

    # 将结果存储在列表中并返回
    for d in range(days):
        for s in range(shifts):
            ls.append([pulp.value(X_d[d][s]), pulp.value(Y_d[d][s])])

    return ls


# 主程序
if __name__ == "__main__":
    # 读取CSV文件为DataFrame
    df = pd.read_csv('结果表4.csv')

    # 初始化列表
    ls1 = []
    ls2 = []

    # 遍历分拣中心
    for center in df['分拣中心'].unique():
        # 提取当前分拣中心的数据
        tem = df[df.分拣中心 == center]

        # 按日期和小时分组,计算每个小时的货量总和
        result = tem.groupby(['日期', '小时'])['货量'].sum()

        # 初始化每日货量列表
        daily_loads = []

        # 临时列表用于存储每日的小时货量
        tem = []

        for index, i in enumerate(result.values):
            tem.append(i)
            # 每累计完24小时,将小时货量列表添加到每日货量列表中
            if len(tem) == 24:
                daily_loads.append(tem)
                tem = []

        # 遍历每日货量列表
        for loads in daily_loads:
            # 调用order函数计算每个班次的订单量,并传递给opt函数进行排班优化
            # opt函数返回每个班次的固定员工数量和临时员工数量
            for reg, tem in opt([order(loads)]):
                # 输出每个班次的固定员工数量和临时员工数量
                print(reg, tem)
                # 将结果添加到列表中
                ls1.append(reg)
                ls2.append(tem)

    # 生成结果DataFrame
    df = pd.read_csv('结果表4.csv')

    # 定义班次时间段列表
    time_delta = ['00:00-08:00', '05:00-13:00', '08:00-16:00', '12:00-20:00', '14:00-22:00', '16:00-24:00']

    # 初始化空列表,用于存储结果
    ls = []

    # 遍历分拣中心
    for center in df['分拣中心'].unique():
        # 遍历日期
        for date in df['日期'].unique():
            # 遍历班次时间段
            for time in time_delta:
                # 将分拣中心、日期和班次时间段组合成一个列表,并添加到结果列表中
                ls.append([center, date, time])

    # 将结果列表转换为DataFrame
    res = pd.DataFrame(ls, columns=['分拣中心', '日期', '班次'])

    # 添加正式工人数和临时工人数列
    res['正式工人数'] = ls1
    res['临时工人数'] = ls2

    # 将结果保存为CSV文件
    res.to_csv('排班结果.csv', index=False)
    print("排班结果已保存到: 排班结果.csv")
