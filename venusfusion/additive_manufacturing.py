#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:42:17 2026

@author: iwamura
"""

import numpy as np

def simulate_factory_output(power_available_mw=10.0):
    # --- 定数設定 ---
    # CO2をCとO2に分解するのに必要なエネルギー (約33MJ/kg)
    ENERGY_CO2_BREAKDOWN = 33e6 
    
    # 炉1基の推定質量: 10,000kg (10トン)
    # そのうち 80% を炭素複合材(機体・構造)で作ると仮定
    carbon_needed_per_unit = 10000 * 0.8
    
    # --- 計算 ---
    # 母船が「余剰電力」として10MWを製造に回した場合
    energy_per_day = power_available_mw * 1e6 * 24 * 3600
    
    # 1日に分解できる炭素量 (kg)
    carbon_produced_per_day = (energy_per_day / ENERGY_CO2_BREAKDOWN) * (12/44) # C/CO2 分子量比
    
    # 炉1基を完成させるのに必要な日数
    days_to_print_one_unit = carbon_needed_per_unit / carbon_produced_per_day
    
    return carbon_produced_per_day, days_to_print_one_unit

# 実行
c_day, days = simulate_factory_output(10.0) # 母船の余剰10MWを投入

print(f"--- 15. 母船ヘスペロス 工場稼働レポート ---")
print(f"1日あたりの炭素生産量: {c_day:.1f} kg")
print(f"潜水艦型炉1基（炭素8トン分）のプリント期間: {days:.2f} 日")