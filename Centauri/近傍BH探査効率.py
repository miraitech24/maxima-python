#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:18:24 2026

@author: iwamura
"""

# Python: 近傍BH探査の効率

import numpy as np

# 既知のBH密度
galaxy_radius = 50000  # 光年
galaxy_volume = (4/3) * np.pi * galaxy_radius**3
n_bh_galaxy = 1e8  # 1億個

bh_density = n_bh_galaxy / galaxy_volume
# = 1.9e-7 個/立方光年

# 探査範囲と発見期待値
def expected_bh_in_volume(radius_ly):
    volume = (4/3) * np.pi * radius_ly**3
    return volume * bh_density

radii = [10, 50, 100, 500, 1000]
for r in radii:
    n = expected_bh_in_volume(r)
    print(f"半径{r:4d}光年以内のBH期待値: {n:.2f}個")

# 結果:
# 半径 10光年以内: 0.0008個（ほぼゼロ）
# 半径 50光年以内: 0.1個（10%の確率で1個）
# 半径100光年以内: 0.8個（ほぼ1個）
# 半径500光年以内: 100個
# 半径1000光年以内: 800個