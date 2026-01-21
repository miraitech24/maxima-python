#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 16:30:55 2026

@author: iwamura
"""

import numpy as np

def predict_venus_env(altitude_km):
    # --- 物理モデルの定義 ---
    # 高度に応じた温度 (平地 460℃ -> 山頂 380℃)
    # altitudes_km ではなく altitude_km に修正
    temp_c = 460 - (altitude_km * 7.2) 
    
    # 高度に応じた密度 (平地 65kg/m3 -> 山頂 30kg/m3)
    density = 65 * np.exp(-altitude_km / 15.9)
    
    # 高度に応じた風速 (平地 2m/s -> 山頂 10m/s)
    wind_speed = 2 + (altitude_km * 0.8)

    # 動圧 q = 1/2 * density * velocity^2
    dynamic_pressure_venus = 0.5 * density * (wind_speed**2)
    
    # 地球換算風速 (1.2kg/m3の空気で同等の圧力を受ける速度)
    equivalent_earth_wind = np.sqrt(2 * dynamic_pressure_venus / 1.2)

    return {
        "temp": temp_c,
        "density": density,
        "wind": wind_speed,
        "eq_wind": equivalent_earth_wind
    }

# 実行
plains = predict_venus_env(0)
peaks = predict_venus_env(11)

print(f"--- 金星地表気象シミュレーション ---")
print(f"【地表 0km (平地)】")
print(f"  温度: {plains['temp']:.1f} ℃ / 換算風速: {plains['eq_wind']:.1f} m/s")
print(f"【標高 11km (マクスウェル山頂)】")
print(f"  温度: {peaks['temp']:.1f} ℃ / 換算風速: {peaks['eq_wind']:.1f} m/s")