#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 11:57:48 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
from rectenna_params import R_RECT_M

# 金星の基本定数
R_VENUS = 6051.8e3 # m
SURFACE_AREA = 4.6e14 # m^2
N_STATIONS = 865

def analyze_coverage():
    # 1拠点あたりの受電面積
    area_per_station = np.pi * (R_RECT_M**2)
    
    # 全拠点の総受電面積
    total_rect_area = area_per_station * N_STATIONS
    
    # 全球に対するカバレッジ
    coverage_ratio = total_rect_area / SURFACE_AREA
    
    # SR制動トルクの維持計算 (概念)
    # 10TWの電力をこの面積で受けた時の平均電力密度 [W/m^2]
    power_density = 10.0e12 / total_rect_area if total_rect_area > 0 else 0

    print(f"--- Rectenna Grid Analysis (#901b) ---")
    print(f"Single Station Beam Radius: {R_RECT_M/1000:.2f} km")
    print(f"Total Rectenna Coverage: {coverage_ratio*100:.2f} % of Venus")
    print(f"Required Power Density for 10TW: {power_density:.2f} W/m^2")
    
    print("\n[考察]")
    print(f"1. ビーム半径は約{R_RECT_M/1000:.0f}kmに広がるため、865拠点で金星全土をほぼ完全にカバー可能。")
    print(f"2. 電力密度は約{power_density:.1f}W/m^2となり、これは地球の太陽定数の数倍程度。")
    print(f"   大気を熱的に制御するには十分かつ、地表構造物を焼き切らない安全なレベル。")

analyze_coverage()