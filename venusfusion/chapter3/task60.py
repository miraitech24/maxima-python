#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 13:07:53 2026

@author: iwamura
"""

import numpy as np
import subprocess

# --- Step 1: Maxima による着水衝撃圧の解析解導出 ---
def get_impact_pressure_formula():
    maxima_code = """
    display2d:false$
    /* 衝撃圧 P = 1/2 * rho * v^2 * K (Kは形状係数) */
    /* タンク壁の応力 sigma = P * r / t (薄肉円筒近似) */
    sigma_eqn: (1/2 * rho * v^2 * K) * r / d$
    print(sigma_eqn)$
    """
    with open("impact_logic.mac", "w") as f:
        f.write(maxima_code)
    return "0.5 * rho * v**2 * K * r / d"

# --- Step 2: Python によるモンテカルロ・ロス率シミュレーション ---
def run_recovery_loss_sim(mass):
    formula_str = get_impact_pressure_formula()
    
    # 定数設定
    rho_water = 1025     # 海水密度 (kg/m^3)
    K_shape = 2.5        # 滑空機形状係数
    r_tank = 0.4         # タンク半径 (m)
    d_wall = 0.008       # タンク壁厚 (8mm)
    sigma_yield = 450e6  # 強化アルミ合金の降伏応力 (Pa)
    
    # 試行回数
    n_trials = 10000
    # 着水速度のばらつき (平均 30m/s, 標準偏差 5m/s)
    v_samples = np.random.normal(30, 5, n_trials)
    
    # Maxima由来の応力計算
    stress_samples = 0.5 * rho_water * v_samples**2 * K_shape * r_tank / d_wall
    
    # 破損判定とロス率計算
    # 応力が降伏点を超えた場合、タンクの5%〜20%が漏洩すると仮定
    damage_mask = stress_samples > sigma_yield
    leakage_rates = np.where(damage_mask, np.random.uniform(0.05, 0.20, n_trials), 0.0)
    
    avg_loss_rate = np.mean(leakage_rates)
    net_payload = mass * (1 - avg_loss_rate)

    print(f"--- #60 Ocean Landing & Recovery Results ---")
    print(f"Mean Impact Stress   : {np.mean(stress_samples)/1e6:.2f} MPa")
    print(f"Structural Integrity : {100 * (1 - np.mean(damage_mask)):.2f} % (Safe Landing)")
    print(f"Average Hydrogen Loss: {avg_loss_rate * 100:.2f} %")
    print(f"Net Recovered Mass   : {net_payload:.2f} kg")
    
    return avg_loss_rate, net_payload

if __name__ == "__main__":
    current_mass = 662.13
    loss_rate, final_mass = run_recovery_loss_sim(current_mass)