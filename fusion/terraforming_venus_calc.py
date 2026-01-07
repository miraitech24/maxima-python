#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 12:32:43 2026

@author: iwamura
"""

# terraforming_venus_calc.py (概念設計)

# 金星大気の総質量 (kg)
MASS_VENUS_ATMOSPHERE = 4.8e20 
# CO2の割合
CO2_RATIO = 0.96
# CO2 1kgあたりの分解に必要なエネルギー (J/kg)
ENERGY_TO_BREAK_CO2_PER_KG = 1.2e7 

def calculate_required_units(years_to_complete, unit_output_mw):
    """
    目標年数と1基あたりの出力から、必要な人工太陽の数を算出
    """
    total_energy_needed = MASS_VENUS_ATMOSPHERE * CO2_RATIO * ENERGY_TO_BREAK_CO2_PER_KG
    seconds_available = years_to_complete * 365 * 24 * 3600
    
    required_power_watt = total_energy_needed / seconds_available
    required_units = required_power_watt / (unit_output_mw * 1e6)
    
    return required_units

# 例: 30年で完了させたい場合、100MW級のユニットが何個必要か？
units = calculate_required_units(30, 100)
print(f"必要な100MW級核融合ユニット: 約 {units:.2e} 基")