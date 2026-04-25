#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 12:52:33 2026

@author: iwamura
"""

import numpy as np

# --- #32（掘削）および環境条件からの継承 ---
L_chimney = 1000.0   # 煙突の長さ (m) = シャフトの深さ
D_chimney = 20.0     # 煙突の直径 (m)
A_chimney = np.pi * (D_chimney/2)**2

# 金星の環境（山頂〜地下平均）
rho_air = 35.0       # 大気密度 (kg/m3)
g = 8.87             # 金星重力 (m/s2)
T_ground = 460 + 273.15 # 地下温度 (K)
T_summit = 380 + 273.15 # 山頂温度 (K)

def simulate_v44_revised():
    # 1. 煙突効果による圧力差 (Buoyancy Pressure)
    # Delta P = rho * g * L * (dT / T_avg)
    dT = T_ground - T_summit
    T_avg = (T_ground + T_summit) / 2
    dP = rho_air * g * L_chimney * (dT / T_avg)
    
    # 2. 上昇気流の流速 (ベルヌーイの式より)
    # v = sqrt(2 * dP / rho)
    v_wind = np.sqrt(2 * dP / rho_air)
    
    # 3. 発電出力 (風力タービン効率 40% 想定)
    # Power = 0.5 * rho * A * v^3 * efficiency
    mass_flow = rho_air * A_chimney * v_wind
    power_gen_w = 0.5 * rho_air * A_chimney * (v_wind**3) * 0.4
    
    print(f"--- #44 大気動力学（修正：地下シャフト発電） ---")
    print(f"煙突仕様: 直径{D_chimney}m, 長さ{L_chimney}m")
    print(f"発生上昇気流: {v_wind:.2f} m/s")
    print(f"質量流量: {mass_flow/1e3:.1f} トン/s")
    print(f"回収可能電力: {power_gen_w/1e6:.2f} MW")
    
    return power_gen_w

simulate_v44_revised()