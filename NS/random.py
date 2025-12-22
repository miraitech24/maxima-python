#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 21:42:11 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

def visualize_infinite_solutions():
    # 空間の定義
    nx = 100
    x = np.linspace(0, 1, nx)
    
    plt.figure(figsize=(10, 6))
    
    # 50回、同じ条件（のつもり）で計算を実行
    for i in range(50):
        # 初期状態は「ほぼ」同じだが、境界に目に見えない乱数を混ぜる
        u = np.exp(-0.5 * ((x - 0.5) / 0.1)**2) 
        u += np.random.normal(0, 0.05, nx) # 宇宙のノイズ（乱数）
        
        # 簡易的な流体（NS方程式の核）の進展
        # 数値計算の過程で乱数が自己増幅していく
        for _ in range(30):
            u[1:-1] = u[1:-1] - 0.1 * u[1:-1] * (u[1:-1] - u[:-2])
            
        # 実行のたびに変わる「無数の解」を薄く重ねる
        plt.plot(x, u, color='cyan', alpha=0.15)

    # 最後に、学者が「これが正解だ」と信じている平均的な線を一本引く
    plt.plot(x, np.exp(-0.5 * ((x - 0.5) / 0.1)**2), color='red', lw=2, label='Academic Ideal')

    plt.title("The Reality: Infinite Divergent Solutions")
    plt.xlabel("Space (Boundary Conditions with Randomness)")
    plt.ylabel("Velocity / State")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()

    print("赤線（理論上の解）の周りに広がる青い霧のようなものが、現実の『無数の解』です。")
    print("実行するたびに、この霧の形は変わります。同じ流れなど、二度と現れません。")

if __name__ == "__main__":
    visualize_infinite_solutions()