#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 22:05:19 2026

@author: iwamura
"""

# #1007 Python数値計算セクション
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import importlib

# 実行ディレクトリをパスに追加
sys.path.append(os.getcwd())

def run_simulation():
    # Maxima出力ファイルのロード
    if not os.path.exists("penrose_params.py"):
        print("Error: penrose_params.py が存在しません。先に Maxima を実行してください。")
        return

    import penrose_params
    importlib.reload(penrose_params)

    # パラメータ設定: スピン a/M (0 to 0.999)
    M = 1.0
    a_values = np.linspace(0, 0.999, 100)
    
    # 利得計算
    try:
        gains = [penrose_params.get_max_gain(M, a) for a in a_values]
    except Exception as e:
        print(f"Calculation Error: {e}")
        return

    # 結果の可視化
    plt.figure(figsize=(10, 6))
    plt.plot(a_values, gains, label='Max Theoretical Gain', color='#6200ee', lw=2.5)
    plt.fill_between(a_values, gains, color='#6200ee', alpha=0.1)
    
    plt.title("Black Hole Energy Extraction Simulation (#1007)")
    plt.xlabel("Dimensionless Spin (a/M)")
    plt.ylabel("Maximum Energy Gain (%)")
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    
    plt.savefig("penrose_simulation_result.png")
    print("シミュレーション完了: penrose_simulation_result.png を保存しました。")

if __name__ == "__main__":
    run_simulation()

