from pulp import LpProblem, LpMaximize, LpVariable, value

prob = LpProblem("Crude_Oil_Optimization", LpMaximize)

# 定义分段采购变量
x1 = LpVariable("x1", 0, 500)    # 0-500吨区间
x2 = LpVariable("x2", 0, 500)    # 501-1000吨区间
x3 = LpVariable("x3", 0, 500)    # 1001-1500吨区间

# 添加分段约束
prob += x1 <= 500
prob += x2 <= 500
prob += x3 <= 500
prob += x1 + x2 + x3 <= 1500  # 总采购量约束

# 计算分段成本
purchase_cost = 10000*x1 + 8000*x2 + 6000*x3

# 定义生产量变量
gas_A = LpVariable("Gas_A", 0, None)  # 汽油甲产量
gas_B = LpVariable("Gas_B", 0, None)  # 汽油乙产量

# 原料分配约束
prob += x2 + x3 <= 500 + x1 + x2 + x3  # 原油A总用量
prob += (gas_A <= (x2 + 1000 - (x2+x3))/0.5, "Gas_A_ratio")  # 甲的比例约束
prob += (gas_B <= (x3 + 1000 - (x2+x3))/0.6, "Gas_B_ratio")  # 乙的比例约束

# 建立目标函数
revenue = 4800*gas_A + 5600*gas_B
prob += revenue - purchase_cost

# 求解并输出结果
prob.solve()
print(f"最优采购方案：{value(x1)+value(x2)+value(x3):.0f}吨")
print(f"最大利润：{value(prob.objective):.2f}元")
