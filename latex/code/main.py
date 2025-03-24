from pulp import LpProblem, LpMaximize, LpVariable

# 初始化问题
prob = LpProblem("Dairy_Production_Planning", LpMaximize)

# 定义决策变量
x1 = LpVariable("Product1", lowBound=0, cat='Continuous')  # 奶制品1的产量(kg)
x2 = LpVariable("Product2", lowBound=0, cat='Continuous')  # 奶制品2的产量(kg)
x3 = LpVariable("Product3", lowBound=0, cat='Continuous')  # 奶制品1的精加工后的产量(kg)
x4 = LpVariable("Product4", lowBound=0, cat='Continuous')  # 奶制品2的精加工后的产量(kg)

# 目标函数（每日利润最大化）
prob += 24*(x1 - (x3*(1/0.8))) + (44*x3) + \
        16*(x2 - (x4*(1/0.75))) + (32*x4), "Total_Profit"

# 添加约束条件
# 牛奶约束（每桶牛奶12kg，每天最多50桶）
prob += 12*x1 + 8*x2 <= 50*12, "Milk_Constraint"

# 时间约束（每天480小时）
prob += 3*x1 + x2 + 2*x3 + 2*x4 <= 480, "Time_Constraint"

# 设备约束（奶制品1最多100kg）
prob += x1 <= 100, "Equipment_Constraint"

prob.solve()

print("生产计划优化结果:")
print(f"奶制品1产量: {x1.varValue:.2f} kg")
print(f"奶制品2产量: {x2.varValue:.2f} kg")
print(f"奶制品精加工1产量: {x3.varValue:.2f} kg")
print(f"奶制品精加工2产量: {x4.varValue:.2f} kg")
print(f"最大日利润: {prob.objective.value():.2f} 元")

# 灵敏度分析
print("\n灵敏度分析:")
for constraint in prob.constraints.values():
    print(f"约束 '{constraint.name}' 影子价格: {constraint.pi:.2f}")
