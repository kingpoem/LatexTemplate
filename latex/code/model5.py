import pulp

courses = [
    {'id':1, 'name':'微积分', '学分':5, '类别':'数学', '先修课':[]},
    {'id':2, 'name':'线性代数', '学分':4, '类别':'数学', '先修课':[]},
    {'id':3, 'name':'最优化方法', '学分':3, '类别':'运筹学', '先修课':[7]},
    {'id':4, 'name':'数据结构', '学分':3, '类别':'计算机', '先修课':[]},
    {'id':5, 'name':'应用统计', '学分':3, '类别':'数学', '先修课':[]},
    {'id':6, 'name':'计算机模拟', '学分':3, '类别':'运筹学', '先修课':[]},
    {'id':7, 'name':'计算机编程', '学分':2, '类别':'计算机', '先修课':[]},
    {'id':8, 'name':'预测理论', '学分':3, '类别':'运筹学', '先修课':[5]},
    {'id':9, 'name':'数学实验', '学分':3, '类别':'数学', '先修课':[]}
]

def build_model(phase=1):
    """构建优化模型"""
    prob = pulp.LpProblem("CourseSelection", pulp.LpMinimize if phase==1 else pulp.LpMaximize)
    
    # 创建决策变量
    x = {c['id']: pulp.LpVariable(f"x{c['id']}", cat='Binary') for c in courses}
    
    # 目标函数
    if phase == 1:
        prob += pulp.lpSum(x.values())  # 最小化课程数
    else:
        prob += pulp.lpSum(c['学分']*x[c['id']] for c in courses)  # 最大化学分
    
    # 公共约束条件
    math = [c['id'] for c in courses if c['类别'] == '数学']
    ors = [c['id'] for c in courses if c['类别'] == '运筹学']
    cs = [c['id'] for c in courses if c['类别'] == '计算机']
    
    prob += pulp.lpSum(x[m] for m in math) >= 2    # 数学至少2门
    prob += pulp.lpSum(x[o] for o in ors) >= 3     # 运筹学至少3门
    prob += pulp.lpSum(x[c] for c in cs) >= 2      # 计算机至少2门
    
    # 先修课约束
    for c in courses:
        for p in c['先修课']:
            prob += x[c['id']] <= x[p]  # 选修课程c必须先修p
    
    # 二阶段额外约束
    if phase == 2:
        # 添加课程数等于第一阶段最优解的约束
        min_courses = sum(var.value() for var in x.values())
        prob += pulp.lpSum(x.values()) == min_courses
    
    return prob, x

# 第一阶段：最小化课程数
prob1, x1 = build_model(phase=1)
prob1.solve(pulp.PULP_CBC_CMD(msg=False))

# 解析第一阶段结果
selected_phase1 = [c for c in courses if x1[c['id']].value() == 1]
print("问题一：最少选修课程方案")
print(f"课程数: {len(selected_phase1)}")
print("选课列表:", [c['name'] for c in selected_phase1])
print("总学分:", sum(c['学分'] for c in selected_phase1))

# # 第二阶段：最大化学分
# prob2, x2 = build_model(phase=2)
# prob2.solve(pulp.PULP_CBC_CMD(msg=False))

# # 解析第二阶段结果
# selected_phase2 = [c for c in courses if x2[c['id']].value() == 1]
# print("\n问题二：最少课程下的最高学分方案")
# print(f"课程数: {len(selected_phase2)}")
# print("选课列表:", [c['name'] for c in selected_phase2])
# print("总学分:", sum(c['学分'] for c in selected_phase2))