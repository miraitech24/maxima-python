#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 12:24:13 2026

@author: iwamura
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import sys

def run_coupling_analysis(M0_val=100000, fuel_ratio=0.5, days=14):
    # --- 1. SymPy 変数定義 ---
    t = sp.symbols('t', real=True, positive=True)
    M_0, F_max, Isp, g_0 = sp.symbols('M_0 F_max Isp g_0', real=True, positive=True)
    
    ve = Isp * g_0
    mdot = F_max / ve
    
    # --- 2. 物理パラメータ設定 ---
    p_val = {F_max: 4669, Isp: 3000, g_0: 9.80665, M_0: M0_val}
    mdot_val = float(mdot.subs(p_val))
    M_fuel = M0_val * fuel_ratio
    t_empty = M_fuel / mdot_val
    T_end = days * 24 * 3600

    # --- 3. フェーズ分離計算 (SymPy沼回避) ---
    # 加速フェーズの速度と距離の式
    v_acc_expr = ve * sp.log(M_0 / (M_0 - mdot * t))
    # 積分範囲を [0, t] に限定し、t_emptyを超えないように数値評価する
    d_acc_expr = sp.integrate(v_acc_expr, (t, 0, t))

    # 数値評価用の関数生成
    v_func = sp.lambdify(t, v_acc_expr.subs(p_val), 'numpy')
    d_func = sp.lambdify(t, d_acc_expr.subs(p_val), 'numpy')

    # 境界値の確定
    t_acc_limit = min(t_empty, T_end)
    v_max = float(v_func(t_acc_limit))
    d_acc_total = float(d_func(t_acc_limit))

    # 慣性航行フェーズの計算
    t_inertial = max(0, T_end - t_empty)
    d_inertial = v_max * t_inertial
    d_total = d_acc_total + d_inertial

    # --- 4. 結果表示 ---
    print(f"--- 連成Step 2-5 最終解析結果 (SymPy/Non-Complex) ---")
    print(f"物理制約: 推力={p_val[F_max]}N, 初速=0m/s")
    print(f"燃料枯渇: {t_empty/86400:.2f} 日")
    print(f"最大速度: {v_max:,.2f} m/s")
    print(f"14日後の到達距離: {d_total/1e9:,.3f} million km")

    # 判定
    dist_threshold = 41.4 
    if (d_total / 1e6) < dist_threshold:
        print(f"\n【判定】NG: 距離不足。推力が低すぎて燃料枯渇後の慣性航行でも届きません。")
        print("対策: #41(電力)増強による推力制限緩和、または#14b(ハイドライド)の高密度化。")
    else:
        print(f"\n【判定】OK: 航行成立。データを #47b (ROI) へ引き渡します。")

    # --- 5. グラフ描画 ---
    t_plot = np.linspace(0, T_end, 500)
    # 燃料切れ以降は速度を一定に固定（ベクトル演算）
    v_plot = np.piecewise(t_plot, [t_plot <= t_empty, t_plot > t_empty], 
                          [lambda x: v_func(x), v_max])

    plt.figure(figsize=(10, 5))
    plt.plot(t_plot / 86400, v_plot, label="Velocity (m/s)", lw=2)
    plt.axvline(x=t_empty/86400, color='orange', linestyle='--', label="Fuel Empty")
    plt.title("Step 5: Navigation Profile (Fixed Discontinuity)")
    plt.xlabel("Time [days]")
    plt.ylabel("Velocity [m/s]")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # 引数: 質量, 燃料比, 日数
    m = float(sys.argv[1]) if len(sys.argv) > 1 else 100000
    fr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
    d = int(sys.argv[3]) if len(sys.argv) > 3 else 14
    run_coupling_analysis(m, fr, d)