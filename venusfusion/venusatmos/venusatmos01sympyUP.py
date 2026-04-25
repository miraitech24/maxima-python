#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 13:26:52 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def run_venus_isru_analysis():
    # 1. SymPyによる解析解の導出
    z = sp.symbols('z', real=True)
    C = sp.Function('C')
    D_sym, v_sym, S_sym, C0_sym, dC0_sym = sp.symbols('D v S C0 dC0', real=True)

    # 移流拡散方程式の定義
    ode = D_sym * C(z).diff(z, z) - v_sym * C(z).diff(z) + S_sym
    
    # 境界条件設定: C(0)=C0, C'(0)=dC0
    ics = {C(0): C0_sym, C(z).diff(z).subs(z, 0): dC0_sym}
    sol_ivp = sp.dsolve(ode, C(z), ics=ics)
    
    # NumPy高速計算用に変換
    func_C = sp.lambdify((z, D_sym, v_sym, S_sym, C0_sym, dC0_sym), sol_ivp.rhs, "numpy")

    # 2. 数値シミュレーション実行
    altitudes = np.linspace(0, 100, 500) # 高度0-100km
    params = {
        'D': 0.85,    # 拡散係数
        'v': 0.32,    # 上昇気流速度 [m/s]
        'S': -0.012,  # 抽出による消費
        'C0': 1.0,    # 地表濃度基準
        'dC0': 0.04   # 地表フラックス
    }

    try:
        # 計算実行
        concentration = func_C(altitudes, params['D'], params['v'], params['S'], params['C0'], params['dC0'])
        
        # 最大濃縮地点の特定
        peak_idx = np.argmax(concentration)
        peak_alt = altitudes[peak_idx]
        max_val = concentration[peak_idx]

        print(f"=== 重水素分布解析結果 (#1) ===")
        print(f"解析解 C(z) = {sol_ivp.rhs}")
        print(f"最大濃縮高度: {peak_alt:.2f} km")
        print(f"ピーク相対濃度: {max_val:.4f}")

        # 可視化
        plt.figure(figsize=(6, 8))
        plt.plot(concentration, altitudes, lw=2, label='Deuterium Concentration')
        plt.axhline(peak_alt, color='r', ls='--', label=f'Extraction Target: {peak_alt:.1f}km')
        plt.xlabel('Relative Concentration')
        plt.ylabel('Altitude (km)')
        plt.title('Venus Atmospheric ISRU Profile (#1)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()

        if max_val > 1.1:
            print("判定: 特定高度での濃縮を確認。燃料自給システムの運用は可能です。")
        else:
            print("判定: 濃縮度が不十分。#26テスラ送電による局所励起が必要です。")

    except Exception as e:
        print(f"計算エラー: {e}")

if __name__ == "__main__":
    run_venus_isru_analysis()