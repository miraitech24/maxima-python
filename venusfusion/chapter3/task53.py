#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 13:04:07 2026

@author: iwamura
"""

import sympy as sp
import numpy as np

# --- Step 1: SymPy による滑空解析解の導出 ---
def derive_gliding_range():
    # h: 高度, x: 水平距離, LD: 揚抗比
    h = sp.symbols('h')
    LD = sp.symbols('LD')
    # 滑空の基本式: dx = LD * (-dh)
    # これを積分して水平距離 x を求める
    x_range = sp.integrate(LD, (h, 0, 30000)) 
    return sp.lambdify(LD, x_range, 'numpy')

# --- Step 2: Python による動的到達シミュレーション ---
def run_city_injection_sim(mass):
    # 解析解の取得
    calc_base_range = derive_gliding_range()
    
    # 滑空機の性能諸元
    L_D_ratio = 15.0  # 高性能滑空翼を想定
    v_stall = 60.0    # 失速速度 (m/s)
    
    # 理論上の最大滑空距離 (高度30kmからの無動力滑空)
    max_range_km = calc_base_range(L_D_ratio) / 1000.0
    
    # 大気密度変化を考慮した有効射出半径の補正
    # 質量増加(662kg)により、揚力維持に必要な速度が上がり、実質的な滑空比が微減するモデル
    efficiency_loss = (mass - 500) / 1000  # 500kg超過分による効率低下
    effective_range = max_range_km * (1 - efficiency_loss)

    print(f"--- #53 Inter-city Gliding Injection Results ---")
    print(f"Input Capsule Mass   : {mass:.2f} kg")
    print(f"Theoretical Max Range: {max_range_km:.2f} km")
    print(f"Mass-Adjusted Radius : {effective_range:.2f} km")
    print(f"Coverage Area        : {np.pi * effective_range**2 / 1e6:.2f} million km^2")
    
    return effective_range

if __name__ == "__main__":
    current_mass = 662.13 # #34bの結果を継承
    radius = run_city_injection_sim(current_mass)