#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 11:47:30 2026

@author: iwamura
"""

import numpy as np

def calculate_net_energy(efficiency_gain, input_energy_kw):
    """
    核融合ユニットの出力計算
    efficiency_gain: 触媒による反応増幅率
    input_energy_kw: 起動・制御に必要なエネルギー (kW)
    """
    # 触媒が「壁」を10分の1に下げたと仮定した場合の出力
    output_energy = input_energy_kw * (efficiency_gain ** 2)
    return output_energy

# 触媒なし(1.0) vs 優れた触媒(10.0)
input_power = 10  # 10kWの入力
gain_none = calculate_net_energy(1.0, input_power)
gain_catalyst = calculate_net_energy(10.0, input_power)

print(f"標準的な効率: {gain_none} kW (元を取るのがやっと)")
print(f"触媒による効率: {gain_catalyst} kW (100倍の出力 = 街を支えられる)")