#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 14:50:39 2026

@author: iwamura
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def analyze_logistics_packing():
    # --- SymPy: パッキング効率の定式化 ---
    P_tesla = sp.symbols('P_tesla') # 受電電力 [W]
    E_hydride = sp.symbols('E_hydride') # ハイドライド1kgあたりの充填・固定エネルギー [J/kg]
    t_charge = sp.symbols('t_charge') # 滞在時間 [s]
    
    # 蓄積される商品の質量 M
    M_cargo = (P_tesla / E_hydride) * t_charge
    
    # --- 数値計算 ---
    # 設定: 1.3万トンを目標
    TARGET_MASS = 1.3e7 # [kg]
    # ハイドライド生成に必要な熱管理・固定エネルギー (想定 150 MJ/kg)
    E_HYDRIDE_VAL = 1.5e8 
    # テスラ送電による受電電力 (例: 15 GW = 1.5e10 W)
    P_TESLA_VAL = 1.5e10 
    
    # 滞在時間 (1日〜20日)
    days = np.linspace(1, 20, 100)
    seconds = days * 24 * 3600
    
    # 質量計算
    mass_kg = (P_TESLA_VAL / E_HYDRIDE_VAL) * seconds
    mass_tons = mass_kg / 1000

    # --- 可視化 ---
    plt.figure(figsize=(10, 6))
    plt.plot(days, mass_tons, 'b-', label='Cargo Hydride Mass')
    plt.axhline(y=13000, color='r', linestyle='--', label='Mission Target (13,000 Tons)')
    plt.axvline(x=14, color='g', linestyle=':', label='Max Stay Time (14 Days)')
    
    plt.xlabel('Stay Time at Venus Orbit (Days)')
    plt.ylabel('Hydride Packed (Tons)')
    plt.title('#14b: Energy to Matter Conversion (Tesla Power Charging)')
    plt.grid(True, which='both', ls='-', alpha=0.5)
    plt.legend()
    plt.show()

    # 交点の特定
    actual_days = (TARGET_MASS * E_HYDRIDE_VAL) / P_TESLA_VAL / (24*3600)
    print(f"=== #14b 物流整合性チェック ===")
    print(f"目標 1.3万トンのパッキングに必要な期間: {actual_days:.2f} 日")
    print(f"判定: 14日間の滞在枠内で収まるため、#48の爆速往復ミッションと【整合】します。")

if __name__ == "__main__":
    analyze_logistics_packing()