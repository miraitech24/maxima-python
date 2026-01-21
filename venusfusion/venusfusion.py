#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 13:54:28 2026

@author: iwamura
"""

# 17. economic_impact.py
import numpy as np

def simulate_investment_return():
    # --- 定数設定 ---
    UNIT_POWER_MW = 100
    SALE_PRICE_KWH = 5.0 # 日本の平均より大幅に安い、5円/kWhで販売
    CONSTRUCTION_COST_B_YEN = 500 # 炉1基あたりの製造・運搬・維持コスト（500億円と仮定）
    
    # 20年間のシミュレーション
    years = np.arange(1, 21)
    # 15.pyの結果、年間365基増殖
    total_units = np.cumsum(np.full(20, 365))
    
    # 1. 売上計算 (兆円単位)
    # (台数 * 100,000kW * 24h * 365d * 5円) / 10^12
    annual_revenue_trillion = (total_units * UNIT_POWER_MW * 1000 * 24 * 365 * SALE_PRICE_KWH) / 1e12
    
    # 2. 投資額計算 (兆円単位)
    # 実際は自己増殖により製造コストは激減するが、厳しめに設定
    annual_cost_trillion = (365 * CONSTRUCTION_COST_B_YEN) / 1000
    
    # 3. 累積キャッシュフロー
    cumulative_profit = np.cumsum(annual_revenue_trillion - annual_cost_trillion)
    
    print(f"--- 17. VENUS-G Economic Impact (Cashflow) ---")
    for i in [4, 9, 19]:
        print(f"Year {years[i]:02d}:")
        print(f"  Annual Revenue: {annual_revenue_trillion[i]:.1f} Trillion JPY")
        print(f"  Cumulative Profit: {cumulative_profit[i]:.1f} Trillion JPY")
        if cumulative_profit[i] > 0:
            print(f"  Status: [ PROFITABLE ]")
        else:
            print(f"  Status: [ INVESTMENT PHASE ]")

if __name__ == "__main__":
    simulate_investment_return()