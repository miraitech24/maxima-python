#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 12:16:37 2026

@author: iwamura
"""

# shuttle48.py
import numpy as np
import importlib
import target_expr

def run_combined_analysis():
    importlib.reload(target_expr)
    
    # 設計パラメータ
    SIGMA = 5.67e-8
    EPSILON = 0.9
    AREA = 1200.0        # ラジエーター面積 [m^2]
    T_LIMIT = 550.0      # 燃料熱安定限界 [K]
    D_VENUS = 5.0e10     # 地球-金星間距離 [m]
    MASS_SHIP = 200000.0  # 船体質量 [kg]
    LOSS_FACTOR = 1200.0 # 1Nあたりの排熱量 [W/N]

    # Step 1: 熱制約による最大推力の特定
    thrust_range = np.linspace(1000, 300000, 500)
    p_thermal = thrust_range * LOSS_FACTOR
    
    # 表面温度の計算
    temps = target_expr.get_temp_formula(p_thermal, EPSILON, SIGMA, AREA, 3.0)
    
    # 安全な推力の抽出
    safe_thrusts = thrust_range[temps < T_LIMIT]
    if len(safe_thrusts) == 0:
        print("Error: 冷却能力不足")
        return
    
    max_f = safe_thrusts[-1]
    max_a = max_f / MASS_SHIP

    # Step 2: 軌道所要時間の計算
    # 往路(t) + 復路(t) = 2 * t
    t_one_way_sec = target_expr.get_travel_time(D_VENUS, max_a)
    total_days = (t_one_way_sec * 2) / (24 * 3600)

    print(f"=== 統合連成解析結果 (#47, #56, #48) ===")
    print(f"熱限界最大推力: {max_f/1000:.2f} kN")
    print(f"最大運用加速度: {max_a:.4f} m/s^2 (約 {max_a/9.8:.3f} G)")
    print(f"計算上の往復日数: {total_days:.2f} 日")

    if total_days <= 14.0:
        print("判定: 【成功】 往復2週間以内の高速航行は可能です。")
    else:
        print(f"判定: 【不可】 目標まで {total_days-14:.2f} 日不足。質量削減または面積拡大が必要。")

if __name__ == "__main__":
    run_combined_analysis()