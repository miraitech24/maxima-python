#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:38:31 2026

@author: iwamura
"""

import numpy as np

def calculate_cooling_cost(external_temp_c, internal_target_c=25.0):
    # --- 物理定数 ---
    # 核融合炉1基の出力: 100MW (100,000,000 W)
    total_power_output = 100e6 
    
    # 炉の表面積 (潜水艦型: 半径2m, 長さ10mの円筒を想定)
    surface_area = 2 * np.pi * 2 * 10 + 2 * np.pi * (2**2) # 約150 m^2
    
    # 断熱材の性能 (最新の真空断熱材を想定: 熱貫流率 U = 0.05 W/m2K)
    u_value = 0.05 
    
    # --- 熱力学計算 ---
    t_ext = external_temp_c + 273.15 # ケルビン換算
    t_int = internal_target_c + 273.15
    
    # 1. 外部から侵入する熱量 (Q_in = U * A * deltaT)
    q_in = u_value * surface_area * (t_ext - t_int)
    
    # 2. ヒートポンプの成績係数 (COP) 
    # 現実的な効率を考慮し、理論値の30%と仮定
    cop_theoretical = t_int / (t_ext - t_int)
    cop_real = cop_theoretical * 0.3
    
    # 3. 冷却に必要な電力 (P_cool = Q_in / COP)
    power_for_cooling = q_in / cop_real
    
    # 4. 消費比率
    cost_percentage = (power_for_cooling / total_power_output) * 100
    
    return q_in, power_for_cooling, cost_percentage

# 山頂と平地で比較
q_plain, p_plain, pct_plain = calculate_cooling_cost(460.0)
q_peak, p_peak, pct_peak = calculate_cooling_cost(380.8)

print(f"--- 14. 能動冷却エネルギー収支レポート ---")
print(f"【地表 0km (平地 460.0℃)】")
print(f"  侵入熱量: {q_plain/1000:.2f} kW / 冷却電力: {p_plain/1000:.2f} kW")
print(f"  出力消費率: {pct_plain:.4f} %")

print(f"\n【標高 11km (山頂 380.8℃)】")
print(f"  侵入熱量: {q_peak/1000:.2f} kW / 冷却電力: {p_peak/1000:.2f} kW")
print(f"  出力消費率: {pct_peak:.4f} %")