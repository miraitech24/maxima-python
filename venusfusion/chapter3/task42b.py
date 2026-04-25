#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 12:21:27 2026

@author: iwamura
"""

import sympy as sp
import numpy as np

# --- Step 1: SymPy による解析解導出 ---
def derive_tether_formulas():
    m, v, k, x = sp.symbols('m v k x')
    # エネルギー保存則: 1/2*m*v^2 = 1/2*k*x^2 -> x = v*sqrt(m/k)
    x_max = v * sp.sqrt(m / k)
    # 最大張力 T = k * x
    T_max = k * x_max
    # 最大減速度 a = T / m
    a_max = T_max / m
    return sp.lambdify((m, v, k), (T_max, a_max), 'numpy')

# --- Step 2: Python による数値計算 ---
# 前工程 #34a からのバトン
m_payload = 529.60  # kg
v_rel = 7800.0      # m/s (7.8 km/s)

# テザー諸元 (カーボンナノチューブ・テザー)
L = 100000          # テザー長 100km (衝撃吸収距離を稼ぐため長大化)
E = 1.0e11          # ヤング率 (Pa)
A = 0.00005         # 断面積 (50 mm^2)
k_tether = (E * A) / L

calc_impact = derive_tether_formulas()
T_peak, a_peak = calc_impact(m_payload, v_rel, k_tether)

# 結果出力
print(f"--- #42b Tether Capture Results ---")
print(f"Peak Tension       : {T_peak / 1e6:.2f} MN")
print(f"Peak Deceleration  : {a_peak / 9.80665:.2f} G")
print(f"Tether Stretching  : { (v_rel * np.sqrt(m_payload/k_tether)) / 1000:.2f} km")
print(f"Material Stress    : { (T_peak / A) / 1e9:.2f} GPa")
print(f"Safety Status      : {'SUCCESS' if (T_peak/A) < 60e9 else 'FAILED (Tether Broken)'}")