#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 12:51:07 2026

@author: iwamura
"""

# task26_1.py
# CSV役割：レールガンに流せる最大電流 I を決定する

import numpy as np

# Maximaから設計データをインポート
try:
    with open("params_26_1.txt", "r") as f:
        data = f.read().split()
        C_val = float(data[0])
        V_start = float(data[1])
except:
    C_val, V_start = 16.0, 5000.0 # fallback

# 回路定数（レールの抵抗とインダクタンス）
R, L = 0.005, 1e-6
dt = 1e-6
t = np.arange(0, 0.02, dt)

# 逐次計算（オイラー法）
I_list = []
v_c = V_start
i_l = 0.0

for _ in t:
    di = (v_c - i_l * R) / L * dt
    i_l += di
    v_c -= (i_l / C_val) * dt
    I_list.append(i_l)

# 最大電流 I_max を確定（これが課題43の入力になる）
I_max = max(I_list)
with open("params_Imax.txt", "w") as f:
    f.write(str(I_max))

print(f"Peak Pulse Current: {I_max/1e6:.2f} MA")