#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 14:54:03 2026

@author: iwamura
"""

import numpy as np
import pandas as pd
import os

def run_heat_simulation():
    # ファイル読み込み
    input_file = "model_expr.txt"
    if not os.path.exists(input_file):
        print("Error: Maximaを実行して model_expr.txt を生成してください。")
        return

    with open(input_file, "r") as f:
        formula = f.read().strip()

    # 定数設定
    sigma_val = 5.67e-8
    epsilon_val = 0.85
    
    # 金星の高度別環境温度（例：地表から高度50kmまで）
    env_temps = [735, 640, 550, 460, 370, 280] 
    reactor_temp = 1000 # 炉心温度 1000K 固定での排熱量計算
    
    results = []
    for t_env in env_temps:
        # 安全な評価のために context を使用
        context = {
            "T": reactor_temp,
            "T_env": t_env,
            "sigma": sigma_val,
            "epsilon": epsilon_val
        }
        # Maximaから引き継いだ数式で計算
        p_out = eval(formula, {"__builtins__": None}, context)
        results.append({"Env_Temp_K": t_env, "Heat_Loss_W": p_out})
    
    df = pd.DataFrame(results)
    df.to_csv("cooling_results.csv", index=False)
    print("--- シミュレーション結果 ---")
    print(df)

if __name__ == "__main__":
    run_heat_simulation()