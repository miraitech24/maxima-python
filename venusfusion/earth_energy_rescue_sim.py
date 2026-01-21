#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:53:55 2026

@author: iwamura
"""

import numpy as np

def earth_energy_rescue_sim(new_units_per_day=1.0):
    # --- 定数 ---
    EARTH_ANNUAL_CONSUMPTION_TWH = 25000 # 地球の年間消費電力
    UNIT_POWER_MW = 100 
    
    # 20年間をシミュレーション
    years = np.arange(1, 21)
    
    # 1. 炉の基数を計算 (整数型にキャストして float エラーを回避)
    daily_increments = np.full(20, new_units_per_day * 365)
    total_units = np.cumsum(daily_increments).astype(int)
    
    # 2. 金星での総発電量 (TWh/year)
    # (台数 * 100MW * 24時間 * 365日) / 1,000,000(TWh換算)
    # 年間の累計供給ポテンシャル
    venus_output_twh = (total_units * UNIT_POWER_MW * 24 * 365) / 1e6
    
    # 3. 地球への供給率 (%)
    supply_rate = (venus_output_twh / EARTH_ANNUAL_CONSUMPTION_TWH) * 100
    
    return years, total_units, supply_rate

# 実行
years, units, rates = earth_energy_rescue_sim(1.0)

print(f"--- 16. 地球エネルギー救済シミュレーション ---")
print(f" 5年目: 炉 {int(units[4]):>6,d} 基 / 地球供給率: {rates[4]:.2f} %")
print(f"10年目: 炉 {int(units[9]):>6,d} 基 / 地球供給率: {rates[9]:.2f} %")
print(f"20年目: 炉 {int(units[19]):>6,d} 基 / 地球供給率: {rates[19]:.2f} %")