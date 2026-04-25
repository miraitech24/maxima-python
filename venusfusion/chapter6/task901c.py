#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 12:03:53 2026

@author: iwamura
"""

import numpy as np
from torque_params import M_ATM_KG, N_NAT_NM

# 定数
POWER_TOTAL_W = 10.0e12 # 水星からの受電電力
EFFICIENCY_DRAG = 0.15  # 電力から大気制動（推力）への変換効率 (プラズマ加速等)
R_VENUS = 6052e3

def analyze_stability():
    # 1. 供給される制動トルク N_supply
    # P = N * omega => N = P / omega
    # 目標風速 1m/s (omega = 1/R_venus)
    omega_target = 1.0 / R_VENUS
    n_supply = (POWER_TOTAL_W * EFFICIENCY_DRAG) / omega_target
    
    # 2. 安全率の計算
    safety_margin = n_supply / N_NAT_NM
    
    # 3. 10TWで制動可能な最大風速 (N_supply = N_nat となる風速)
    # P * eff / (v/R) = N_nat => v = (P * eff * R) / N_nat
    v_limit = (POWER_TOTAL_W * EFFICIENCY_DRAG * R_VENUS) / N_NAT_NM

    print(f"--- SR Stability Analysis (#901c) ---")
    print(f"Atmosphere Mass: {M_ATM_KG:.2e} kg")
    print(f"Available Braking Torque: {n_supply:.2e} Nm")
    print(f"Natural SR Driving Torque: {N_NAT_NM:.2e} Nm")
    print(f"System Safety Margin: {safety_margin:.2f} x")
    print(f"Controllable Wind Speed Limit: {v_limit:.2f} m/s")
    
    print("\n[考察]")
    print(f"1. 安全率{safety_margin:.1f}倍: 水星からの10TWは、SRを再発させようとする自然の力を圧倒しています。")
    print(f"2. 制御限界: 万一大気が乱れても、風速{v_limit:.1f}m/s（時速約{v_limit*3.6:.0f}km）までなら、")
    print(f"   水星の電力だけで力ずくで停止状態へ引き戻すことが可能です。")
    print(f"3. 結論: これにより865拠点の「住民」は、二度とあの大嵐に怯える必要がなくなりました。")

analyze_stability()