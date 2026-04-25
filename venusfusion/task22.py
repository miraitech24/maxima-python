#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 14:47:41 2026

@author: iwamura
"""

import numpy as np
import pandas as pd
import math

def run_simulation(G_val, lambda_val, N0_val, steps):
    # Maximaから出力された数式をインポート（簡易的な文字列置換でPython用に変換）
    with open("sol_expr.txt", "r") as f:
        raw_expr = f.read().strip()
    
    # Maximaの数式表現をPython/numpy形式に変換
    py_expr = raw_expr.replace("%e", "math.e")
    
    results = []
    for t in range(steps):
        # 物理パラメータをコンテキストとして評価
        N_t = eval(py_expr, {"math": math, "G": G_val, "lambda": lambda_val, "N0": N0_val, "t": t})
        results.append({"step": t, "concentration": N_t})
    
    # データの蓄積と出力
    df = pd.DataFrame(results)
    df.to_csv("tritium_history.csv", index=False)
    print("シミュレーション完了: tritium_history.csv に保存されました")

if __name__ == "__main__":
    # %run simulation.py 1.5 0.05 0 100 のような引数想定
    import sys
    args = sys.argv[1:]
    G = float(args[0]) if len(args) > 0 else 1.0
    run_simulation(G, 0.056, 0, 50)