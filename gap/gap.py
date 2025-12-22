#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 20:47:49 2025

@author: iwamura
"""

# 自然の「知ったこっちゃない」を反映したシミュレーション
import numpy as np
import matplotlib.pyplot as plt

def realistic_universe():
    r = np.logspace(-2, 2, 400)

    # 領域によって「勝手に」切り替わる法則
    # つなぎ目は人間が困るだけで、自然は「この場合はこう」と決めている
    def physical_reality(radius):
        if radius < 0.5:
            # ミクロ：量子力学的な振る舞い
            return 1 / (radius**2 + 0.1) 
        else:
            # マクロ：相対論的な重力
            return 1 / radius**2

    forces = [physical_reality(val) for val in r]

    plt.figure(figsize=(10, 6))
    plt.loglog(r, forces, color='black', lw=2, label='Actual Phenomenon')
    plt.axvline(x=0.5, color='red', linestyle=':', label='The "Gap" Humans Worry About')

    plt.title("Reality: Laws just 'are' what they 'are'")
    plt.xlabel("Scale (Distance)")
    plt.ylabel("Observed Strength")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    print("自然は赤線の境界で『つなぎ目が…』なんて悩みません。")
    print("『この場合はこうなる』という現実がそこにあるだけです。")

realistic_universe()