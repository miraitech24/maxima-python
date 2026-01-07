#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 15:26:43 2026

@author: iwamura
"""

import numpy as np

def deploy_fusion_grid(target_area_size=1000): # 1km四方
    # テスラ送電の限界距離 (8.pyより)
    LIMIT_DISTANCE = 50.0 

    # 1km四方をカバーするために必要な炉の数
    # 50m間隔の正三角形グリッド（ハニカム構造）が最も効率的
    num_units_needed = int((target_area_size / LIMIT_DISTANCE)**2 * (2/np.sqrt(3)))

    # 母船ヘスペロスからの投下精度 (誤差10mと仮定)
    drop_accuracy = 10.0

    print(f"■ 金星地表自動グリッド構築シミュレーション ■")
    print(f"カバー面積: {target_area_size}m x {target_area_size}m")
    print(f"必要リアクター数: {num_units_needed} 基")
    print(f"配置戦略: ハニカム・メッシュ構造")

    return num_units_needed

deploy_fusion_grid()