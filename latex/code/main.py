from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus, PULP_CBC_CMD, value

courses = {
    1: {'name': '微积分', 'credit':5, 'pre':[]},
    2: {'name': '线性代数', 'credit':4, 'pre':[]},
    3: {'name': '最小化方法', 'credit':4, 'pre':[1,2]},
    4: {'name': '数据结构', 'credit':3, 'pre':[7]},
    5: {'name': '应用统计', 'credit':4, 'pre':[1,2]},
    6: {'name': '计算机模拟', 'credit':3, 'pre':[7]},
    7: {'name': '计算机编程', 'credit':2, 'pre':[]},
    8: {'name': '预测理论', 'credit':2, 'pre':[5]},
    9: {'name': '数学实验', 'credit':3, 'pre':[1,2]}
}

def build_model(weights=(0.5, 0.5)):
    prob = LpProblem("Course_Selection", LpMinimize)
    
    x = LpVariable.dicts('x', courses.keys(), cat='Binary')
    
    total_courses = lpSum(x[c] for c in courses)
    total_credits = lpSum(courses[c]['credit']*x[c] for c in courses)
    prob += weights[0]*total_courses - weights[1]*total_credits
    
    for c in courses:
        for preq in courses[c]['pre']:
            prob += x[c] <= x[preq]
    
    return prob, x

def solve_model(model, variables):
    model.solve(PULP_CBC_CMD(msg=False))
    
    if LpStatus[model.status] != 'Optimal':
        return None
    
    selected = [c for c in courses if value(variables[c]) > 0.5]
    total_credits = sum(courses[c]['credit'] for c in selected)
    return {
        'courses': sorted(selected),
        'total': len(selected),
        'credits': total_credits
    }

prob1, x1 = build_model(weights=(1, 0))
result1 = solve_model(prob1, x1)

prob2, x2 = build_model(weights=(1, 2)) 
result2 = solve_model(prob2, x2)

print(f"问题1结果：选课{result1['total']}门，课程{result1['courses']}，学分{result1['credits']}")
print(f"问题2结果：选课{result2['total']}门，课程{result2['courses']}，学分{result2['credits']}")