#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 09:53:03 2026

@author: iwamura
"""

# Python: 漫画のコマ割り輪郭を生成するサンプル
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_manga_page(chapter, page_number, panels, output_path):
    """漫画ページのコマ割り輪郭を生成"""
    width, height = 1800, 2600  # 漫画ページサイズ
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # コマ割りの設定
    margin = 40  # 余白
    panel_gap = 20  # コマ間の隙間
    
    for i, panel in enumerate(panels):
        x, y, w, h = panel['rect']
        # コマの枠線を描画
        draw.rectangle(
            [x, y, x+w, y+h],
            outline='black',
            width=4
        )
        # コマ番号を表示
        draw.text((x+10, y+10), str(i+1), fill='black')
        # 内容の説明を表示
        if 'description' in panel:
            draw.text((x+10, y+40), panel['description'], fill='gray')
        # セリフのプレースホルダー
        if 'dialogue' in panel:
            draw.text((x+10, y+h-60), panel['dialogue'], fill='blue')
        # 数値データのプレースホルダー
        if 'data' in panel:
            draw.text((x+10, y+h-120), panel['data'], fill='red')
    
    img.save(output_path)
    print(f"ページ生成: {output_path}")

# 第1話「種火」のコマ割り
chapter1_panels = [
    {'rect': [40, 40, 860, 600], 'description': '水星ダイソン環の全景', 'dialogue': '1.64PW...これが人類の新たな力だ', 'data': '出力: 1.64PW'},
    {'rect': [920, 40, 840, 600], 'description': '田中博士と時超えケンタ', 'dialogue': 'お前の名前は時超えケンタだ', 'data': 'AI起動: 0年'},
    {'rect': [40, 660, 560, 800], 'description': 'マイクロスロートの概念図', 'dialogue': '時空を曲げて距離を0にする', 'data': '遅延: 0秒'},
    {'rect': [620, 660, 560, 400], 'description': 'プロキシマbの赤い空', 'dialogue': '4.2光年先の星へ', 'data': '距離: 4.2光年'},
    {'rect': [1200, 660, 560, 400], 'description': '自己複製ロボット', 'dialogue': '私が拓く', 'data': 'ロボット数: 10万台'},
    {'rect': [620, 1080, 1140, 380], 'description': '旅立ち', 'dialogue': '21年後、プロキシマbで会おう', 'data': '航行時間: 21年'},
]

create_manga_page(1, 1, chapter1_panels, 'chapter1_page1.png')
