import numpy as np
import matplotlib.pyplot as plt

data = np.array([
    [1790, 3.9], [1800, 5.3], [1810, 7.2], [1820, 9.6], [1830, 12.9],
    [1840, 17.1], [1850, 23.2], [1860, 31.4], [1870, 38.6], [1880, 50.2],
    [1890, 62.9], [1900, 76.0], [1910, 92.0], [1920, 105.7], [1930, 122.8],
    [1940, 131.7], [1950, 150.7], [1960, 179.3], [1970, 203.2], [1980, 226.5],
    [1990, 248.7], [2000, 281.4]
])
years = data[:, 0]
actual_population = data[:, 1]

# 转换为十年为单位的相对时间
t = (years - years[0]) // 10  # 从1790年开始计算十年间隔
X = actual_population

# 指数增长模型定义
def exponential_growth(t, X0, r):
    """指数增长模型 X(t) = X0 * e^(rt)"""
    return X0 * np.exp(r * t)

# 最小二乘法实现（线性化处理）
# 线性化模型：ln(X) = rt + ln(X0)
t = years - years[0]  # 获取年数差（0, 10, 20,...210）

Y = np.log(X)
A = np.column_stack([t/10, np.ones_like(t)])

# 正规方程求解
theta = np.linalg.inv(A.T @ A) @ A.T @ Y
r_per_decade = theta[0]  # 直接对应每10年增长率
lnX0 = theta[1]
X0 = np.exp(lnX0)

print(f"Linear Least Squares: X0={X0:.2f}  r={r_per_decade:.4f}/10yr")

plt.figure(figsize=(10,6))
plt.scatter(t, X, c='blue', s=100, label='Observed data')
plt.plot(t, X0 * np.exp(r_per_decade * t/10), 'r--', lw=2, label='Model fit')
plt.xlabel('Years since 1790', fontsize=12)
plt.ylabel('Population (millions)', fontsize=12)
plt.title('Population Growth Model Fitting', fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('latex/figure/population_growth_model_fitting.png', dpi=300)
