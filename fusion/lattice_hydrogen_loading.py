#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:50:05 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# =================================================================
# 1. 物理定数の設定
# =================================================================
H_BAR = 1.054e-34      # プランク定数
E_CHARGE = 1.602e-19   # 電荷
EPSILON_0 = 8.854e-12  # 真空の誘電率
M_D = 3.343e-27        # 重水素の質量
MU = M_D / 2           # 換算質量

# =================================================================
# 2. 核融合確率計算エンジン (WKB近似)
# =================================================================
def tunnel_probability(E_ev, screening_ev=0):
    """
    E_ev: 粒子のエネルギー (eV)
    screening_ev: 触媒（電子雲など）による障壁低下量 (eV)
    """
    E_total = (E_ev + screening_ev) * E_CHARGE
    if E_total <= 0: return 0
    
    velocity = np.sqrt(2 * E_total / MU)
    # ガモフ因子 (Gamow factor)
    eta = (E_CHARGE**2) / (4 * np.pi * EPSILON_0 * H_BAR * velocity)
    return np.exp(-2 * np.pi * eta)

# =================================================================
# 3. 触媒・構造による増幅シミュレーション
# =================================================================
def localized_field_enhancement(radius_nm, gap_nm):
    """ナノ粒子の尖端や隙間でどれだけ電界が強まるか"""
    return (radius_nm / gap_nm)**1.5

def energy_output_calc(prob, fuel_moles=1.0):
    """4D反応(47.6MeV)に基づいた期待エネルギー出力(MJ)"""
    AVOGADRO = 6.022e23
    energy_per_reaction_j = 47.6 * 1e6 * E_CHARGE
    # 簡易的な期待値計算 (反応率probに依存)
    return (fuel_moles * AVOGADRO) * prob * energy_per_reaction_j / 1e6

# =================================================================
# 4. メイン・シミュレーション実行
# =================================================================
if __name__ == "__main__":
    energies = np.logspace(-2, 4, 500) # 0.01eV ~ 10keV
    
    # シナリオ設定
    # A: 真空(標準物理) / B: 阪大モデル級遮蔽(300eV) / C: 未知の超触媒(800eV)
    p_normal = [tunnel_probability(e) for e in energies]
    p_arata_takahashi = [tunnel_probability(e, 300) for e in energies]
    p_frontier = [tunnel_probability(e, 800) for e in energies]

    # --- 可視化 ---
    plt.figure(figsize=(12, 7))
    plt.plot(energies, p_normal, label='Scenario A: Vacuum (Impossible)', color='red')
    plt.plot(energies, p_arata_takahashi, label='Scenario B: Pd-Lattice (Arata/Takahashi)', color='blue')
    plt.plot(energies, p_frontier, label='Scenario C: Targeted Catalyst (Goal)', color='gold', lw=3)
    
    plt.xscale('log')
    plt.yscale('log')
    plt.axvline(x=0.025, color='green', ls='--', label='Room Temp (300K)')
    plt.ylim(1e-100, 1)
    plt.title("Path to Artificial Sun: Required Screening for Realization")
    plt.xlabel("Input Energy (eV)")
    plt.ylabel("Tunneling Probability")
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    plt.show()

    # --- 実用化への数値出力 ---
    print("--- 実用化シミュレーション結果 ---")
    prob_goal = tunnel_probability(0.025, 800)
    print(f"目標触媒下での常温反応確率: {prob_goal:.2e}")
    
    output_mj = energy_output_calc(prob_goal, fuel_moles=0.01) # わずか0.02gの重水素
    print(f"微量燃料からの期待出力: {output_mj:.2e} MJ")
    print(f"これはガソリン約 {output_mj/35:.2e} リットル分に相当します。")