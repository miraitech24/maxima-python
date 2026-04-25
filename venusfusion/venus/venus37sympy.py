#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 13:13:22 2026

@author: iwamura
"""

import sympy as sp

# 変数定義
t = sp.symbols('t') # 時間
N = sp.Function('N')(t) # システムの総稼働ユニット数
r = sp.symbols('r') # 自己増殖/修復率 (units/day) - #32より
lam = sp.symbols('lambda') # 故障率 (1/MTBF) - #36より
N_min = sp.symbols('N_min') # 拠点を維持するための最小ユニット数

# 微分方程式: 増加分 = 増殖(r * N) - 故障(lambda * N)
# ただし、増殖には資源（#28の炭素）や電力(#41)の制約があるため
# ロジスティック成長モデルに近い飽和特性を考慮する
K = sp.symbols('K') # 環境容量（利用可能な最大炭素リソース）
dndt = r * N * (1 - N/K) - lam * N

# 1. 定常状態 (dN/dt = 0) の解
equilibrium = sp.solve(dndt, N)

# 2. 生存条件の抽出
# N > 0 となるためには r > lambda である必要がある
survival_condition = r > lam

print(f"--- #37 生存閾値 解析結果 ---")
print(f"定常状態の解 (N*): {equilibrium}")
print(f"永続生存の必須条件: {survival_condition}")

# 具体的な数値代入 (仮定)
# #32より r = 0.05 (1日5%増殖), #36より MTBF=100日 => lambda = 0.01
res = dndt.subs({r: 0.05, lam: 0.01, K: 1000})
print(f"現在のパラメータでの成長勾配: {res}")