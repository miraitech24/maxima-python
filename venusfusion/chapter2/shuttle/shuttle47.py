#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 11:59:57 2026

@author: iwamura
"""

# main_analysis.py
import numpy as np
from target_expr import get_temp_formula

def run_thermal_coupling():
    # 物理定数・設計値
    SIGMA = 5.67e-8
    EPSILON = 0.9
    AREA = 1200.0      # ラジエーター面積(m^2)
    T_SPACE = 3.0      # 宇宙背景放射(K)
    T_LIMIT = 550.0    # 水素ハイドライド熱安定限界(K)

    # 推力レンジ(N) 0 to 150kN
    thrust_n = np.linspace(100, 150000, 100)
    
    # 排熱量換算：核融合エンジン損失 (1Nあたり1.1kWの熱損失と仮定)
    p_thermal = thrust_n * 1100.0
    
    # Maximaからインポートした関数で計算
    try:
        surface_temps = get_temp_formula(p_thermal, EPSILON, SIGMA, AREA, T_SPACE)
        
        # 限界値の特定
        safe_mask = surface_temps < T_LIMIT
        if not any(safe_mask):
            max_thrust = 0
        else:
            max_thrust = thrust_n[safe_mask][-1]

        print(f"=== 連成解析結果 (#47 & #56) ===")
        print(f"燃料安定限界温度: {T_LIMIT} K")
        print(f"現在の設計での最大許容推力: {max_thrust/1000:.2f} kN")
        
        # #48へのフィードバック
        # 2週間往復には概ね 50kN 以上の持続推力が必要と仮定
        if max_thrust < 50000:
            print("判定: 排熱限界により、2週間航行に必要な加速を維持できません。面積拡大が必要です。")
        else:
            print("判定: 物理制約クリア。この推力値を上限として #48 軌道シミュレーションを開始してください。")

    except NameError as e:
        print(f"インポートエラー: {e}。target_expr.py に Maxima の制御記号が混入していないか確認してください。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    run_thermal_coupling()