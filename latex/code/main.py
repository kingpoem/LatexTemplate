import matplotlib.pyplot as plt
import os

params = {
    't1': 2,        # Start time of firefighting
    't2': 4,        # Completion time of firefighting
    'b': 2,         # Maximum fire intensity
    'beta': 1.5,    # Fire spread slope
    'lambda_theta_X': 2.0  # Firefighting slope parameter
}

t_points = [0, params['t1'], params['t2']]
dB_dt_points = [0, params['b'], 0]

os.makedirs('./latex/figure', exist_ok=True)

plt.figure(figsize=(8, 4), dpi=100)
ax = plt.gca()

ax.plot(t_points, dB_dt_points, 
        color='black', 
        linewidth=1.5,
        marker='o',
        markersize=6)

# Fill areas
ax.fill_between(t_points[:2], 0, dB_dt_points[:2],
                color='violet', alpha=0.15, label='Spread Phase')
ax.fill_between(t_points[1:], 0, dB_dt_points[1:],
                color='lightgray', alpha=0.3, label='Firefighting Phase')

# Axis labels
ax.set_xlabel('Time $t$ (hours)', fontsize=12)
ax.set_ylabel('Fire Spread Rate $\dfrac{\mathrm{d}B}{\mathrm{d}t}$', fontsize=12)
ax.set_xticks([0, params['t1'], params['t2']])
ax.set_xticklabels(['$0$', '$t_1$', '$t_2$'])
ax.set_yticks([0, params['b']])
ax.set_yticklabels(['$0$', '$b$'])
ax.grid(alpha=0.2)

plt.tight_layout()
plt.savefig('./latex/figure/fire_spread.png', bbox_inches='tight')  # 新增保存语句