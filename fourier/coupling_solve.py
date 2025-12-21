#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 21 14:05:31 2025

@author: iwamura
"""

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
import os
import re

def main():
    filename = "result.txt"
    if not os.path.exists(filename):
        print(f"Error: {filename} が見つかりません。")
        return

    # 1. Maximaからの引き渡しファイル読み込み
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()
            
            # 正規表現で数値(小数点、マイナス含む)以外をすべて除去
            clean_val = re.findall(r"[-+]?\d*\.\d+|\d+", content)
            
            if not clean_val:
                raise ValueError(f"数値が見つかりません。ファイル内容: '{content}'")
            
            maxima_res = float(clean_val[0])
    except Exception as e:
        print(f"数値変換エラー。詳細: {e}")
        return

    # 2. Pythonによる数値的補完（数値積分）
    a, b = 1.0, 2.0
    func = lambda x: np.exp(-a * x**2) * np.cos(b * x)
    python_res, _ = quad(func, 0, np.inf)

    # 3. 結果の比較表示 
    print("=" * 45)
    print(f"Maxima 解析解 (from file): {maxima_res}")
    print(f"Python 数値積分結果:      {python_res}")
    print(f"絶対誤差:                {abs(maxima_res - python_res)}")
    print("=" * 45)

    # 4. 可視化
    x = np.linspace(0, 5, 500)
    plt.figure(figsize=(9, 4))
    plt.plot(x, func(x), label=r'$e^{-ax^2}\cos(bx)$', color='teal')
    plt.fill_between(x, func(x), color='teal', alpha=0.15)
    plt.title(f"Integral Verification: Maxima vs Python")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()