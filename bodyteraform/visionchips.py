#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 16:10:29 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# 引数処理: python visionchips.py [V0] [lambda] [x_max]
v0 = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
lam = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
xmax = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0

# Maximaが作成したモジュールをインポート
if not os.path.exists("formula_module.py"):
    print("Error: Run Maxima script first.")
    sys.exit(1)

import formula_module

# 計算
x = np.linspace(0, xmax, 200)
# 正確にカッコが閉じた関数を呼び出し
y = [formula_module.get_voltage(xi, lam, v0) for xi in x]

# 可視化

plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f"V0={v0}mV, λ={lam}mm", color='cyan', lw=2)
plt.fill_between(x, y, color='cyan', alpha=0.1)
plt.title("Bio-Interface: Neural Signal Terraforming")
plt.xlabel("Distance x (mm)")
plt.ylabel("Potential V (mV)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()