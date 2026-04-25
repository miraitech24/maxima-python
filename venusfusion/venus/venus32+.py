#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 12:49:49 2026

@author: iwamura
"""

import numpy as np

# --- #41+ からの入力 ---
P_supply_gw = 100.0   # 供給電力 (GW)
P_alloc_ratio = 0.2   # 掘削・建設への投入比率 (20%)

# --- #32+ & #28 設計パラメータ ---
shaft_diameter = 20.0 # シャフト径 (m)
shaft_depth = 1000.0  # 到達目標深さ (m)
e_s_rock = 5.0e9      # 比掘削エネルギー (J/m3) ※玄武岩
rho_cnt = 1600.0      # CNT補強壁の密度 (kg/m3)
wall_thickness = 0.5  # シャフト壁面のライニング厚 (m)

def simulate_step32_plus():
    p_work_w = P_supply_gw * P_alloc_ratio * 1e9
    
    # 1. 掘削計算
    vol_rock = np.pi * (shaft_diameter/2)**2 * shaft_depth
    t_excavation = (vol_rock * e_s_rock) / p_work_w # 秒
    
    # 2. #28 炭素抽出と #32 壁面施工
    # 壁面の体積 = (外円柱 - 内円柱)
    vol_wall = (np.pi * ((shaft_diameter/2) + wall_thickness)**2 - np.pi * (shaft_diameter/2)**2) * shaft_depth
    mass_cnt_needed = vol_wall * rho_cnt
    
    # 建設期間の算出
    days = t_excavation / (24 * 3600)
    
    print(f"--- #32+ 地下進出掘削レポート ---")
    print(f"投入電力 (#41+より): {P_supply_gw * P_alloc_ratio:.1f} GW")
    print(f"掘削対象容積: {vol_rock:.1f} m3")
    print(f"1km垂直抗 掘削完了までの期間: {days:.2f} 日")
    print(f"必要CNT量 (#28より抽出): {mass_cnt_needed/1e3:.1f} トン")
    
    return days

simulate_step32_plus()