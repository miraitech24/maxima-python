#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 15:32:44 2025

@author: iwamura
"""

#!/usr/bin/env python3
# Spyder(Python)用スクリプト（クリーン版）
# 使い方:
#  - 同じディレクトリに params.txt と analytic.txt を置く
#  - Spyder で実行、またはターミナルで `python spyder_solve_and_plot.py analytic.txt`

import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import csv
import re
import sys
import unicodedata

def parse_params_txt(path):
    """
    params.txt を読み込み、コメントを除去して key: value; 形式をパースする。
    サポートするコメント: /* ... */ , //... , #...
    値は可能なら float に変換する。
    """
    params = {}
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # remove C-style comments /* ... */
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    # remove // comments
    text = re.sub(r'//.*', '', text)
    # remove # comments
    text = re.sub(r'#.*', '', text)

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            left, right = line.split(':', 1)
            name = left.strip()
            # remove trailing semicolon/comma and surrounding whitespace
            valstr = right.strip().rstrip(';').rstrip(',').strip()
            # try float conversion
            try:
                val = float(valstr)
            except Exception:
                val = valstr
            params[name] = val
    return params

def parse_analytic_txt(path):
    data = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                try:
                    data[k.strip()] = float(v.strip())
                except:
                    data[k.strip()] = v.strip()
    return data

# 解析解（減衰系）
def analytic_solution(t, m, c, k, x0, v0):
    wn = math.sqrt(k/m)
    zeta = c/(2*math.sqrt(m*k))
    if zeta < 1.0 - 1e-8:
        wd = wn*math.sqrt(1 - zeta*zeta)
        A = x0
        B = (v0 + zeta*wn*x0)/wd
        x = math.exp(-zeta*wn*t)*( A*math.cos(wd*t) + B*math.sin(wd*t) )
    elif abs(zeta-1.0) < 1e-8:
        # 臨界減衰
        A = x0
        B = v0 + wn*x0
        x = (A + B*t)*math.exp(-wn*t)
    else:
        # 過減衰
        r1 = -wn*(zeta) + wn*math.sqrt(zeta*zeta - 1)
        r2 = -wn*(zeta) - wn*math.sqrt(zeta*zeta - 1)
        C2 = (v0 - r1*x0)/(r2 - r1)
        C1 = x0 - C2
        x = C1*math.exp(r1*t) + C2*math.exp(r2*t)
    return x

def mass_spring_damper_rhs(t, y, m, c, k):
    x, v = y
    dxdt = v
    dvdt = -(c/m)*v - (k/m)*x
    return [dxdt, dvdt]

def to_float(val, default=0.0):
    try:
        return float(val)
    except:
        return default

def main():
    # analytic file can be passed as first command-line arg (useful with %run)
    analytic_path = sys.argv[1] if len(sys.argv) > 1 else "analytic.txt"

    params = parse_params_txt("params.txt")
    ana = parse_analytic_txt(analytic_path)

    # パラメータ取得（存在チェックおよび float 化）
    m = to_float(params.get('m', 1.0), 1.0)
    c = to_float(params.get('c', 0.0), 0.0)
    k = to_float(params.get('k', 1.0), 1.0)
    x0 = to_float(params.get('x0', 0.0), 0.0)
    v0 = to_float(params.get('v0', 0.0), 0.0)
    t_end = to_float(params.get('t_end', 10.0), 10.0)
    dt = to_float(params.get('dt', 0.01), 0.01)

    wn = ana.get('wn', math.sqrt(k/m))
    zeta = ana.get('zeta', c/(2*math.sqrt(m*k)))
    print("Parameters (from params.txt): m={}, c={}, k={}, x0={}, v0={}".format(
        m, c, k, x0, v0))
    print("Analytic params (from {}): wn={}, zeta={}".format(analytic_path, wn, zeta))

    t = np.arange(0, t_end + dt/2, dt)

    # 数値解（初期値を float にして渡す）
    y0 = [float(x0), float(v0)]
    sol = solve_ivp(mass_spring_damper_rhs, [0, t_end], y0, t_eval=t, args=(m, c, k), rtol=1e-8)
    x_num = sol.y[0, :]

    # 解析解（閉形式）
    x_ana = np.array([analytic_solution(tt, m, c, k, x0, v0) for tt in t])

    # CSV 出力
    with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['t', 'x_numeric', 'x_analytic'])
        for ti, xn, xa in zip(t, x_num, x_ana):
            writer.writerow([ti, xn, xa])

    # プロット
    plt.figure(figsize=(8, 4))
    plt.plot(t, x_num, label='numeric (solve_ivp)', linewidth=1)
    plt.plot(t, x_ana, '--', label='analytic', linewidth=1)
    plt.xlabel('t [s]')
    plt.ylabel('x [m]')
    plt.title('Mass-Spring-Damper response\nwn={:.4f}, zeta={:.4f}'.format(wn, zeta))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('response.png', dpi=150)
    print("Saved results.csv and response.png")
    plt.show()

if __name__ == "__main__":
    main()