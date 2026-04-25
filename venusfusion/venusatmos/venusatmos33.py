#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 12:19:20 2026

@author: iwamura
"""

import numpy as np
import sys
import os
import matplotlib.pyplot as plt

# Maxima成果物のインポート
if os.path.exists("model_export.py"):
    import model_export
else:
    print("Error: model_export.py not found.")
    sys.exit(1)

def run_coupling_retry(M0=100000, fuel_ratio=0.5, days=14):
    # 物理定数
    F_max = 4669
    Isp = 3000
    g0 = 9.80665
    ve = Isp * g0
    mdot = F_max / ve
    T_end = days * 24 * 3600
    
    # 燃料枯渇の判定
    M_fuel = M0 * fuel_ratio
    t_empty = M_fuel / mdot
    
    # 最終ステータスの計算
    if T_end <= t_empty:
        # 14日経っても燃料が残っている場合
        v_final = model_export.get_v_acc(M0, T_end, mdot, ve)
        d_final = model_export.get_d_acc(M0, T_end, mdot, ve)
    else:
        # 途中で燃料が尽きる場合
        v_max = model_export.get_v_acc(M0, t_empty, mdot, ve)
        d_acc_end = model_export.get_d_acc(M0, t_empty, mdot, ve)
        # 慣性航行距離を加算
        d_final = d_acc_end + v_max * (T_end - t_empty)
        v_final = v_max

    print(f"--- 連成Step 2-5 実行結果 ---")
    print(f"燃料枯渇まで: {t_empty/3600/24:.2f} 日")
    print(f"最終速度: {v_final:,.2f} m/s")
    print(f"14日後の到達距離: {d_final/1e9:,.3f} million km")
    
    # 判定
    dist_threshold = 41.4 # M km
    if (d_final/1e6) < dist_threshold:
        print("\n【判定】NG: 到達不可。推力(#56)または燃料比(#14b)の強化が必要です。")
    else:
        print("\n【判定】OK: 航行成立。ROI計算へ。")

    # グラフ描画（不連続な速度変化を可視化）
    t_plot = np.linspace(0, T_end, 500)
    v_plot = [model_export.get_v_acc(M0, ti, mdot, ve) if ti <= t_empty else v_final for ti in t_plot]
    
    plt.figure(figsize=(8, 4))
    plt.plot(t_plot/86400, v_plot, label="Velocity Profile")
    plt.axvline(x=t_empty/86400, color='r', linestyle='--', label="Fuel Empty")
    plt.xlabel("Days"); plt.ylabel("m/s"); plt.legend(); plt.grid(True)
    plt.show()

if __name__ == "__main__":
    m_val = float(sys.argv[1]) if len(sys.argv) > 1 else 100000
    fr_val = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    run_coupling_retry(m_val, fr_val)