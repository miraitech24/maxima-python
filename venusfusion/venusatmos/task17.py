#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 14:51:48 2026

@author: iwamura
"""

import numpy as np
import pandas as pd
import math
import os

def run_tunneling_sim(A_val, D_eff_val, E_val):
    # ファイル存在チェック
    input_file = "sol_v.txt"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} が見つかりません。先にMaximaスクリプトを実行してください。")
        return

    with open(input_file, "r") as f:
        raw_expr = f.read().strip()
    
    # Maximaの数式をPythonで評価可能な形式に置換
    py_expr = raw_expr.replace("exp", "math.exp").replace("^", "**")
    
    # 遮蔽半径 D を 2.0 から 10.0 まで変化させて繰り返し計算
    results = []
    for D_val in np.linspace(2.0, 10.0, 20):
        context = {"math": math, "A": A_val, "D_eff": D_eff_val, "E_kin": E_val, "D": D_val}
        prob = eval(py_expr, context)
        results.append({"shielding_radius_D": D_val, "probability": prob})
    
    df = pd.DataFrame(results)
    df.to_csv("tunneling_results.csv", index=False)
    print("--- シミュレーション完了 ---")
    print(df.head())

if __name__ == "__main__":
    # パラメータ: A(定数), D_eff(有効距離), E(エネルギー)
    run_tunneling_sim(12.5, 0.8, 15.0)