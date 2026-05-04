#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 14:42:29 2026

@author: iwamura
"""
# TAG: BIO-504C_optimization
import sympy as sp
from sympy import symbols, diff, solve, sqrt, lambdify

# 変数とパラメータ
x, y, lam, R = symbols('x y lam R', positive=True)

# 目的関数：放射線耐性と微小重力適応の総和（各確率は資源の平方根に比例）
P = sqrt(x) + sqrt(y)

# 制約条件：資源合計は R
g = x + y - R

# ラグランジアン
L = P - lam * g

# 停留条件
eq1 = diff(L, x)
eq2 = diff(L, y)
eq3 = diff(L, lam)

# 方程式を解く
sol = solve([eq1, eq2, eq3], (x, y, lam), dict=True)
opt = sol[0]
opt_x = opt[x]
opt_y = opt[y]
opt_P = sp.simplify(P.subs({x: opt_x, y: opt_y}))

# シンボル結果の表示
print("最適解:")
print(f"x = {opt_x}")
print(f"y = {opt_y}")
print(f"最大確率 P = {opt_P}")

# Markdown出力 (LaTeX)
md_content = f"""# BIO-504C 資源配分最適化結果

## 問題設定
宇宙環境耐性遺伝子の発現率（放射線耐性 $P_{{rad}}$ と微小重力適応 $P_{{micro}}$）を資源配分 $x, y$ の関数としてモデル化し、総資源 $R$ の下で最大化する。

**目的関数**:
$$
P(x, y) = \\sqrt{{x}} + \\sqrt{{y}}
$$

**制約条件**:
$$
x + y = R, \\quad x \\ge 0, \\; y \\ge 0
$$

## ラグランジュ未定乗数法
ラグランジアン $L = \\sqrt{{x}} + \\sqrt{{y}} - \\lambda (x + y - R)$ の停留条件より、

$$
\\frac{{\\partial L}}{{\\partial x}} = \\frac{{1}}{{2\\sqrt{{x}}}} - \\lambda = 0,
\\quad
\\frac{{\\partial L}}{{\\partial y}} = \\frac{{1}}{{2\\sqrt{{y}}}} - \\lambda = 0,
\\quad
\\frac{{\\partial L}}{{\\partial \\lambda}} = -(x + y - R) = 0
$$

## 最適配分
Sympy による解:
$$
x = \\frac{{R}}{{2}}, \\quad
y = \\frac{{R}}{{2}}
$$

## 最大総耐性確率
$$
P_{{\\text{{max}}}} = \\sqrt{{\\frac{{R}}{{2}}}} + \\sqrt{{\\frac{{R}}{{2}}}} = \\sqrt{{2R}}
$$

## 考察
資源を放射線耐性と微小重力適応に均等配分するとき、全体の宇宙適応確率が最大となる。  
この結果は、各適応機構が資源投入に対して収穫逓減（平方根型）であることに由来する。  
実際の生物学的パラメータ（例えば異なる感度係数）が付与されれば、最適配分は偏る可能性がある。

"""

with open("BIO-504C_optimization.md", "w", encoding="utf-8") as f:
    f.write(md_content)
print("Markdownファイル 'BIO-504C_optimization.md' を出力しました。")

