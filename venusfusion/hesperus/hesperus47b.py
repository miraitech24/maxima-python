#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 12:51:58 2026

@author: iwamura
"""

import sympy as sp

# 1. SymPy：利益構造の定義
# --------------------------------------------------
m_initial, m_fuel, loss_rate, price_per_ton, fixed_cost = sp.symbols('m_initial m_fuel loss_rate price_per_ton fixed_cost')

# 地球到着時の正味重量 (初期量 - 燃料消費) * (1 - 突入焼失率)
m_net = (m_initial - m_fuel) * (1 - loss_rate)
# 売上
sales = m_net * price_per_ton
# 総コスト (燃料分原価 + 固定費)
total_cost = (m_fuel * price_per_ton * 0.1) + fixed_cost # 燃料原価は売価の10%と仮定
# ROI公式
roi_expr = (sales - total_cost) / total_cost * 100

# 2. Python：実績値の投入
# --------------------------------------------------
results_48_57 = {
    "m_initial": 20000.0,    # 2万トン
    "m_fuel": 18748.8,       # #48/#57の算出結果
}

params_biz = {
    loss_rate: 0.15,         # #42 大気圏突入焼失率 15%
    price_per_ton: 500000,   # 水素ハイドライド売価 (円/トン) 仮想
    fixed_cost: 100000000,   # 固定費 1億円
}

# 3. ROI算出
final_roi = roi_expr.subs(results_48_57).subs(params_biz).evalf()

print(f"--- #47b Final ROI Calculation ---")
print(f"Net Hydride Delivered: {float(m_net.subs(results_48_57).subs(params_biz)):.2f} tons")
print(f"Final ROI: {final_roi:.2f}%")
print(f"Target ROI: 74.00%")
print(f"Judgment: {'GO' if final_roi >= 74.0 else 'NOGO (Efficiency optimization required)'}")