#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 21:16:01 2026

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import importlib
import model_functions 

# 常に最新の数式ファイルを読み込む
importlib.reload(model_functions)
from model_functions import calculate_yield

def run_analysis():
    # 物理定数（仮値）
    A = 1.0
    k = 1.38e-23
    sigma = 5.0e19
    DeltaE = 1.5e-21 
    
    # 刺激強度 S の範囲
    S_range = np.linspace(1e-3, 1e-1, 1000)
    
    # 計算実行
    try:
        yields = calculate_yield(S_range, A, DeltaE, k, sigma)
        
        plt.figure(figsize=(8, 5))
        plt.plot(S_range, yields, label='STAP Probability')
        plt.axvline(S_range[np.argmax(yields)], color='red', linestyle='--', label='Optimal Stress')
        plt.title("Reproducibility Gap in STAP Cells")
        plt.xlabel("Stress Intensity (pH / Pressure)")
        plt.ylabel("Yield")
        plt.legend()
        plt.grid(True)
        plt.show()
        
    except Exception as e:
        print(f"計算エラー: {e}")

if __name__ == "__main__":
    run_analysis()