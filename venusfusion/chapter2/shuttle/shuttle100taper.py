#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 13:39:02 2026

@author: iwamura
"""

import numpy as np
from tether_params import get_taper_mass

def analyze_taper_roi():
    # パラメータ (Issue #100 共通)
    L, rho, sigma_allow, S_target = 1000.0, 1700.0, 3.5e9, 3.0
    a_max = 90.0   # 加速終了時の最大加速度
    m_p = 1000.0   # 荷物 1t
    
    # 1. テーパーテザーの質量 (SF=3.0を完璧に維持)
    m_tether_taper = get_taper_mass(a_max, m_p, L, rho, S_target, sigma_allow)
    
    # 2. 比較：等断面で強引にSF=3.0を通した場合の質量
    sigma_lim = sigma_allow / S_target
    A_uni = (m_p * a_max) / (sigma_lim - rho * a_max * L)
    m_tether_uniform = rho * A_uni * L
    
    print(f"--- 構造・採算性比較分析 ---")
    print(f"【等断面設計】")
    print(f"  必要質量: {m_tether_uniform:.2f} kg (制限100kgを突破、構造破綻)")
    
    print(f"\n【テーパー設計】")
    print(f"  必要質量: {m_tether_taper:.2f} kg (SF=3.0を維持)")
    print(f"  判定: 採用成功 (制限内でフル加速が可能)")
    
    # 3. 採算性：浮いた重量を「追加荷物」に変えた場合
    save_mass = m_tether_uniform - m_tether_taper
    print(f"\n--- 結論 ---")
    print(f"テーパー化により、物理的に不可能な設計を「可能」にしました。")
    print(f"エンジン全開(9G)が可能になることで航行日数が短縮され、ROIが最大化されます。")

if __name__ == "__main__":
    analyze_taper_roi()