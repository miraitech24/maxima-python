#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 11:51:44 2026

@author: iwamura
"""

import sympy
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, exp, sqrt, lambdify

# 1. SymPy：解析解の定義（不変）
# --------------------------------------------------
t, L, C, R, V_in = symbols('t L C R V_in')
expr_i = (sqrt(C)*V_in*exp((1/2)*t*(-R + sqrt(C*R**2 - 4*L)/sqrt(C))/L)/sqrt(C*R**2 - 4*L) - 
          sqrt(C)*V_in*exp(-1/2*t*(R + sqrt(C*R**2 - 4*L)/sqrt(C))/L)/sqrt(C*R**2 - 4*L))

f_i = lambdify((t, L, C, R, V_in), expr_i, modules=[{'sqrt': np.lib.scimath.sqrt}, 'numpy'])

# 2. Python：電圧最適化と i_vals の保存
# --------------------------------------------------
L_v, C_v, R_v = 0.05, 0.002, 1.5
k, g_limit = 0.001, 50
t_space = np.linspace(0, 0.1, 1000)

# 単位電圧あたりの最大電流から v_limit を算出
i_unit = np.real(f_i(t_space, L_v, C_v, R_v, 1.0))
v_limit = np.sqrt(g_limit / k) / np.max(i_unit)

# 【これが確定データ】
i_vals = i_unit * v_limit

# #47b（ROI計算）への引き渡しファイル作成
# 電流値をcsvとして保存し、次工程で「熱損失 = Σ(R * i^2 * dt)」を計算させる
np.savetxt('pulse_data.csv', i_vals, delimiter=',')

print(f"--- #33 Finalized ---")
print(f"Selected Voltage: {v_limit:.2f}V")
print(f"Data saved to 'pulse_data.csv' for #47b calculation.")

# 3. グラフ：物理的変化の確認
# --------------------------------------------------
plt.figure(figsize=(10, 4))
plt.plot(t_space, i_vals, color='cyan', label=f'Optimized i_vals ({v_limit:.1f}V)')
plt.fill_between(t_space, i_vals, color='cyan', alpha=0.1)
plt.title("Final Pulse Profile for #47b Export")
plt.ylabel("Current [A]")
plt.legend()
plt.show()

# 考察：何をどうしたか
# 1. 5000Vでは強すぎて筐体が壊れる（50G超）ため、SymPy解をベースに「50Gに収まる電圧」を逆算した。
# 2. その結果、波形全体が「相似形」のまま小さくなり、ボトムの跳ね返りも軽減された。
# 3. この i_vals を 'pulse_data.csv' に書き出した。
# 4. #47b では、この電流が流れることで発生する「ジュール熱（無駄なエネルギー）」を
#    このファイルから読み込んで計算し、プロジェクトの最終利益から差し引く。