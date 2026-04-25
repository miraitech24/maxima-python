#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 13:19:38 2026

@author: iwamura
"""

import numpy as np
import pandas as pd

# 1. #33からの物理フィードバック
def get_initial_velocity_from_33():
    # pulse_data.csv (電流値) からローレンツ力を積分して初速を算出
    i_vals = np.loadtxt('pulse_data.csv', delimiter=',')
    k_factor = 0.05  # 加速器の設計定数
    dt = 0.0001
    # 速度 v = ∫ (k * i^2 / m) dt
    v_exit = np.sum(k_factor * (i_vals**2) / 500 * dt) 
    return v_exit

# 2. #56からの排熱制約フィードバック
def get_safe_thrust_limit():
    T_limit = 550.0   # ハイドライド自壊温度 [K]
    Area = 1200.0     # ラジエーター面積 [m^2]
    Loss_Factor = 1200.0 # 1Nあたりの排熱
    # 熱平衡式から最大推力を逆算
    # P_rad = sigma * epsilon * Area * T^4
    f_max = (5.67e-8 * 0.9 * Area * (T_limit**4)) / Loss_Factor
    return f_max

# 3. 軌道・ROI連成計算
v0 = get_initial_velocity_from_33()
f_limit = get_safe_thrust_limit()

print(f"--- #48 Feedback Integration ---")
print(f"Initial Velocity (from #33): {v0:.2f} m/s")
print(f"Max Safe Thrust (from #56): {f_limit:.2f} N")

# ここで14日間の積分を行い、消費燃料を算出 -> #47bへ
# 燃料消費が多すぎれば ROI 525% が削られる「真実」が出る