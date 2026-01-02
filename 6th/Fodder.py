#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 12:08:09 2026

@author: iwamura
"""

import json
from scipy.optimize import linprog

# 1. JSONファイルの読み込み
# (実際には open('feed_model.json') などで読み込みます)
json_data = '''
{
  "parameters": {
    "c": [-50, -80],
    "A_ub": [[2, 3], [1, 4]],
    "b_ub": [100, 80],
    "bounds": [[0, null], [0, null]]
  }
}
'''
model = json.loads(json_data)["parameters"]

# 2. 最適化の実行
# JSONの構造をアンパック演算子(**)や引数指定で流し込む
res = linprog(
    c=model["c"],
    A_ub=model["A_ub"],
    b_ub=model["b_ub"],
    bounds=model["bounds"],
    method='highs'
)

# 3. 結果の表示
if res.success:
    print(f"最適生産量: {res.x}")
    print(f"最大利益: {-res.fun:.2f} 円")