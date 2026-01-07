#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 12:59:14 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import importlib
import maxima_output

# 数式をリロード
importlib.reload(maxima_output)

def plot_venus_grid():
    # パラメータ設定
    Q_val = 2000 
    r_coil = 10.0
    distances = np.linspace(1, 500, 500)
    
    efficiencies = []
    for d in distances:
        # 結合係数 k (距離の3乗に反比例)
        k = (r_coil**3) / (d**3 + r_coil**3)
        # Maximaの数式を呼び出し
        try:
            eff = maxima_output.get_eta_formula(k, Q_val, Q_val)
            efficiencies.append(eff)
        except TypeError:
            # 万が一置換が漏れていた場合のデバッグ用
            print("Error: Still using '^' in maxima_output.py. Check the file.")
            return

    # グラフ描画
    plt.figure(figsize=(8, 5))
    plt.plot(distances, efficiencies, lw=2)
    plt.title("Venus Tesla-Grid: Efficiency vs Distance (Fixed)")
    plt.xlabel("Distance (m)")
    plt.ylabel("Efficiency (0.0 - 1.0)")
    plt.grid(True)
    plt.show()

plot_venus_grid()