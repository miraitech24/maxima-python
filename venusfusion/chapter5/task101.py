#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 13:28:44 2026

@author: iwamura
"""

# task101.py
import matplotlib.pyplot as plt
import numpy as np
import os

# Maximaの出力ファイルを辞書として読み込み
params = {}
if os.path.exists("task101_params.py"):
    with open("task101_params.py") as f:
        exec(f.read(), params)
else:
    params = {'L_ATM': 2.904e29, 'R_EFF': 3110.5, 'P_SUN': 1.54e17}

# 辞書から変数へ展開
L_ATM = params.get('L_ATM')
R_EFF = params.get('R_EFF')
P_SUN = params.get('P_SUN')

def analyze_physics():
    print(f"--- #101 物理基盤確定結果 ---")
    print(f"L_ATM (総角運動量): {L_ATM:.3e} kg·m²/s")
    print(f"R_EFF (有効制動半径): {R_EFF:.2f} m")
    print(f"P_SUN (利用可能太陽電力): {P_SUN:.3e} W")
    
    # 制動ポテンシャルの可視化
    nodes = np.arange(1, 1001)
    surface_area = 4 * np.pi * (6.052e6)**2
    # 拠点の干渉断面積を大気層の抵抗としてモデル化
    interference = 1 - np.exp(-nodes * (np.pi * R_EFF**2 * 1e5) / surface_area) 
    
    plt.figure(figsize=(10, 6))
    plt.plot(nodes, interference * 100, color='blue', lw=2, label='Braking Interference %')
    plt.axvline(x=865, color='red', linestyle='--', label='Final Nodes: 865')
    plt.title('Venus Atmospheric Braking Potential (#101c)')
    plt.xlabel('Number of 10TW Nodes')
    plt.ylabel('Interference Efficiency (%)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('task101_summary.png')
    plt.show() # %runでのグラフ表示用
    print("Graph saved as task101_summary.png")

if __name__ == "__main__":
    analyze_physics()