#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 18:32:40 2026

@author: iwamura
"""

# 36_reliability.py
import numpy as np

def run_coupling_analysis():
    try:
        # 1. Maximaが出力したファイルをインポート
        with open("bridge_data.txt", "r") as f:
            crit_constant = float(f.read().strip())
    except FileNotFoundError:
        print("Error: bridge_data.txt が見つかりません。Maximaを先に実行してください。")
        return

    # 2. 実数としてのパラメータ設定 (m は整数である必要はない)
    m_est = 3.25  # 摩耗故障期の実数解
    eta_est = 1200.0
    
    # 3. Maximaの理論解を適用
    # t_limit = eta * (crit_constant)^(1/m)
    t_limit = eta_est * (crit_constant)**(1/m_est)
    
    print(f"--- 3Dプリンター保守限界解析 ---")
    print(f"Maximaからの引き渡し定数: {crit_constant}")
    print(f"形状パラメータ m (実数)  : {m_est}")
    print(f"尺度パラメータ eta       : {eta_est} 時間")
    print(f"信頼度99.9%維持の限界時間: {t_limit:.4f} 時間")

if __name__ == "__main__":
    run_coupling_analysis()