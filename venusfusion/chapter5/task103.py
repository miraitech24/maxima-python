#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 15:19:16 2026

@author: iwamura
"""

# task103.py
import numpy as np
import matplotlib.pyplot as plt

def run_ultimate_shift_sim():
    years = np.linspace(0, 800, 801)
    # 拠点増殖を加速：20年倍増、300年で865拠点到達
    nodes = np.array([min(2**(y / 20), 865) for y in years])
    
    L_ATM = 2.905e29
    T_INIT = 737.0  # 463.8 degC
    momentum = np.zeros(len(years))
    temp = np.zeros(len(years))
    
    momentum[0] = L_ATM
    temp[0] = T_INIT
    
    # 【極重要】制動係数をさらに3桁強化 (10^24オーダー)
    # 拠点が単なる点ではなく、大気循環の「ハブ」として全大気に干渉する想定
    B_BASE = 5.0e24 

    for i in range(1, len(years)):
        # 1. 密度フィードバック：冷えるほど制動力が指数的に強化
        density_fb = (T_INIT / temp[i-1])**8.0
        
        # 2. 制動力：運動量に対する強い負の相関
        braking = nodes[i] * B_BASE * (momentum[i-1] / L_ATM)**0.3 * density_fb
        momentum[i] = max(momentum[i-1] - braking, 1e-10)
        
        # 3. 冷却の相転移：SRが落ちるほど「温室効果の蓋」が指数関数的に吹き飛ぶ
        sr_ratio = momentum[i] / L_ATM
        # 目標温度 (理論限界)
        t_target = T_INIT * (sr_ratio**0.25)
        
        # 4. 指数的な排熱加速：風速低下が10%を超えると冷却効率が100倍速に加速
        # ステファン・ボルツマン則を模した排熱効率の動的変化
        cooling_speed = 0.05 * np.exp(5.0 * (1.0 - sr_ratio))
        
        # 温度更新
        diff = (temp[i-1] - t_target) * cooling_speed
        temp[i] = max(temp[i-1] - diff, 288.15)

    # 描画
    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    
    ax1.plot(years, momentum/L_ATM*100, 'r-', label='SR Velocity (%)', lw=2)
    ax1.set_ylabel('SR Velocity (%)', color='r')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right')
    
    ax3.plot(years, temp - 273.15, 'orange', label='Temp (degC)', lw=2)
    ax3.set_ylabel('Temperature (degC)', color='orange')
    ax3.axhline(y=50, color='blue', linestyle='--', label='Target 50C')
    ax3.set_xlabel('Years')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper right')

    plt.suptitle('Venus Terraforming: 600-Year Breakthrough Model (#103)')
    plt.show()

    goal_indices = np.where((temp - 273.15) <= 50)[0]
    goal_year = years[goal_indices[0]] if len(goal_indices) > 0 else "Not Reached"

    print(f"--- #103 最終見通し報告（臨界突破版） ---")
    print(f"50度到達予測: {goal_year} 年")
    print(f"300年時点の気温: {temp[300]-273.15:.1f} degC")
    print(f"500年時点の気温: {temp[500]-273.15:.1f} degC")
    print(f"600年時点の気温: {temp[600]-273.15:.1f} degC")

if __name__ == "__main__":
    run_ultimate_shift_sim()