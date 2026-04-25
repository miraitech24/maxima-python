#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 11:55:19 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt

# --- 1. 山頂（マクスウェル山想定）の環境定数 ---
T_ambient = 380 + 273.15  # 外気温 (K) : 山頂は約380℃
P_ambient = 45 * 101325   # 外気圧 (Pa) : 山頂は約45気圧
rho_venus = 30.0          # 大気密度 (kg/m3) : 45気圧時の推定値
v_wind = 100.0            # スーパーローテーション風速 (m/s)

# --- 2. LENR炉のスペック ---
P_thermal_target = 100.0  # 目標熱出力 (GW)
T_core_limit = 1000 + 273.15 # 炉の構造材耐熱限界 (K) : 1000℃

# --- 3. ラジエーター冷却能力の計算 ---
# ニュートンの冷却法則: Q = h * A * (T_surface - T_ambient)
# 強制対流熱伝達係数 h の簡易見積もり (金星の高密度大気特性を考慮)
def calc_h_convection(v, rho):
    # 金星の超臨界CO2に近い高密度大気では、地球より熱伝達が極めて高い
    return 10.0 * (rho * v)**0.8 

def simulate_summit():
    h = calc_h_convection(v_wind, rho_venus)
    
    # 必要なラジエーター面積 A (km2) を逆算
    # 炉の表面温度を耐熱限界の 90% と仮定
    T_surface = T_core_limit * 0.9
    
    # 100GWを冷やすのに必要な面積
    required_area_m2 = (P_thermal_target * 1e9) / (h * (T_surface - T_ambient))
    required_area_km2 = required_area_m2 / 1e6

    print(f"--- 山頂拠点：第1段階 熱収支レポート ---")
    print(f"外気条件: {T_ambient-273.15:.1f} ℃ / {P_ambient/101325:.1f} atm")
    print(f"熱伝達係数 h: {h:.2f} W/(m2·K)")
    print(f"100GW冷却に必要なラジエーター面積: {required_area_km2:.3f} km2")
    
    # 面積に応じた「建設コスト」と「余剰電力」の推移
    areas = np.linspace(0.1, 2.0, 100) # km2
    cooling_cap_gw = (h * areas * 1e6 * (T_surface - T_ambient)) / 1e9
    
    plt.figure(figsize=(10, 5))
    plt.plot(areas, cooling_cap_gw, label='Cooling Capacity (GW)', color='blue')
    plt.axhline(y=P_thermal_target, color='red', linestyle='--', label='Target 100GW')
    plt.fill_between(areas, cooling_cap_gw, P_thermal_target, where=(cooling_cap_gw >= P_thermal_target), color='green', alpha=0.3, label='Stable Zone')
    
    plt.title("Venus Summit: LENR Cooling Balance")
    plt.xlabel("Radiator Area (km^2)")
    plt.ylabel("Power (GW)")
    plt.legend()
    plt.grid(True)
    plt.show()

simulate_summit()