#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 15:55:57 2025

@author: iwamura
"""

import sys
import matplotlib.pyplot as plt

def solve_and_plot(file_name):
    with open(file_name.strip(), 'r') as f:
        # Maximaのリスト形式をPythonリストに変換
        data = eval(f.read().replace("{", "[").replace("}", "]"))
    
    labels = ['(C,C)\nOptimal', '(C,D)', '(D,C)', '(D,D)\nNash Eq.']
    p1_scores = [cell[0] for row in data for cell in row]
    social_scores = [sum(cell) for row in data for cell in row]
    
    x = range(len(labels))
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 社会的総利得（棒グラフ）
    ax1.bar(x, social_scores, color='lightgray', label='Social Total Utility', alpha=0.5)
    ax1.set_ylabel('Total Utility (Social)')
    
    # プレイヤー1の利得（折れ線グラフ）
    ax2 = ax1.twinx()
    ax2.plot(x, p1_scores, color='red', marker='o', label='Player 1 Individual Payoff')
    ax2.set_ylabel('Individual Payoff (P1)')

    plt.xticks(x, labels)
    plt.title("Gap between Individual Rationality and Social Optimality")
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
    plt.grid(axis='y', linestyle='--')
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        solve_and_plot(sys.argv[1])