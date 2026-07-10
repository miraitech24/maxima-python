#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:02:52 2026

@author: iwamura
"""

# 負のエネルギー密度の空間分布
import numpy as np

rho_negative = -4.815e42  # J/m^3（1mスロート1個あたり）
volume_per_wh = 10.0  # m^3（影響範囲）

# 空間の「耐荷重」計算
# 真空崩壊の閾値: -1e45 J/m^3（理論値）
vacuum_collapse_threshold = -1e45

max_wh_per_volume = abs(vacuum_collapse_threshold / rho_negative)
# = 1e45 / 4.815e42 ≈ 208

print(f"真空崩壊を起こさずに配置可能な最大WH数: {max_wh_per_volume:.0f} 個/m³")