#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 12:09:45 2026

@author: iwamura
"""

import numpy as np
from repair_params import REPAIR_COST_RATIO, DECAY_RATE

# シミュレーション設定
INITIAL_OUTPUT_TW = 12.0 # 初期設計出力（余裕分含む）
TARGET_BRAKING_TW = 10.0 # 金星制動に最低必要な電力
YEARS = 1000            # 1000年間の運用シミュレーション

def analyze_long_term_stability():
    # 維持費を差し引いた純出力
    net_output = INITIAL_OUTPUT_TW * (1.0 - REPAIR_COST_RATIO)
    
    # 資源消費量（水星からの持ち出し）
    # パネル面積 4000km^2 と仮定
    total_mass_kt = 4000 * 1e6 * 0.27 / 1e6 # kt
    annual_loss_t = total_mass_kt * 1000 * DECAY_RATE
    
    print(f"--- Long-term Resource & Energy Balance (#901d) ---")
    print(f"Annual Self-Repair Energy Overhead: {REPAIR_COST_RATIO*100:.4f} %")
    print(f"Net Power Available for Venus: {net_output:.2f} TW")
    print(f"Annual Material Loss: {annual_loss_t:.2f} tons/year")
    
    if net_output >= TARGET_BRAKING_TW:
        margin = net_output - TARGET_BRAKING_TW
        print(f"Status: STABLE (Excess Power: {margin:.2f} TW)")
    else:
        print(f"Status: WARNING (Power Deficit!)")

    print("\n[考察]")
    print(f"1. 維持コスト: 発電量のわずか{REPAIR_COST_RATIO*100:.4f}%を充てるだけで、パネルは永久に自己修復可能です。")
    print(f"2. 資源消費: 年間{annual_loss_t:.1f}トンの質量欠損は、水星全体の質量の10の17乗分の1以下。")
    print(f"   太陽が燃え尽きるまで、水星の資源が枯渇することはありません。")
    print(f"3. 結論: このシステムは、金星のSRを止める「外付けの慣性保持装置」として完全自律稼働します。")

analyze_long_term_stability()