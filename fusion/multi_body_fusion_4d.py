#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:46:21 2026

@author: iwamura
"""

import numpy as np

def localized_field_enhancement(radius, gap_distance):
    """
    ナノ粒子間の隙間（ギャップ）でどれだけ電界が強まるかの簡易計算
    radius: 粒子の半径
    gap_distance: 粒子同士の距離
    """
    # 粒子が近づくほど、その間の電界は幾何級数的に増大する
    enhancement_factor = (radius / gap_distance)**1.5 
    return enhancement_factor

# 10nmの粒子が 0.5nmまで近づいた場合
print(f"電界増幅率: {localized_field_enhancement(10, 0.5):.2f} 倍")