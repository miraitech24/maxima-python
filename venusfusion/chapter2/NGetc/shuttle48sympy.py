#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 14:57:18 2026

@author: iwamura
"""

import numpy as np

# --- #14b 確定値からの入力 ---
cargo_mass = 13000 * 1000  # 1.3万トン [kg]
ship_mass = 2000 * 1000    # 船体自重 [kg]
m_initial = ship_mass + cargo_mass

# --- #48 推進パラメータ ---
# 核融合エンジンの比推力 (Isp = 10,000s 想定)
isp = 10000 
g0 = 9.80665
v_e = isp * g0  # 有効噴射速度 [m/s]

# 金星→地球遷移に必要なデルタV (高速往還モード)
delta_v = 25000 # 25km/s (2週間で帰るための強引な加速)

# --- ツィオルコフスキーの公式 ---
# m_final = m_initial / exp(delta_v / v_e)
m_final = m_initial / np.exp(delta_v / v_e)
propellant_consumed = m_initial - m_final

print(f"=== #48 帰還連成シミュレーション ===")
print(f"離脱開始質量: {m_initial/1000:,.0f} トン")
print(f"地球到着質量: {m_final/1000:,.1f} トン")
print(f"消費した推進剤: {propellant_consumed/1000:,.1f} トン")
print(f"地球へ届く純利益（商品）: {(m_final - ship_mass)/1000:,.1f} トン")

# 判定
efficiency = (m_final - ship_mass) / cargo_mass * 100
print(f"輸送効率（歩留まり）: {efficiency:.1f} %")