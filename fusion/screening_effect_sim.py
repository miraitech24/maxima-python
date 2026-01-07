#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:38:31 2026

@author: iwamura
"""

# 4D融合 vs ガソリン燃焼のエネルギー密度比較
ev_to_joule = 1.602e-19
avogadro = 6.022e23

# 1回の4D反応で出るエネルギー (MeV -> Joule)
energy_4d_joule = 47.6 * 1e6 * ev_to_joule

# 1モルの4D反応 (重水素8g分) の総エネルギー
total_energy_4d = (avogadro / 4) * energy_4d_joule

# ガソリンの燃焼エネルギー (約35MJ/L, 1L=約750gとする)
energy_gasoline_per_kg = 46.4e6 # J/kg

print(f"重水素8gから出るエネルギー: {total_energy_4d:.2e} Joules")
print(f"同じエネルギーを得るのに必要なガソリン: {total_energy_4d / energy_gasoline_per_kg:.2e} kg")