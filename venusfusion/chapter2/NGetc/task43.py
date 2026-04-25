#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 13:17:38 2026

@author: iwamura
"""

# task43_logistics.py
import numpy as np

# 1. エネルギー計算
E_required = 0.5 * 100 * (2957.69)**2 # 1発あたりの運動エネルギー (J)
P_recv = 8.0e6 # 課題26で得た受電電力 (8MW)

# 2. サイクルタイムの算出
charge_time = E_required / P_recv / 60 # 分単位
capsules_per_day = (24 * 60) / charge_time

# 3. 3Dプリンター生産能力の境界（仮定：1個製造に2時間）
print(f"1発射あたりの充電時間: {charge_time:.1f} 分")
print(f"1日あたりの最大送出数: {capsules_per_day:.1f} 発")
print(f"1日あたりの総送出エネルギー量: {100 * capsules_per_day} kg/day")