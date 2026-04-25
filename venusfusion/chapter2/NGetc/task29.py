#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 11:03:19 2026

@author: iwamura
"""

# task29.py
import numpy as np
import matplotlib.pyplot as plt
import os, sys, math

# 自作モジュールのパスを通す
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import orbit_params

def run_simulation():
    # 射出速度 v0 [m/s] のスイープ
    v0_list = np.linspace(1000, 5000, 400)
    gamma_fixed = math.radians(-12.5) # 射出角 [rad]
    
    results = []
    for v0 in v0_list:
        mu, r0, re = orbit_params.MU, orbit_params.R0, orbit_params.RE
        e = orbit_params.calc_e(v0, gamma_fixed, mu, r0)
        p = (orbit_params.calc_h(v0, gamma_fixed, r0)**2) / mu
        
        # 地球に到達（近地点半径 < 地球半径）する場合のみ計算
        if p / (1 + e) <= re:
            # 界面での真近点離角
            cos_phi = (p / re - 1) / e
            phi_e = math.acos(max(-1, min(1, cos_phi)))
            # 突入角 (Flight Path Angle) [deg]
            fpa = math.degrees(math.atan2(e * math.sin(phi_e), 1 + e * math.cos(phi_e)))
            results.append([v0, fpa])

    if not results: return
    data = np.array(results)

    # グラフ描画
    plt.figure(figsize=(10, 6))
    plt.plot(data[:, 0], data[:, 1], color='navy', label='Calculated Entry Angle')
    
    # 安全圏 (Entry Corridor) の明示
    plt.axhspan(-7.5, -5.5, color='orange', alpha=0.3, label='Safe Entry Corridor (-5.5° to -7.5°)')
    plt.axhline(-7.5, color='red', linestyle='--', linewidth=1)
    plt.axhline(-5.5, color='red', linestyle='--', linewidth=1)
    
    plt.title("Capsule Entry Angle Sensitivity Analysis")
    plt.xlabel("Injection Velocity $v_0$ [m/s]")
    plt.ylabel("Entry Flight Path Angle $\gamma_e$ [deg]")
    plt.grid(True, which='both', linestyle=':', alpha=0.7)
    plt.legend(loc='upper right')
    plt.show()

if __name__ == "__main__":
    run_simulation()