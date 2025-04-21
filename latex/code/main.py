import pulp

# 课程数据
courses = {
    1: {'credit': 5, 'prerequisites': []},
    2: {'credit': 4, 'prerequisites': []},
    3: {'credit': 4, 'prerequisites': [1, 2]},
    4: {'credit': 3, 'prerequisites': [7]},
    5: {'credit': 4, 'prerequisites': [1, 2]},
    6: {'credit': 3, 'prerequisites': [7]},
    7: {'credit': 2, 'prerequisites': []},
    8: {'credit': 2, 'prerequisites': [5]},
    9: {'credit': 3, 'prerequisites': [1, 2]},
}

# 最少课程数求解
model_min = pulp.LpProblem("Min_Courses", pulp.LpMinimize)
x_min = {i: pulp.LpVariable(f'x_{i}', cat=pulp.LpBinary) for i in courses}
model_min += pulp.lpSum(x_min[i] for i in courses)
for i in courses:
    for p in courses[i]['prerequisites']:
        model_min += x_min[i] <= x_min[p]
model_min.solve()
k_min = int(pulp.value(model_min.objective))
print(f"最少课程数: {k_min}")
selected_min = [i for i in courses if x_min[i].value() == 1]
print("选课方案:", selected_min)

# 多目标优化求解帕累托前沿
pareto_front = []
for k in range(k_min, 10):
    model_max = pulp.LpProblem("Max_Credits", pulp.LpMaximize)
    x_max = {i: pulp.LpVariable(f'x_{i}', cat=pulp.LpBinary) for i in courses}
    model_max += pulp.lpSum(courses[i]['credit'] * x_max[i] for i in courses)
    model_max += pulp.lpSum(x_max[i] for i in courses) == k
    for i in courses:
        for p in courses[i]['prerequisites']:
            model_max += x_max[i] <= x_max[p]
    status = model_max.solve()
    if status == pulp.LpStatusOptimal:
        credits = pulp.value(model_max.objective)
        selected = [i for i in courses if x_max[i].value() == 1]
        pareto_front.append((k, credits, selected))

# 筛选帕累托最优解
pareto_optimal = []
max_credit = -1
for k, c, s in sorted(pareto_front, key=lambda x: x[0]):
    if c > max_credit:
        pareto_optimal.append((k, c, s))
        max_credit = c

print("\n帕累托最优解:")
for k, c, s in pareto_optimal:
    print(f"课程数: {k}, 总学分: {c}, 选课方案: {s}")