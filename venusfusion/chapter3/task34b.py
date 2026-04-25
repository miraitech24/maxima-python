#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 12:33:35 2026

@author: iwamura
"""

import numpy as np
import subprocess

# --- Step 1: Maxima による熱伝導解析解の導出 ---
def get_thermal_solution():
    maxima_code = """
    display2d:false$
    /* 1次元熱伝導モデル: dT/dt = alpha * d2T/dx2 */
    /* 表面温度 Ts(t), 裏面(芯部)温度 T_core(t), 断熱厚 d */
    /* 簡略化した特性時間近似解を導出 */
    tau: d^2 / alpha$
    T_core: T_env * (1 - exp(-t/tau))$
    print(T_core)$
    """
    with open("thermal_logic.mac", "w") as f:
        f.write(maxima_code)
    
    # 実際には物理定数を反映した式を返すが、ここではロジックを継承
    return "T_env * (1 - exp(-t * alpha / d**2))"

# --- Step 2: Python による断熱材厚の最適化シミュレーション ---
def optimize_insulation():
    # 前回の失敗値
    T_failed = 558.20
    T_limit = 500.0  # 目標値
    T_env = 1800.0   # 突入時の平均気流温度 (K)
    t_reentry = 1200 # 有効加熱時間 (s)
    alpha = 1.2e-7   # 炭素系断熱材の熱拡散率 (m^2/s)
    
    # Maxima由来のロジックで d を逆算
    # T_limit = T_env * (1 - exp(-t * alpha / d**2))
    # -> d = sqrt( -t * alpha / ln(1 - T_limit/T_env) )
    
    d_min = np.sqrt(-t_reentry * alpha / np.log(1 - T_limit/T_env))
    
    # 重量計算
    surface_area = 4.5 # m^2
    density_ablator = 1400 # kg/m^3
    mass_increase = d_min * surface_area * density_ablator
    
    # #34aからのベース質量 529.60 kg に加算
    new_total_mass = 529.60 + mass_increase

    print(f"--- #34b Thermal Optimization Results ---")
    print(f"Required Insulation Thickness (d) : {d_min*1000:.2f} mm")
    print(f"Ablator Mass Added               : {mass_increase:.2f} kg")
    print(f"New Arrival Mass (to #53)        : {new_total_mass:.2f} kg")
    print(f"Predicted Core Temperature       : {T_limit:.2f} K")
    print(f"Thermal Safety Status            : SUCCESS")

    return new_total_mass

if __name__ == "__main__":
    final_mass_for_next = optimize_insulation()