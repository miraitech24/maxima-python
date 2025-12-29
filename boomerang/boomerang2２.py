#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 16:13:05 2025

@author: iwamura
"""

import subprocess
import pandas as pd
import matplotlib.pyplot as plt

def run_reform_simulation():
    # --- STEP 1: Maximaを実行してデータを生成 ---
    print("Maxima running: Calculating the 'Fiscal Freedom' roadmap...")
    subprocess.run(["maxima", "--very-quiet", "-r", 'load("reform.mac")$'])

    # --- STEP 2: 生成されたCSVを読み込む (ここが引き渡し) ---
    df = pd.read_csv("reform_results.csv")
    
    # --- STEP 3: 比較用の「ザイム真理教（緊縮）」データを作成 ---
    # 成長率1%固定、負担率35%固定
    df['zaimu_gdp'] = 550.0 * (1.01 ** df['year'])
    df['zaimu_tax'] = df['zaimu_gdp'] * 0.35
    df['zaimu_cum_tax'] = df['zaimu_tax'].cumsum()

    # --- STEP 4: 可視化 ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 左図：GDPの推移（蛇口が太くなる様子）
    ax1.plot(df['year'], df['gdp'], 'b-o', label='Reform: GDP Growth (d=0.9)', lw=2)
    ax1.plot(df['year'], df['zaimu_gdp'], 'r--', label='Status Quo: Stagnation (d=0.5)')
    ax1.set_title("GDP Projection: Opening the Faucet")
    ax1.set_ylabel("GDP (Trillion Yen)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 右図：累計税収（ブーメラン着弾の証明）
    ax2.plot(df['year'], df['cumulative_tax'], 'g-s', label='Reform: Cumulative Tax', lw=2)
    ax2.plot(df['year'], df['zaimu_cum_tax'], 'r--', label='Status Quo: Cumulative Tax')
    
    # 逆転（クロスオーバー）ポイントの自動検出
    crossover = df[df['cumulative_tax'] > df['zaimu_cum_tax']].iloc[0] if any(df['cumulative_tax'] > df['zaimu_cum_tax']) else None
    if crossover is not None:
        ax2.annotate('Break Even!', xy=(crossover['year'], crossover['cumulative_tax']), 
                     xytext=(crossover['year']-5, crossover['cumulative_tax']+1000),
                     arrowprops=dict(facecolor='black', shrink=0.05))

    ax2.set_title("Cumulative Tax Revenue: The Boomerang Proof")
    ax2.set_ylabel("Total Tax (Trillion Yen)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

# 実行
if __name__ == "__main__":
    run_reform_simulation()