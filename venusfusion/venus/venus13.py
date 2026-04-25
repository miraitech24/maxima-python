#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 12:23:24 2026

@author: iwamura
"""

import numpy as np

# --- Step 1: #13 再計算（厚み d の真の解） ---
T_reactor_bottom = 700 + 273.15 # 炉の底面温度 (700℃)
T_ground_limit = (380 + 25) + 273.15 # 岩盤許容温度 (380℃ + 25K)
k_insulation = 0.03  # CNT系高性能断熱材 (W/m·K)
P_thermal = 100e9    # 100GW
A_radiator = 34000   # 34,000 m2

def finalize_insulation():
    # 必要な温度降下 Delta T
    dT_drop = T_reactor_bottom - T_ground_limit
    
    # ラジエーターが99.9%の熱を捨て、地面へ0.1%漏れるとした時の流束
    heat_flux_leak = (P_thermal * 0.001) / A_radiator 
    
    # 厚み d = (k * dT) / flux
    d_required = (k_insulation * dT_drop) / heat_flux_leak
    
    print(f"--- #13 断熱仕様 最終確定 ---")
    print(f"炉底部と地表の温度差: {dT_drop:.1f} K")
    print(f"必要な断熱層の厚み: {d_required:.3f} m")
    return d_required

d_ins = finalize_insulation()