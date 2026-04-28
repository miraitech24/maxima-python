#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 08:01:09 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAI‑18 把持ハンド：磁場外乱シミュレーション
Maximaが出力した pai18_maxout.csv を読み込み、コイルの向き（磁場との角度）を
ランダムに変えながら外乱力を計算し、統計を表示します。
"""

import numpy as np
import matplotlib.pyplot as plt
import os, sys

# ファイル存在確認（なければ停止）
CSV_FILE = "pai18_maxout.csv"
if not os.path.exists(CSV_FILE):
    print(f"ERROR: {CSV_FILE} not found. Run Maxima first.")
    sys.exit(1)

data = np.genfromtxt(CSV_FILE, delimiter=',', names=True)

# パラメータ
L_coil = 0.05           # コイル長 [m]（Maximaと同じ）
B_jupiter = 420e-9      # 磁場 [T]
n_samples = 1000        # 角度試行回数

print("R [m] ごとの外乱力（方向ランダム）の最大値・平均値・標準偏差")
print("-" * 60)
for row in data:
    R = row['R']
    I_act = row['I_act']
    # 磁場とコイルの角度θ [0, π] 一様分布 → 力の大きさは |sinθ| に比例
    theta = np.random.uniform(0, np.pi, n_samples)
    F_dist_inst = np.abs(I_act * L_coil * B_jupiter * np.sin(theta))  # 垂直成分
    max_val = np.max(F_dist_inst)
    mean_val = np.mean(F_dist_inst)
    std_val = np.std(F_dist_inst)
    print(f"R={R:.2f}m  max={max_val:.2e}N  mean={mean_val:.2e}N  std={std_val:.2e}N")

# ヒストグラム例（R=0.05 m）
R_target = 0.05
idx = np.argmin(np.abs(data['R'] - R_target))
I_target = data['I_act'][idx]
theta = np.random.uniform(0, np.pi, n_samples)
F_samples = np.abs(I_target * L_coil * B_jupiter * np.sin(theta))

plt.hist(F_samples, bins=30, color='c', edgecolor='k')
plt.xlabel('Disturbance force (N)')
plt.ylabel('Frequency')
plt.title(f'Histogram of magnetic disturbance force (R={R_target} m)')
plt.grid(True)
plt.tight_layout()
plt.savefig('pai18_dist_hist.png', dpi=150)
plt.show()
print("Histogram saved as pai18_dist_hist.png")
