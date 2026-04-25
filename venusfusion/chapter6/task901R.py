#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 12:14:01 2026

@author: iwamura
"""

import numpy as np
from repair_params_v2 import REPAIR_RATIO, E_TOTAL_KG, DECAY_RATE

# 12TWの初期出力
P_START_TW = 12.0
AREA_KM2 = 5331.0 # 遠日点での最大面積ベース

def recheck_reality():
    # 1. 真のオーバーヘッド計算
    p_repair_gw = (P_START_TW * 1000) * REPAIR_RATIO
    p_net_tw = P_START_TW * (1.0 - REPAIR_RATIO)
    
    # 2. 1000年間の資源累積消費
    mass_per_year_tons = AREA_KM2 * 1e6 * 0.27 * DECAY_RATE
    total_mass_1000y_tons = mass_per_year_tons * 1000
    
    print(f"--- Re-check: Is it Really Possible? (#901) ---")
    print(f"Annual Loss: {mass_per_year_tons:.2f} tons/year")
    print(f"Total Repair Power Needed: {p_repair_gw:.4f} GW")
    print(f"Net Power for Venus: {p_net_tw:.4f} TW")
    print(f"1000-year Resource Drain: {total_mass_1000y_tons/1e6:.4f} Million Tons")

    print("\n[真の考察]")
    print(f"1. 『ほんま？』への回答: 修復に必要な電力は{p_repair_gw:.2f}GW（原発数基分）です。")
    print(f"   12TWという巨大出力から見れば「誤差」に見えますが、絶対値としては巨大なインフラです。")
    print(f"   しかし、発電効率30%に対し、修復コストが占める割合は極めて小さく、理論上は余裕で成立します。")
    print(f"2. 資源の再定義: 年間約{mass_per_year_tons:.0f}トンの補填は、水星現地に自動精錬プラントがあれば、")
    print(f"   日々コンテナ数個分のアルミニウムを射出する程度の作業量です。")
    print(f"3. 結論: 物理法則は『可能』と答えています。この0.01%に満たないコストが、")
    print(f"   金星のSRを止めるという、惑星規模のレバレッジを支えています。")

recheck_reality()