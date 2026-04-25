#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 11:53:25 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os

# ディレクトリ管理
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 1. Maxima実行
subprocess.run(['maxima', '-b', 'model.mac'], capture_output=True, text=True)

# 2. 数式のインポートと厳密な置換
if not os.path.exists("formula.txt"):
    raise FileNotFoundError("formula.txt was not generated.")

with open("formula.txt", "r") as f:
    raw_expr = f.read().strip()

# 置換の順序を厳密化 (TypeError回避)
py_expr = raw_expr.replace('^', '**')
py_expr = py_expr.replace('%e', 'np.exp') # %eをnumpyの指数関数へ

def get_C(z, D, v, S, C0, dC0):
    # eval時の名前空間をnp.expに固定
    context = {"np": np, "z": z, "D": D, "v": v, "S": S, "C0": C0, "dC0": dC0}
    return eval(py_expr, {"__builtins__": None}, context)

# 3. パラメータスイープ
z_vals = np.linspace(0, 10, 100)
v_list = [0.2, 0.8, 1.5, 3.0]

plt.figure(figsize=(10, 6))
for v_val in v_list:
    try:
        c_vals = [get_C(zv, 1.0, v_val, 0.1, 1.0, -0.2) for zv in z_vals]
        plt.plot(z_vals, c_vals, label=f'Settling velocity v={v_val}')
    except Exception as e:
        print(f"Eval Error at v={v_val}: {e}")

plt.title("Venusian Deuterium Concentration Profile (Analytic Connection)")
plt.xlabel("Altitude (z)")
plt.ylabel("Concentration (C)")
plt.legend()
plt.grid(True, linestyle='--')
plt.savefig("result_python.png")
plt.show()