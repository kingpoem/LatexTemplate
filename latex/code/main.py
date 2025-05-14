import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Step1: Prepare and check data
year = np.array([1949, 1950, 1951, 1956, 1960, 1966, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977,
1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992,
1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007,
2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
2023])
pop = np.array([54167, 55195, 56300, 61465, 66207, 72538, 82992, 85229, 87177, 89211, 90869, 92420,
93717, 94974, 96259, 97542, 98705, 100772, 101654, 103008, 104357, 105851, 107507, 109300,
111026, 112704, 114333, 115823, 117171, 118517, 119850, 121121, 122369, 123626, 124761,
125785, 126743, 127827, 128453, 129227, 129988, 130756, 131448, 132129, 132802, 133450,
134091, 134916, 135922, 136726, 137846, 139326, 139323, 140011, 140541, 141008, 141212,
141260, 141175, 140967])

x = pop /10000
t = year - year[0]

# Step2: Define Logistic model
def logistic_model(t_val,x_m,x0,r):
    return x_m / (1 + ((x_m-x0)/x0)*np.exp(-r*t_val))

# Step3: Initial guess
beta0 = [max(x)*1.1,x[0],0.03]

# Step4: Fit the model
popt, pconv = curve_fit(logistic_model, t, x, p0=beta0, maxfev=10000)
x_m, x0, r = popt

# 新增评估指标计算
x_pred = logistic_model(t, *popt)  # 获取预测值
ss_res = np.sum((x - x_pred)**2)   # 残差平方和
ss_tot = np.sum((x - np.mean(x))**2)  # 总平方和
r_squared = 1 - (ss_res / ss_tot)     # R²
rmse = np.sqrt(np.mean((x - x_pred)**2))  # RMSE

# Step5: Display results
print(f'x_m = {x_m:.4f} (100 million)')
print(f'x_0 = {x0:.4f} (100 million)')
print(f'r = {r:.4f}/year')
print(f'R² = {r_squared:.4f}')  # 新增R²输出
print(f'RMSE = {rmse:.4f} (100 million)')  # 新增RMSE输出

# Step6: Plot original data vs fitted curve
t_fit = np.linspace(0,t[-1],200)
x_fit = logistic_model(t_fit,*popt)

plt.figure(figsize=(10,6))
plt.scatter(year,x,s=32,c='b')
plt.plot(year[0]+t_fit,x_fit,'r-',linewidth=2.5)
plt.xlabel('Year')
plt.ylabel('Population (100 million)')
plt.legend(['Original Data','Logistic Fit'],loc='best')
plt.title('Population Data vs Logistic Model Fit Comparison')
plt.grid(True)
plt.savefig('./latex/figure/population.png', dpi=300, bbox_inches='tight')
