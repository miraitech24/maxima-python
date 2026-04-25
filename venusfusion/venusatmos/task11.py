#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 15:22:50 2026

@author: iwamura
"""

import numpy as np
import re

# 1. Maximaから理論式をインポート
with open("formula_11.txt", "r") as f:
    formula_raw = re.sub(r'<[^>]+>', '', f.read()).strip()
    formula_py = formula_raw.replace("^", "**").replace("log", "np.log")

# 2. 統計的な力仕事 (1000回の試行)
trials = 1000
p_base = 90.0  # 基本気圧
d_base = 1000.0 # 雲までの距離
success_count = 0

print("Simulating 1000 lightning strikes with atmospheric turbulence...")

for _ in range(trials):
    # 気圧と距離にランダムなゆらぎ(不足分)を与える
    p = p_base + np.random.normal(0, 5) 
    d = d_base + np.random.normal(0, 100)
    x = (p/1013.25) * (d/100) # 単位換算
    
    # Maximaの式で判定
    v_critical = eval(formula_py, {"np": np, "x": x})
    v_actual = 5e6 + np.random.normal(0, 1e6) # 雷雲の電圧変動
    
    if v_actual > v_critical:
        success_count += 1

print(f"Simulation Complete. Lightning Capture Rate: {success_count/trials*100:.2f}%")