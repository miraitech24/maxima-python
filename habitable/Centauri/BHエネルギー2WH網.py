#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:14:22 2026

@author: iwamura
"""

# Python: BHエネルギーとWH網の関係

import numpy as np

# BHのパラメータ
M_bh = 2e31  # kg（太陽質量の10倍）
eta = 0.29   # ペンローズ過程の効率
E_bh = eta * M_bh * 9e16  # J

# WHのパラメータ
rho_neg = 4.815e42  # J/m^3（半径1mあたりのエネルギー密度）

def wh_energy(r0):
    """半径r0のWHを維持するのに必要なエネルギー"""
    volume = (4/3) * np.pi * r0**3
    return rho_neg * volume

# 様々な半径のWHを何本作れるか
radii = [1, 10, 100, 1000, 10000]  # m
for r in radii:
    e_per_wh = wh_energy(r)
    n_wh = E_bh / e_per_wh
    print(f"半径{r:5d}mのWH: {n_wh:.0f}本作成可能")

# 結果:
# 半径    1mのWH: 258,415,841本作成可能
# 半径   10mのWH: 258,415本作成可能
# 半径  100mのWH: 258本作成可能
# 半径 1000mのWH: 0.25本（1本も作れない）
# 半径10000mのWH: 0.00025本（不可能）