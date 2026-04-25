import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# データ読み込み
df = pd.read_csv('VF005_simple_data.csv')

# 温度プロット
plt.figure(figsize=(10, 6))
plt.plot(df['t'], df['T_s'], 'r-', label='表面温度 T_s', linewidth=2)
plt.plot(df['t'], df['T_a'], 'b-', label='大気温度 T_a', linewidth=2)
plt.xlabel('時間 (年)')
plt.ylabel('温度 (K)')
plt.title('VF-005: 金星温度進化')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('VF005_python_temperatures.png', dpi=300)
plt.show()

# SR風速プロット
plt.figure(figsize=(10, 6))
plt.plot(df['t'], df['S'], 'g-', label='SR風速係数 S', linewidth=2)
plt.xlabel('時間 (年)')
plt.ylabel('風速係数')
plt.title('VF-005: SR風速係数')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('VF005_python_wind.png', dpi=300)
plt.show()

print('プロット完了')
