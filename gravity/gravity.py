#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 12:34:54 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess

def run_gravity_coupling():
    print("Step 1: Maximaによる重力場の解析...")
    subprocess.run(["maxima", "-b", "gravity.mac"], capture_output=True)

    print("Step 2: 時空の歪みデータのインポート...")
    with open("gravity_result.txt", "r") as f:
        g_time_raw = f.read()
    
    # Python形式に変換
    # Maximaの変数はそのまま、数値計算用にラムダ関数化
    g_time_func = lambda r: eval(g_time_raw.replace("^", "**"), {"r": r})

    print("Step 3: 重力による時間の遅れ（GPS補正の原理）の可視化...")
    r_axis = np.linspace(1.5, 10, 100) # 天体からの距離
    time_dilation = [np.sqrt(-g_time_func(r)) for r in r_axis]

    plt.figure(figsize=(10, 6))
    plt.plot(r_axis, time_dilation, color='red', label="Time Flow Rate")
    plt.axhline(1.0, color='black', linestyle='--', label="Flat Spacetime (Normal Time)")
    plt.title("General Relativity: Time Dilation near Mass")
    plt.xlabel("Distance from Center (r)")
    plt.ylabel("Rate of Time Flow")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    print("天体に近づくほど、時間の進みが遅くなっていることが確認できます。")

if __name__ == "__main__":
    run_gravity_coupling()