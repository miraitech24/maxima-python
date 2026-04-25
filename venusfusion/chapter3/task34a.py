#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 12:17:29 2026

@author: iwamura
"""

import numpy as np
import subprocess

# --- Step 1: Maxima による数式導出 ---
def get_maxima_formula():
    maxima_code = """
    display2d:false$
    /* ツィオルコフスキーの方程式 dv = ve * ln(m0/m1) */
    /* ここで ve = Isp * g0 */
    /* 残存質量比 R = m1/m0 を dv と ve の関数として解く */
    eqn: dv = ve * log(1/R)$
    sol: solve(eqn, R)$
    print(rhs(sol[1]))$
    """
    with open("formula.mac", "w") as f:
        f.write(maxima_code)
    
    # Maxima実行
    result = subprocess.check_output(["maxima", "--very-quiet", "-r", "load(\"formula.mac\")$"])
    return result.decode().strip() # exp(-dv/ve) が返る

# --- Step 2: Python による数値シミュレーション ---
def run_pre_arrival_retro():
    # Maximaからロジックを継承
    formula_str = get_maxima_formula()
    
    # 定数設定
    g0 = 9.80665
    Isp = 12000     # 核融合エンジンの想定比推力 (s)
    v_arrival = 272 # 到着速度 (km/s)
    v_target = 7.8  # テザー捕獲許容速度 (km/s)
    m_initial = 5000 # カプセル初期質量 (kg)

    dv = (v_arrival - v_target) * 1000 # m/s
    ve = Isp * g0 # 有効排気速度
    
    # Maximaの解 e^(-dv/ve) を計算
    mass_ratio = np.exp(-dv / ve)
    m_final = m_initial * mass_ratio
    fuel_loss = m_initial - m_final

    print(f"--- #34a Retro-propulsion Analysis ---")
    print(f"Maxima Derived Formula: R = {formula_str}")
    print(f"Delta-V Required      : {dv/1000:.2f} km/s")
    print(f"Final Payload Mass    : {m_final:.2f} kg")
    print(f"Fuel Consumed         : {fuel_loss:.2f} kg")
    print(f"Mass Retention Rate   : {mass_ratio*100:.2f} %")
    
    # 次のステップ #42b へのバトン
    return m_final, v_target

if __name__ == "__main__":
    final_mass, v_rel = run_pre_arrival_retro()