#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 11:23:55 2025

@author: iwamura
"""

import sys
import matplotlib.pyplot as plt

def solve_and_plot(file_name):
    # ファイルからデータをインポート
    with open(file_name.strip(), 'r') as f:
        data = eval(f.read().replace("{", "[").replace("}", "]"))
    
    # 戦略名と社会利得の計算
    labels = ['(C,C)', '(C,D)', '(D,C)', '(D,D)']
    utilities = []
    
    for row in data:
        for cell in row:
            utilities.append(sum(cell))
    
    # Matplotlibを用いた可視化
    plt.figure(figsize=(8, 5))
    colors = ['skyblue', 'orange', 'orange', 'salmon']
    bars = plt.bar(labels, utilities, color=colors)
    
    plt.title("Social Total Utility by Strategy")
    plt.xlabel("Strategy Combination (Player A, Player B)")
    plt.ylabel("Total Utility (Sum)")
    plt.axhline(0, color='black', linewidth=0.8)
    
    # 数値をバーの上に表示
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval - 0.5, yval, ha='center', va='top')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_and_plot(sys.argv[1])