#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 13:16:22 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Maximaが生成したファイルをインポート
try:
    from tether_params import get_t_max
except SyntaxError:
    print("Error: Maxima output contains invalid tags. Check tether_params.py")
    raise

def solve_issue_100():
    # 設計定数 (CNT複合材)
    L, rho, sigma_allow = 1000.0, 1700.0, 3.5e9
    A = 0.000058  # 質量 98.6kg (100kg制限内)
    
    # 航行プロファイル
    time = np.linspace(0, 3600, 100)
    accel_profile = np.linspace(50, 90, 100)      # 5G -> 9G
    payload_profile = np.linspace(1000, 800, 100) # 燃料消費
    
    sf_history = []
    for a, m_p in zip(accel_profile, payload_profile):
        t_max = get_t_max(a, m_p, L, rho, A)
        sf = sigma_allow / (t_max / A)
        sf_history.append(sf)

    # 安全率推移の可視化
    
    plt.figure(figsize=(8, 4))
    plt.plot(time, sf_history, label="Dynamic Safety Factor", lw=2)
    plt.axhline(y=3.0, color='r', ls='--', label="Requirement (S=3.0)")
    plt.fill_between(time, sf_history, 3.0, where=(np.array(sf_history) < 3.0), color='red', alpha=0.2)
    plt.title("Tether Durability Analysis (Issue #100)")
    plt.xlabel("Mission Time (s)"); plt.ylabel("Safety Factor S"); plt.legend(); plt.grid(True)
    plt.show()

    print(f"Total Tether Mass: {rho * A * L:.2f} kg")
    print(f"Minimum Safety Factor: {min(sf_history):.2f}")

if __name__ == "__main__":
    solve_issue_100()