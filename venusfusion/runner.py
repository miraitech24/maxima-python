#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 14:14:12 2026

@author: iwamura
"""

import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import io

def run_maxima_analysis(heat_source_power, altitude_km):
    """
    Maximaを呼び出して、特定の排熱強度と高度における温度分布を計算する
    """
    # 高度に応じた簡易的な金星大気パラメータ（高度0〜50kmを想定）
    # 密度 rho = 65 * exp(-alt/15.9), 風速 v = 1 + alt*2 (簡易モデル)
    rho = 65.0 * (2.718 ** (-altitude_km / 15.9))
    v = 1.0 + altitude_km * 2.0 
    
    # Maximaへの命令（バッチモード実行）
    # 引数を変数として事前に定義し、transport.macを実行
    maxima_cmd = (
        f"S_const: {heat_source_power}; "
        f"rho: {rho}; "
        f"v: {v}; "
        f"load(\"transport.mac\");"
    )
    
    # Maximaプロセスの実行
    result = subprocess.run(
        ['maxima', '--very-quiet', '-r', maxima_cmd],
        capture_output=True, text=True
    )
    
    # result.dat から計算結果（例：緯度45度地点の温度上昇）を読み込む
    try:
        with open("result.dat", "r") as f:
            temp_at_mid_lat = float(f.read().strip())
        return temp_at_mid_lat
    except:
        return None

# --- メイン処理：高度別の排熱拡散シミュレーション ---
altitudes = [0, 10, 20, 30, 40, 50] # 高度(km)
powers = [1e12, 1e13, 1e14]         # 核融合炉の出力(W)

results = []

for p in powers:
    temp_profile = []
    for a in altitudes:
        t = run_maxima_analysis(p, a)
        temp_profile.append(t)
    results.append(temp_profile)

# --- 可視化 ---
plt.figure(figsize=(10, 6))
for i, p in enumerate(powers):
    plt.plot(altitudes, results[i], marker='o', label=f'Power: {p:.0e} W')

plt.title("Venus Atmospheric Heat Transport: Temp vs Altitude")
plt.xlabel("Altitude (km)")
plt.ylabel("Steady-state Temperature at 45° Lat (K)")
plt.grid(True)
plt.legend()
plt.show()