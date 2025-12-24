#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 16:47:36 2025

@author: iwamura
"""

import sys

def run_garbage_collection(file_name):
    try:
        with open(file_name.strip(), 'r') as f:
            # データのパース
            data = eval(f.read())
        
        award_names = ["Nobel Economics", "Fields Medal", "Practical (Stats)"]
        
        # 評価アルゴリズム（重み付け）
        # [K: 知識の美しさ, U: 実用的価値, B: 偏向・副作用, M: 維持コスト]
        # 実務家視点：実用性重視、偏りとコストを厳しく引く
        w = [0.05, 0.95, -0.60, -0.30]
        
        print(f"{'Award Name':<18} | {'Score':>6} | {'Status'}")
        print("-" * 40)
        
        for name, metrics in zip(award_names, data):
            # 加重平均によるスコアリング
            score = sum(m * wi for m, wi in zip(metrics, w))
            # スコアがマイナス、または実用性(U)が閾値(0.3)以下を「不要」と判定
            status = "REDUNDANT (不要)" if score < 0 or metrics[1] < 0.3 else "VALUABLE"
            print(f"{name:<18} | {score:>6.2f} | {status}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_garbage_collection(sys.argv[1])