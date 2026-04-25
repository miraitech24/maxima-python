#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 13:36:26 2026

@author: iwamura
"""

import numpy as np
import re

# 1. Maximaからの式読み込み
with open("formula_11_v2.txt", "r") as f:
    # 完全にタグや空白を排除
    formula_raw = re.sub(r'<[^>]+>', '', f.read()).strip()
    formula_py = formula_raw.replace("log", "np.log")

# 2. 金星地表パラメータでの評価 (不足分を補完)
P = 90.0   # 90気圧
A = 15.0   # 金星大気成分による定数(仮)
B = 360.0  # 金星大気成分による定数(仮)
gma = 0.1  # 二次電子放出係数
d = 1000.0 # 雲間距離(m)

# 計算実行
E_crit = eval(formula_py)
print(f"金星地表での絶縁破壊電界強度閾値: {E_crit:.2f} V/m")