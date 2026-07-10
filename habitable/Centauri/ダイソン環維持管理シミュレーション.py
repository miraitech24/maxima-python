#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:20:20 2026

@author: iwamura
"""

# Python: ダイソン環の経年劣化と維持コスト

import numpy as np
import matplotlib.pyplot as plt

# パラメータ
years = np.arange(0, 10000, 10)
degradation_rate = 0.001  # 年間0.1%の劣化
repair_capacity = 0.0008  # 年間0.08%の修復能力（自己複製ロボット）

# 状態のシミュレーション
state = np.zeros_like(years)
state[0] = 1.0  # 初期状態100%

for i in range(1, len(years)):
    degradation = degradation_rate * state[i-1]
    repair = repair_capacity * state[i-1]
    state[i] = state[i-1] - degradation + repair

    # 修復能力が劣化を上回れば、永遠に維持可能
    if repair_capacity >= degradation_rate:
        state[i] = min(state[i], 1.0)  # 100%以上にはならない

print(f"年間劣化率: {degradation_rate*100:.2f}%")
print(f"年間修復率: {repair_capacity*100:.2f}%")
print(f"修復が劣化を上回る: {repair_capacity >= degradation_rate}")

if repair_capacity >= degradation_rate:
    print("→ ダイソン環は事実上永遠に維持可能")
else:
    print(f"→ {years[np.where(state < 0.5)[0][0]]}年後に50%以下に低下")