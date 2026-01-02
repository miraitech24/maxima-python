#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 12:58:04 2026

@author: iwamura
"""

import sys
import json
import numpy as np
import os
from stl import mesh

def generate_feed_stl(json_file):
    # 1. JSONの読み込み
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 本来は最適化計算の結果を使うが、ここではメッセージに合わせて固定値
        h_a, h_b = 20.0, 15.0 
    except Exception as e:
        print(f"JSON読み込みエラー: {e}")
        return

    # 2. 直方体作成用の関数
    def create_box(x_range, y_range, z_range):
        vertices = np.array([
            [x_range[0], y_range[0], z_range[0]], [x_range[1], y_range[0], z_range[0]],
            [x_range[1], y_range[1], z_range[0]], [x_range[0], y_range[1], z_range[0]],
            [x_range[0], y_range[0], z_range[1]], [x_range[1], y_range[0], z_range[1]],
            [x_range[1], y_range[1], z_range[1]], [x_range[0], y_range[1], z_range[1]]
        ])
        faces = np.array([
            [0,3,1], [1,3,2], [0,4,7], [0,7,3], [4,5,6], [4,6,7],
            [5,1,2], [5,2,6], [2,3,6], [3,7,6], [0,1,5], [0,5,4]
        ])
        box = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                box.vectors[i][j] = vertices[f[j],:]
        return box

    # メッシュ生成
    box_a = create_box([0, 10], [0, 10], [0, h_a])
    box_b = create_box([0, 10], [0, 10], [h_a, h_a + h_b])
    combined = mesh.Mesh(np.concatenate([box_a.data, box_b.data]))

    # 3. 保存先の決定（絶対パスで指定すると確実です）
    # 入力ファイル名に基づいた名前（feed_model.stl）にする
    output_filename = os.path.abspath(json_file.replace('.json', '.stl'))
    
    combined.save(output_filename)
    
    print(f"飼料A ({h_a}) と 飼料B ({h_b}) の比率に基づいたSTLを生成しました。")
    print(f"保存先: {output_filename}") # ここで保存場所をフルパスで表示します

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %run Fodder1.py <json_file>")
    else:
        generate_feed_stl(sys.argv[1])