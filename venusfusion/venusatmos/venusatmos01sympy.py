#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 11:54:41 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import os

# 1. SymPyによる解析解の導出 (Maximaの役割を代替)
z = sp.symbols('z', real=True)
C = sp.Function('C')
D, v, S, C0, dC0 = sp.symbols('D v S C0 dC0', real=True, positive=True)

# 微分方程式の定義: D*C''(z) - v*C'(z) + S = 0
ode = D * C(z).diff(z, z) - v * C(z).diff(z) + S

# 一般解の導出
sol = sp.dsolve(ode, C(z))

# 境界条件の適用: C(0)=C0, C'(0)=dC0
ics = {C(0): C0, C(z).diff(z).subs(z, 0): dC0}
sol_ivp = sp.dsolve(ode, C(z), ics=ics)

# 解析解（右辺）を高速計算用にNumPy関数へ変換 (Lambdify)
# これにより、Maximaからのインポートで発生していた型エラーを完全に回避
func_C = sp.lambdify((z, D, v, S, C0, dC0), sol_ivp.rhs, "numpy")

# 2. Pythonによるパラメータスイープ (沈降速度 v > 0 の影響)
z_vals = np.linspace(0, 10, 100)
v_list = [0.2, 0.8, 1.5, 3.0]

plt.figure(figsize=(10, 6))
for v_val in v_list:
    # 物理条件: D=1.0, S=0.1, C0=1.0, dC0=-0.2 (下向き勾配)
    c_vals = func_C(z_vals, 1.0, v_val, 0.1, 1.0, -0.2)
    plt.plot(z_vals, c_vals, label=f'Settling velocity v={v_val}')

plt.title("Deuterium Concentration Profile in Venusian Clouds (v > 0)")
plt.xlabel("Altitude (z)")
plt.ylabel("Concentration (C)")
plt.legend()
plt.grid(True, linestyle='--')
plt.savefig("result_python.png")
plt.show()

# 参考用に解析解をテキスト出力
with open("formula_sympy.txt", "w") as f:
    f.write(str(sol_ivp.rhs))