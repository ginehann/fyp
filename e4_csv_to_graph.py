import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import pandas as pd
import numpy as np

table = '/Users/yapginehann/Desktop/codes/recordings/e4.1/feed_table.csv'
df = pd.read_csv(table)

x = np.array([1, 2, 3, 4, 5, 6])
y_1 = np.array(df['mean_activity'])
y_2 = np.array(df['interval']) / 3600

X_Y_Spline_1 = make_interp_spline(x, y_1, bc_type='natural')
X_Y_Spline_2 = make_interp_spline(x, y_2, bc_type='natural')
X_ = np.linspace(x.min(), x.max(), 500)
Y_1 = X_Y_Spline_1(X_)
Y_2 = X_Y_Spline_2(X_)

fig, ax = plt.subplots()

ax.plot(X_, Y_1, color='red')
ax.plot(x, y_1, 'ro')
ax.tick_params(axis='y', labelcolor='darkred')

ax2 = ax.twinx()
ax2.plot(X_, Y_2, color='blue')
ax2.plot(x, y_2, 'bo')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.yaxis.set_label_position("right")
ax2.yaxis.set_ticks_position("right")
ax2.set_ylabel('Interval to next feeding event (hrs)', color='blue')

ax.set_ylabel('Mean velocity (pixels per second)', color='darkred')
ax.set_xlabel('Feeding events')
ax.set_title("Feeding logic log")
ax.set_ylim(None, 1800)
ax2.set_ylim(-30, 150)

# plt.show()
output_graph = '/Users/yapginehann/Desktop/codes/recordings/e41, chrono.png'
plt.savefig(output_graph)



