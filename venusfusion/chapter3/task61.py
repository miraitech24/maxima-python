#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 13:14:27 2026

@author: iwamura
"""

import subprocess
import numpy as np

def run_final_accounting():
    # --- Step 1: Maxima による価値評価関数の書き出し ---
    maxima_script = """
    display2d:false$
    V_total: eta * (P_cnt*W_cnt + P_alu*W_alu + P_abl*W_abl)$
    print(V_total)$
    """
    with open("recycle_logic.mac", "w") as f:
        f.write(maxima_script)
    
    # Maximaで数式を評価（期待値計算の準備）
    formula = subprocess.check_output(["maxima", "--very-quiet", "-r", "load(\"recycle_logic.mac\")$"]).decode().strip()

    # --- Step 2: Python による最終ROI決算 ---
    # 定数・変数設定
    params = {
        'eta': 0.85,    # 再資源化効率（15%は加工損失）
        'W_cnt': 80.0,   # 筐体用CNT重量 (kg)
        'W_alu': 52.0,   # 特殊合金重量 (kg)
        'W_abl': 100.0,  # 燃え残ったアブレータ重量 (kg)
        'P_cnt': 150.0,  # CNT市場単価 ($/kg)
        'P_alu': 15.0,   # 合金市場単価 ($/kg)
        'P_abl': 5.0     # アブレータ端材単価 ($/kg)
    }

    # MaximaのロジックをPythonで実行（evalを使用せず明示的に計算）
    scrap_value = params['eta'] * (
        params['P_cnt']*params['W_cnt'] + 
        params['P_alu']*params['W_alu'] + 
        params['P_abl']*params['W_abl']
    )

    # 主産物（水素ハイドライド）の利益
    hydrogen_mass = 400.0  # カプセル内積荷
    P_hydrogen = 50.0      # 水素売価 ($/kg)
    main_revenue = hydrogen_mass * P_hydrogen
    
    # 総投資コスト（金星製造＋往還燃料＋地球側回収費）
    total_cost = 12000.0 
    
    final_revenue = main_revenue + scrap_value
    final_roi = (final_revenue / total_cost) * 100

    print(f"--- #61 Final Resource Recycling & ROI Results ---")
    print(f"Maxima Derived Logic   : {formula}")
    print(f"Scrap Resource Value   : ${scrap_value:.2f}")
    print(f"Main Hydrogen Revenue  : ${main_revenue:.2f}")
    print(f"Total Project Revenue  : ${final_revenue:.2f}")
    print(f"FINAL PROJECT ROI      : {final_roi:.2f} %")
    print(f"Target ROI Comparison  : {'GO (Target Met)' if final_roi > 74.0 else 'NO-GO'}")

    return final_roi

if __name__ == "__main__":
    run_final_accounting()