#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 12:01:11 2026

@author: iwamura
"""

import numpy as np

# --- Step 1: #13 地殻熱応力（山頂岩盤） ---
P_thermal = 100e9         # 炉の熱出力 (100GW)
A_radiator = 34000.0      # ラジエーター面積 (m2)
k_rock = 2.5              # 岩石の熱伝導率 (W/m·K) (玄武岩等)
alpha_rock = 8e-6         # 熱膨張係数 (1/K)
E_rock = 50e9             # ヤング率 (Pa)

def calc_geothermal_stress(leakage_ratio=0.01):
    # ラジエーターから地面へ1%（仮）の熱が漏れると仮定
    Q_leak = P_thermal * leakage_ratio 
    heat_flux = Q_leak / A_radiator # W/m2
    
    # 岩盤表面の温度上昇 (簡易半無限固体モデル)
    # 1年（3.15e7秒）後の深さ1m地点の温度上昇
    depth = 1.0
    time = 3.15e7
    dT = (heat_flux * depth) / k_rock
    
    # 熱応力 sigma = E * alpha * dT
    stress = E_rock * alpha_rock * dT
    
    print(f"--- #13 地殻熱応力解析（山頂） ---")
    print(f"地盤への漏洩熱量: {Q_leak/1e6:.1f} MW")
    print(f"1m深部の推定温度上昇: {dT:.1f} K")
    print(f"発生熱応力: {stress/1e6:.1f} MPa")
    
    # 岩盤の引張強度（通常10-20MPa）と比較
    limit = 15.0
    status = "SAFE" if stress/1e6 < limit else "DANGER: CRACK RISK"
    print(f"判定: {status}")

calc_geothermal_stress(0.001) # 0.1%の漏洩で計算