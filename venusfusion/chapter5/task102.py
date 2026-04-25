#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 13:55:12 2026

@author: iwamura
"""

# task102.py
import numpy as np
import matplotlib.pyplot as plt
import os

# #101からのパラメータ継承
params = {}
if os.path.exists("task101_params.py"):
    with open("task101_params.py") as f:
        exec(f.read(), params)
else:
    params = {'L_ATM': 2.905e29, 'R_EFF': 94.49, 'P_SUN': 7.219e16}

# 設定定数
TARGET_NODES = 865
YEARS = 300
GENERATIONS = 10
GEN_TIME = YEARS / GENERATIONS # 1世代30年

def simulate_growth():
    t = np.linspace(0, YEARS, 301)
    # 30年ごとに倍増する自己増殖モデル (2^(t/30))
    nodes = 2**(t / GEN_TIME)
    nodes = np.minimum(nodes, TARGET_NODES) # 865で飽和
    
    # 拠点増加に伴う「大気の網」の密度 (有効面積比)
    r_v = 6.052e6
    surface_area = 4 * np.pi * r_v**2
    # 1拠点の制動影響範囲を拡大解釈（随伴流R_EFF*1000）
    effective_area_per_node = np.pi * (params['R_EFF'] * 1000)**2 
    coverage = (nodes * effective_area_per_node) / surface_area

    # グラフ作成
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Years from Hesperus Arrival')
    ax1.set_ylabel('Number of LENR Nodes', color=color)
    ax1.plot(t, nodes, color=color, lw=3, label='Node Growth')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Planetary Coverage (%)', color=color)
    ax2.plot(t, coverage * 100, color=color, linestyle='--', label='Braking Coverage')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 100)

    plt.title('Infrastructure Expansion Roadmap (#102b)')
    fig.tight_layout()
    plt.savefig('task102_growth.png')
    plt.show()
    
    # 世代ごとのマイルストーン出力
    print(f"--- #102 インフラ展開シミュレーション結果 ---")
    print(f"Generation 5 (150yr): {2**5:.0f} nodes")
    print(f"Final Target (300yr): {nodes[-1]:.0f} nodes reached.")
    print(f"Final Coverage: {coverage[-1]*100:.1f}% of Venus surface.")

if __name__ == "__main__":
    simulate_growth()