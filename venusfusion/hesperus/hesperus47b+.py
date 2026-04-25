#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 12:54:13 2026

@author: iwamura
"""

import numpy as np
from scipy.optimize import fsolve

# 1. 前工程からの定数
M0 = 20_000_000 # 2万トン
Isp = 10000
g0 = 9.80665
target_dist = 41.4e9 # 4,140万km (m換算)
target_time = 14 * 24 * 3600 # 14日間
loss_rate = 0.15 # 大気圏損耗
price_per_ton = 500_000
fixed_cost = 100_000_000

# 2. ROI 74.0% を達成するための必要残存重量を逆算
# ROI = (Sales - Cost) / Cost = 0.74
# Sales = m_net * price
# Cost = (m_fuel * price * 0.1) + fixed_cost
# ※ 燃料原価率 0.1, 固定費 1億

def calculate_roi(m_dot):
    ve = Isp * g0
    # 14日後の到達距離 (s)
    dist = ve * (target_time - (M0 - m_dot * target_time) / m_dot * np.log(M0 / (M0 - m_dot * target_time)))
    
    # 到達距離不足ならROI計算不能としてペナルティ
    if dist < target_dist: return -999 
    
    m_fuel = m_dot * target_time
    m_net = (M0 - m_fuel) * (1 - loss_rate)
    
    sales = m_net * price_per_ton
    costs = (m_fuel * price_per_ton * 0.1) + fixed_cost
    roi = (sales - costs) / costs
    return roi - 0.74 # 目標との差分

# 3. 最適な m_dot (燃料消費率) を探索
optimized_m_dot = fsolve(calculate_roi, 7.0)[0] # 7kg/s付近から探索

# 4. 結果の再計算
ve = Isp * g0
final_dist = ve * (target_time - (M0 - optimized_m_dot * target_time) / optimized_m_dot * np.log(M0 / (M0 - optimized_m_dot * target_time)))
final_fuel = optimized_m_dot * target_time
final_net = (M0 - final_fuel) * (1 - loss_rate)
final_roi_val = ((final_net * price_per_ton) - (final_fuel * price_per_ton * 0.1 + fixed_cost)) / (final_fuel * price_per_ton * 0.1 + fixed_cost) * 100

print(f"--- #47b Optimized ROI Solution ---")
print(f"Optimized Fuel Consumption: {optimized_m_dot:.2f} kg/s")
print(f"Final Distance: {final_dist/1e9:.2f} million km (Requirement: 41.4M)")
print(f"Net Hydride Delivered: {final_net:.2f} tons")
print(f"Final ROI: {final_roi_val:.2f}%")
print(f"Judgment: {'SUCCESS (ROI 74% Lock)' if final_roi_val >= 73.9 else 'RETRY'}")