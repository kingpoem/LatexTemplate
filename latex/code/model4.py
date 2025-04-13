import pulp

swimmers = ['甲', '乙', '丙', '丁', '戊']
strokes = ['蝶泳', '仰泳', '蛙泳', '自由泳']

times = {
    ('甲', '蝶泳'): 66.8, ('甲', '仰泳'): 75.6, ('甲', '蛙泳'): 87.0, ('甲', '自由泳'): 58.6,
    ('乙', '蝶泳'): 57.2, ('乙', '仰泳'): 66.0, ('乙', '蛙泳'): 66.4, ('乙', '自由泳'): 53.0,
    ('丙', '蝶泳'): 78.0, ('丙', '仰泳'): 67.8, ('丙', '蛙泳'): 84.6, ('丙', '自由泳'): 59.4,
    ('丁', '蝶泳'): 70.0, ('丁', '仰泳'): 74.2, ('丁', '蛙泳'): 69.6, ('丁', '自由泳'): 57.2,
    ('戊', '蝶泳'): 67.4, ('戊', '仰泳'): 71.0, ('戊', '蛙泳'): 83.8, ('戊', '自由泳'): 62.4
}

def solve_swim_team(modified=False):
    """解决混合泳接力队选拔问题"""
    prob = pulp.LpProblem("SwimTeamSelection", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("assign", [(s, st) for s in swimmers for st in strokes], cat='Binary')
    
    # 目标函数：最小化总时间
    prob += pulp.lpSum([x[(s, st)] * times[(s, st)] for (s, st) in x])
    
    # 泳姿约束：每个泳姿必须分配一人
    for st in strokes:
        prob += pulp.lpSum([x[(s, st)] for s in swimmers]) == 1
    
    # 运动员约束：每人最多分配一个泳姿
    for s in swimmers:
        prob += pulp.lpSum([x[(s, st)] for st in strokes]) <= 1
    
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    print(f"\n{'调整后' if modified else '原始'}最优分配方案：")
    total_time = 0
    assignment = []
    for st in strokes:
        for s in swimmers:
            if x[(s, st)].value() == 1:
                time = times[(s, st)]
                assignment.append(f"{s}→{st}({time}s)")
                total_time += time
                break
    print(" + ".join(assignment))
    print(f"总时间：{total_time:.1f}秒")

solve_swim_team()

times[('丁', '蛙泳')] = 75.2   # 丁的蛙泳退步到1'15"2
times[('戊', '自由泳')] = 57.5  # 戊的自由泳进步到57"5
solve_swim_team(modified=True)