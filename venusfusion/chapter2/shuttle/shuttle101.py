#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 16:54:40 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from trajectory_params import get_final_v, get_final_d

def analyze_sprint_mission():
    # 定数 (#100のバトンを継承)
    m_tether = 98.6
    m_payload = 1000.0
    m_fuel = 800.0   # ハイドライド燃料
    m0 = m_payload + m_tether + m_fuel
    F_max = 90000.0  # 90kN (核融合エンジン)
    
    # 燃焼シナリオ: 1時間(3600s)で一気に加速
    t_burn = 3600.0
    m_dot = m_fuel / t_burn
    
    # Maximaの解を用いて加速フェーズ終了時の状態を算出
    v_boost = get_final_v(F_max, m0, m_dot, t_burn)
    d_boost = get_final_d(F_max, m0, m_dot, t_burn)
    
    # 残りの距離を慣性航行
    target_distance = 41.4e9 # 41.4M km
    d_remain = target_distance - d_boost
    t_cruise = d_remain / v_boost
    
    total_days = (t_burn + t_cruise) / (24 * 3600)
    
    print(f"--- #101 往還軌道解析結果 ---")
    print(f"加速終了時速度 (Delta-V): {v_boost/1000:.2f} km/s")
    print(f"加速終了時加速度: {F_max/(m0-m_fuel)/9.8:.2f} G")
    print(f"総航行日数: {total_days:.2f} 日")
    
    # 到達判定
    
    if total_days <= 14.0:
        print("【判定】PASS: 14日以内の地球到達が可能です。")
    else:
        print("【判定】FAIL: 推力または燃料比率が不足しています。")

if __name__ == "__main__":
    analyze_sprint_mission()