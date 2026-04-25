#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 12:49:18 2026

@author: iwamura
"""

import numpy as np
import sympy as sp

# 1. 物理定数と変数の定義
t, M0, m_dot, Isp, g0 = sp.symbols('t M0 m_dot Isp g0', positive=True)

# 質量比と距離の解析解（実数領域）
r = M0 / (M0 - m_dot * t)
dist_expr = (Isp * g0) * (t - (M0 - m_dot * t) / m_dot * sp.log(r))
f_dist = sp.lambdify((t, M0, m_dot, Isp, g0), dist_expr, 'numpy')

# 2. パラメータ設定 (14日間ミッション)
params_val = {
    "M0": 20_000_000,    # 初期質量 2万トン
    "Isp": 10000,        # 比推力 10,000s
    "g0": 9.80665,
    "m_dot": 15.5,       # 燃料消費率 15.5 kg/s
}
target_time = 14 * 24 * 3600  # 14日間（秒）

# 3. 計算実行
dist_km = float(f_dist(target_time, **params_val)) / 1000

# 最終速度と燃料消費量の算出（シンボルを完全に数値置換）
v_final_val = (params_val["Isp"] * params_val["g0"]) * np.log(
    params_val["M0"] / (params_val["M0"] - params_val["m_dot"] * target_time)
)
fuel_consumed_tons = params_val["m_dot"] * target_time / 1000

print(f"--- #48/#57 Finalized ---")
print(f"Total Distance: {dist_km/1e6:.2f} million km (Goal: 41.4M km)")
print(f"Final Velocity: {v_final_val:.2f} m/s")
print(f"Fuel Consumed: {fuel_consumed_tons:.2f} tons")
print(f"Status: {'SUCCESS' if dist_km/1e6 >= 41.4 else 'RETRY'}")