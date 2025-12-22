#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 11:20:49 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess

def run_coupling():
    print("--- Step 1: Maximaによる代数計算の実行 ---")
    subprocess.run(["maxima", "-b", "geometry.mac"], capture_output=True)

    print("--- Step 2: 計算結果のインポートと置換 ---")
    with open("result_tensor.txt", "r") as f:
        data_str = f.read()
    
    # Python用に記号を置換
    # 1. sin -> np.sin
    # 2. ^ (Maximaのべき乗) -> ** (Pythonのべき乗)
    data_str = data_str.replace("sin", "np.sin").replace("^", "**")
    
    theta_val = np.pi / 4 
    
    # 安全に評価
    try:
        ricci_components = eval(data_str, {"np": np, "theta": theta_val})
        print(f"theta={theta_val:.2f} におけるリッチテンソル成分: {ricci_components}")
    except Exception as e:
        print(f"Eval Error: {e}")
        return

    print("--- Step 3: リッチフローの可視化 ---")
    times = np.linspace(0, 0.4, 50)
    g22_initial = np.sin(theta_val)**2
    R22 = ricci_components[1]
    
    # リッチフロー: g(t) = g(0) - 2 * R * t
    g22_history = [max(0, g22_initial - 2 * R22 * t) for t in times]

    plt.figure(figsize=(10, 5))
    plt.plot(times, g22_history, 'b-', label=r"Metric $g_{\phi\phi}$ (Size of circle at $\theta$)")
    plt.axhline(0, color='red', linestyle='--', label="Singularity (Shrunk to point)")
    plt.title("Ricci Flow: How the manifold smooths/shrinks")
    plt.xlabel("Flow Time ($t$)")
    plt.ylabel("Metric Value")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_coupling()