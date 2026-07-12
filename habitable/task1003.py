#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 12:10:39 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from dyson_params import S_MERCURY, A_MAX, P_TARGET

def simulate_growth():
    # 初期条件
    p_initial = 10e12       # 金星から供給される初期電力 (10TW)
    efficiency = 0.3
    # 1TWの電力で1年間に生産できるパネル面積 (自己複製効率の仮定)
    # パネル生産エネルギーコスト: 1e9 J/m2 と仮定
    production_coeff = 3.1536e16 / 1e9  # (sec/year) / (J/m2)
    
    current_area = p_initial / (S_MERCURY * efficiency)
    years = 0
    history = []

    while True:
        current_power = current_area * S_MERCURY * efficiency
        history.append((years, current_power))
        
        if current_power >= P_TARGET or current_area >= A_MAX:
            break
            
        # 収穫した電力の50%を新たなパネル生産へ再投資
        new_area = (current_power * 0.5) * production_coeff
        current_area += new_area
        years += 1
        
        if years > 100: break # 安全ブレーキ

    print(f"--- Dyson Ring Growth Analysis ---")
    print(f"Target Power: {P_TARGET/1e12:.1f} TW")
    print(f"Time to reach target: {years} years")
    print(f"Final Area used: {current_area:.2e} m2 (Max available: {A_MAX:.2e} m2)")

if __name__ == "__main__":
    simulate_growth()