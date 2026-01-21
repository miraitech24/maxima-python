#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 15:04:35 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

def simulate_terraforming(growth_mode='exponential'):
    # --- 定数設定 ---
    CO2_TOTAL_MASS = 4.8e20  # 金星のCO2総質量 (kg)
    DECOMP_ENERGY_PER_KG = 1.2e7  # CO2を分解するのに必要なエネルギー (J/kg)
    TOTAL_ENERGY_NEEDED = CO2_TOTAL_MASS * DECOMP_ENERGY_PER_KG
    
    UNIT_POWER_WATT = 100e6  # 炉1基あたりの出力 (100MW)
    SEC_PER_YEAR = 3600 * 24 * 365
    
    years = np.arange(0, 101, 1)
    units = np.zeros(len(years))
    co2_remaining = np.zeros(len(years))
    co2_remaining[0] = TOTAL_ENERGY_NEEDED
    
    # --- シナリオ設定 ---
    initial_units = 100  # 最初に地球から送り込む数
    
    for t in range(len(years)):
        if growth_mode == 'linear':
            # 毎年1000基ずつ追加
            units[t] = initial_units + (t * 1000)
        elif growth_mode == 'exponential':
            # 5年ごとに数が倍増すると仮定 (自己増殖)
            units[t] = initial_units * (2 ** (t / 5))
            
        # その年の総出力 (J)
        yearly_energy = units[t] * UNIT_POWER_WATT * SEC_PER_YEAR
        
        if t > 0:
            co2_remaining[t] = max(0, co2_remaining[t-1] - yearly_energy)
            
    return years, units, (co2_remaining / TOTAL_ENERGY_NEEDED) * 100

# シミュレーション実行
y, u_lin, c_lin = simulate_terraforming('linear')
y, u_exp, c_exp = simulate_terraforming('exponential')

# --- 可視化 ---
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('Years from Launch')
ax1.set_ylabel('CO2 Remaining (%)', color='tab:red')
ax1.plot(y, c_lin, label='Linear (Piston Transport)', color='tab:red', linestyle='--')
ax1.plot(y, c_exp, label='Exponential (Self-Replication)', color='tab:red', lw=3)
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.grid(True)

ax2 = ax1.twinx()
ax2.set_ylabel('Number of Fusion Units', color='tab:blue')
ax2.plot(y, u_exp, color='tab:blue', alpha=0.3)
ax2.set_yscale('log')
ax2.tick_params(axis='y', labelcolor='tab:blue')

plt.title('Venus Terraforming Timeline: The Power of Self-Replication')
fig.tight_layout()
plt.show()