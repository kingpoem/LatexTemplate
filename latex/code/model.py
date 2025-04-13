# B23040408 王俊琦
# 至少生产80辆
import pulp
from pulp import LpProblem, LpMaximize, LpVariable

prob = LpProblem("Car_Production_Optimization", LpMaximize)

# 定义决策变量（整数类型，且如果生产则≥80）
x1 = LpVariable("Small", lowBound=0, cat="Integer")  # 小型车
x2 = LpVariable("Medium", lowBound=0, cat="Integer") # 中型车
x3 = LpVariable("Large", lowBound=0, cat="Integer")  # 大型车

# 引入0-1变量表示是否生产该车型
y1 = LpVariable("Produce_Small", cat="Binary")  # 小型车
y2 = LpVariable("Produce_Medium", cat="Binary") # 中型车
y3 = LpVariable("Produce_Large", cat="Binary")  # 大型车

# 目标函数：利润最大化
prob += 2 * x1 + 3 * x2 + 4 * x3, "Total_Profit"

# 资源约束
prob += 1.5 * x1 + 3 * x2 + 5 * x3 <= 600, "Steel_Constraint"
prob += 280 * x1 + 250 * x2 + 400 * x3 <= 60000, "Labor_Constraint"

M = 1000 
prob += x1 >= 80 * y1, "Min_Production_Small"
prob += x1 <= M * y1, "Link_Small_Production"
prob += x2 >= 80 * y2, "Min_Production_Medium"
prob += x2 <= M * y2, "Link_Medium_Production"
prob += x3 >= 80 * y3, "Min_Production_Large"
prob += x3 <= M * y3, "Link_Large_Production"
prob.solve()
print("Status:", pulp.LpStatus[prob.status])
print("Optimal Production Plan:")
print(f"Small Cars: {int(x1.value())} (Profit: {2 * x1.value()}万元)")
print(f"Medium Cars: {int(x2.value())} (Profit: {3 * x2.value()}万元)")
print(f"Large Cars: {int(x3.value())} (Profit: {4 * x3.value()}万元)")
print(f"Total Profit: {pulp.value(prob.objective)}万元")