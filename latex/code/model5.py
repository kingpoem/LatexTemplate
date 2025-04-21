from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, value

# 数据
courses = ["微积分", "线性代数", "最优化方法", "数据结构", "应用统计", "计算机概况", "计算机编程", "预测理论", "数学实验"]
credits = [5, 4, 4, 4, 4, 3, 2, 2, 3]  # 学分
math = [1, 1, 1, 0, 1, 0, 0, 0, 1]     # 是否数学课
operations = [0, 0, 1, 0, 1, 1, 0, 1, 1]  # 是否运筹学课
computer = [0, 0, 0, 1, 0, 1, 1, 0, 0]  # 是否计算机课

# 选修依赖关系 (i 依赖 j 表示 R[i][j] = 1)
R = [[0 for _ in range(9)] for _ in range(9)]
R[0][1] = 1  # 微积分 依赖 线性代数
R[1][0] = 1  # 线性代数 依赖 微积分
R[2][1] = 1  # 最优化方法 依赖 线性代数
R[3][6] = 1  # 数据结构 依赖 计算机编程
R[5][1] = 1  # 计算机概况 依赖 线性代数
R[8][1] = 1  # 数学实验 依赖 线性代数

# 第一问：最小学分
prob1 = LpProblem("Course_Selection_Min_Credits", LpMinimize)

# 决策变量：是否选择课程 i
x = [LpVariable(f"x_{i}", cat=LpBinary) for i in range(9)]

# 目标函数：最小化学分
prob1 += lpSum(credits[i] * x[i] for i in range(9))

# 约束条件
# 至少两门数学课
prob1 += lpSum(math[i] * x[i] for i in range(9)) >= 2
# 至少三门运筹学课
prob1 += lpSum(operations[i] * x[i] for i in range(9)) >= 3
# 至少两门计算机课
prob1 += lpSum(computer[i] * x[i] for i in range(9)) >= 2
# 选修依赖约束
for i in range(9):
    for j in range(9):
        if R[i][j] == 1:
            prob1 += x[i] <= x[j]

# 求解
prob1.solve()

# 输出结果
print("第一问：最优选课方案（最小学分）")
selected_courses = [i for i in range(9) if value(x[i]) == 1]
total_credits = sum(credits[i] for i in selected_courses)
print("选择的课程：", [courses[i] for i in selected_courses])
print("总学分：", total_credits)

# 第二问：最小化每天学习压力
prob2 = LpProblem("Course_Selection_Min_Pressure", LpMinimize)

# 决策变量
x = [LpVariable(f"x_{i}", cat=LpBinary) for i in range(9)]  # 是否选择课程 i
d = [[LpVariable(f"d_{i}_{k}", cat=LpBinary) for k in range(5)] for i in range(9)]  # 课程 i 是否在第 k 天学习
z = LpVariable("z")  # 辅助变量，表示每天学习压力的最大值

# 目标函数：最小化每天学习压力的最大值
prob2 += z

# 约束条件
# 课程类别约束（同第一问）
prob2 += lpSum(math[i] * x[i] for i in range(9)) >= 2
prob2 += lpSum(operations[i] * x[i] for i in range(9)) >= 3
prob2 += lpSum(computer[i] * x[i] for i in range(9)) >= 2
for i in range(9):
    for j in range(9):
        if R[i][j] == 1:
            prob2 += x[i] <= x[j]

# 每天学习压力约束
for k in range(5):
    daily_pressure = lpSum(credits[i] * d[i][k] for i in range(9))
    prob2 += daily_pressure * daily_pressure <= z

# 每门课恰好安排一天
for i in range(9):
    prob2 += lpSum(d[i][k] for k in range(5)) == x[i]

# 每天最多 3 门课
for k in range(5):
    prob2 += lpSum(d[i][k] for i in range(9)) <= 3

# 求解
prob2.solve()

# 输出结果
print("\n第二问：最优选课方案（最小化每天学习压力）")
selected_courses = [i for i in range(9) if value(x[i]) == 1]
print("选择的课程：", [courses[i] for i in selected_courses])
print("总学分：", sum(credits[i] for i in selected_courses))
print("每天安排：")
for k in range(5):
    day_courses = [i for i in range(9) if value(d[i][k]) == 1]
    day_credits = sum(credits[i] for i in day_courses)
    print(f"第 {k+1} 天：{[courses[i] for i in day_courses]}，学分：{day_credits}，压力：{day_credits**2}")
print("最大压力：", value(z))