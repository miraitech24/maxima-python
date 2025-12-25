#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 25 12:55:26 2025

@author: iwamura
"""

import numpy as np
import matplotlib.pyplot as plt
import formula
import importlib

def run_log_sim():
    importlib.reload(formula)
    
    # 1年から100万年まで。対数軸で精度を保つため刻みを増やす
    t_axis = np.logspace(0, 6, 10000) 
    T = 15.0 # 初期温度
    history = []
    
    t_prev = t_axis[0]
    for t in t_axis:
        dt = t - t_prev
        
        # 軌道要素
        e = 0.028 + 0.012 * np.sin(2 * np.pi * t / 100000)
        eps = np.radians(23.4 + 0.7 * np.sin(2 * np.pi * t / 41000))
        omega = 2 * np.pi * t / 23000
        
        # 条件: 400ppm + アルベド (極端な発散を防ぐため閾値を調整)
        dF = 14.5
        alpha = 0.3 if T > 5.0 else 0.5 

        # 微分係数取得と更新 (偏差 T-15 を入力)
        dTdt = formula.get_dTdt(T-15, e, eps, omega, dF, alpha)
        
        # 安全策: dTdt が大きくなりすぎないようリミッターをかける
        T += np.clip(dTdt * dt, -2.0, 2.0)
        history.append(T)
        t_prev = t

    plt.figure(figsize=(12, 6))
    plt.plot(t_axis, history, color='darkgreen', linewidth=2)
    plt.xscale('log')
    plt.axhline(y=10.0, color='red', linestyle='--', label='Glacial Limit')
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.title("Log-scale Climate Stability Simulation", fontsize=14)
    plt.xlabel("Years from Present (Log Scale)", fontsize=12)
    plt.ylabel("Global Temperature (°C)", fontsize=12)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    run_log_sim()