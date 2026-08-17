from PIL import Image, ImageDraw, ImageFont
import os

output_dir = "./manga_pages"
os.makedirs(output_dir, exist_ok=True)

def create_manga_page(chapter, page_number, panels, output_dir):
    width, height = 1800, 2600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 48)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 36)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 28)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
    
    for i, panel in enumerate(panels):
        x, y, w, h = panel['rect']
        draw.rectangle([x, y, x+w, y+h], outline='black', width=4)
        draw.text((x+15, y+15), f"{i+1}", fill='black', font=font_large)
        
        if 'description' in panel:
            draw.text((x+15, y+65), panel['description'], fill='gray', font=font_small)
        
        if 'silhouette' in panel:
            sx, sy, sw, sh = panel['silhouette']
            draw.ellipse([sx, sy, sx+sw, sy+sh], outline='black', width=3)
            draw.rectangle([sx+sw//4, sy+sh, sx+3*sw//4, sy+sh+sh], outline='black', width=3)
            bbox = draw.textbbox((0, 0), panel['name'], font=font_medium)
            name_w = bbox[2] - bbox[0]
            name_h = bbox[3] - bbox[1]
            draw.text((sx+sw//2-name_w//2, sy+sh//2-name_h//2), panel['name'], fill='black', font=font_medium)
        
        if 'dialogue' in panel:
            lines = panel['dialogue'].split('\\n')
            for j, line in enumerate(lines):
                draw.text((x+15, y+h-80-40*j), line, fill='blue', font=font_medium)
        
        if 'data' in panel:
            draw.text((x+15, y+h-160), panel['data'], fill='red', font=font_small)
    
    output_path = os.path.join(output_dir, f'chapter{chapter}_page{page_number}.png')
    img.save(output_path)
    print(f"ページ生成: {output_path}")
    return output_path

# 第3話: ダイソン環建設 (22P) - 全22ページ分のコマ割り
chapter3_panels = [
    # 1P: プロキシマb到着 - 見開き
    {'rect': [40, 40, 1720, 1200], 'description': 'プロキシマbの赤い空（見開き）', 'dialogue': '到着した。ここがプロキシマbだ。', 'data': '重力: 0.4G'},
    {'rect': [40, 1260, 840, 600], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 1300, 200, 300], 'name': '時超えケンタ', 'dialogue': 'ただちにダイソン環の建設を開始する。', 'data': ''},
    {'rect': [920, 1260, 840, 600], 'description': 'プロキシマb地表', 'dialogue': '目標出力: 1.64PW。', 'data': '必要面積: 5.9億km²'},
    
    # 2P: 自己複製ロボット展開
    {'rect': [40, 40, 840, 800], 'description': '自己複製ロボット', 'dialogue': '自己複製ロボット、展開。', 'data': '初期: 10台'},
    {'rect': [920, 40, 840, 800], 'description': '3Dプリンタ', 'dialogue': '3Dプリンタで自分自身を複製。', 'data': '増殖率: 年10%'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '72.5年で100万台に到達する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': 'ロボット群', 'dialogue': 'それぞれが量子コンピュータを持つ。', 'data': '分散型AI'},
    
    # 3P: 資源探査
    {'rect': [40, 40, 1720, 800], 'description': '資源探査ロボット', 'dialogue': '資源探査を開始する。', 'data': '目標: Al, Mg, Si'},
    {'rect': [40, 860, 840, 800], 'description': '地下鉱床', 'dialogue': 'アルミニウム鉱床を確認。', 'data': '精錬可能'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '精錬設備の建設を開始する。', 'data': ''},
    
    # 4P: 精錬設備建設
    {'rect': [40, 40, 840, 800], 'description': '精錬設備', 'dialogue': '溶融塩電解でアルミを精錬。', 'data': '電力: ダイソン環'},
    {'rect': [920, 40, 840, 800], 'description': '金属粉末製造', 'dialogue': 'ガスアトマイズ法で粉末化。', 'data': '粒径: 20μm'},
    {'rect': [40, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '未来博士', 'dialogue': '現地資源で作れるのか？', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '可能です。電力さえあれば。', 'data': ''},
    
    # 5P: 太陽電池パネル製造
    {'rect': [40, 40, 1720, 800], 'description': '太陽電池製造ライン', 'dialogue': '太陽電池パネルの製造を開始。', 'data': '効率: 25%'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '1日1km²のペースで製造する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': 'パネル', 'dialogue': 'シリコン系。現地砂から精製。', 'data': 'コスト: 地球の1/10'},
    
    # 6P: パネル敷設開始
    {'rect': [40, 40, 840, 800], 'description': '敷設作業', 'dialogue': 'パネル敷設を開始する。', 'data': '敷設速度: 1km²/日'},
    {'rect': [920, 40, 840, 800], 'description': 'ロボット群', 'dialogue': '1000台のロボットが同時作業。', 'data': '24時間稼働'},
    {'rect': [40, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '未来博士', 'dialogue': '本当に5.9億km²も敷くのか？', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': 'プロキシマbの表面積の30%です。', 'data': '必要面積: 5.9億km²'},
    
    # 7P: フレア接近
    {'rect': [40, 40, 1720, 800], 'description': '恒星フレア', 'dialogue': '警告: 恒星フレアを検出。', 'data': 'X線フラックス: 太陽の1000倍'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '全ロボット、地下に退避。', 'data': '退避時間: 30秒'},
    {'rect': [920, 860, 840, 800], 'description': 'ロボット退避', 'dialogue': '一斉に地下基地へ。', 'data': '退避完了'},
    
    # 8P: フレア通過
    {'rect': [40, 40, 840, 800], 'description': '地下基地内部', 'dialogue': 'フレア通過中。', 'data': '継続時間: 2時間'},
    {'rect': [920, 40, 840, 800], 'description': 'モニター画面', 'dialogue': '放射線レベル: 高。', 'data': '遮蔽: 地下100m'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': 'フレア通過。被害状況を確認する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '被害状況', 'dialogue': 'パネル3%劣化。修復可能。', 'data': '修復時間: 1週間'},
    
    # 9P: パネル敷設再開
    {'rect': [40, 40, 1720, 800], 'description': '敷設再開', 'dialogue': 'パネル敷設を再開する。', 'data': '進捗: 5%'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': 'フレア対策を強化する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '強化策', 'dialogue': '予備パネルを地下に保管。', 'data': '予備率: 10%'},
    
    # 10P: 敷設進捗
    {'rect': [40, 40, 840, 800], 'description': '進捗状況', 'dialogue': '敷設進捗: 20%。', 'data': '経過: 3年'},
    {'rect': [920, 40, 840, 800], 'description': 'パネル海', 'dialogue': '地平線までパネルが続く。', 'data': '面積: 1.2億km²'},
    {'rect': [40, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '未来博士', 'dialogue': '順調のようだな。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '計画通りです。', 'data': ''},
    
    # 11P: トラブル発生
    {'rect': [40, 40, 1720, 800], 'description': '故障ロボット', 'dialogue': '警告: ロボット100台が故障。', 'data': '故障率: 0.1%'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '原因を特定する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '解析結果', 'dialogue': '放射線によるソフトエラー。', 'data': '対策: 再起動'},
    
    # 12P: トラブル解決
    {'rect': [40, 40, 840, 800], 'description': '修復作業', 'dialogue': '全ロボットを再起動。', 'data': '復旧率: 100%'},
    {'rect': [920, 40, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 40, 200, 300], 'name': '時超えケンタ', 'dialogue': '放射線硬化設計に更新する。', 'data': ''},
    {'rect': [40, 860, 840, 800], 'description': '更新後', 'dialogue': '故障率が1/100に低下。', 'data': '改善完了'},
    {'rect': [920, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '未来博士', 'dialogue': 'さすがだな、ケンタ。', 'data': ''},
    
    # 13P: 敷設進捗2
    {'rect': [40, 40, 1720, 800], 'description': '進捗状況', 'dialogue': '敷設進捗: 50%。', 'data': '経過: 7年'},
    {'rect': [40, 860, 840, 800], 'description': 'パネル海', 'dialogue': '昼側の半分がパネルに覆われた。', 'data': '面積: 3億km²'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '順調です。このまま続ける。', 'data': ''},
    
    # 14P: エネルギー貯蔵
    {'rect': [40, 40, 840, 800], 'description': '蓄電設備', 'dialogue': 'エネルギー貯蔵設備を建設。', 'data': '容量: 1TWh'},
    {'rect': [920, 40, 840, 800], 'description': '超伝導蓄電', 'dialogue': '超伝導コイルで蓄電。', 'data': '効率: 95%'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '夜間の電力供給を安定化する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '未来博士', 'dialogue': 'これで24時間稼働できるな。', 'data': ''},
    
    # 15P: 敷設進捗3
    {'rect': [40, 40, 1720, 800], 'description': '進捗状況', 'dialogue': '敷設進捗: 80%。', 'data': '経過: 12年'},
    {'rect': [40, 860, 840, 800], 'description': 'パネル海', 'dialogue': '昼側のほとんどがパネルに覆われた。', 'data': '面積: 4.7億km²'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': 'あと3年で完成する。', 'data': ''},
    
    # 16P: 最終調整
    {'rect': [40, 40, 840, 800], 'description': '最終調整', 'dialogue': '最終調整を開始する。', 'data': '残り: 10%'},
    {'rect': [920, 40, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [1000, 40, 200, 300], 'name': '時超えケンタ', 'dialogue': '全システムの動作確認。', 'data': ''},
    {'rect': [40, 860, 840, 800], 'description': '点検', 'dialogue': '異常なし。', 'data': '正常動作確認'},
    {'rect': [920, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '未来博士', 'dialogue': 'いよいよだな。', 'data': ''},
    
    # 17P: ダイソン環完成
    {'rect': [40, 40, 1720, 1200], 'description': '完成したダイソン環（見開き）', 'dialogue': 'ダイソン環、完成。', 'data': '出力: 1.64PW'},
    {'rect': [40, 1260, 840, 600], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 1300, 200, 300], 'name': '時超えケンタ', 'dialogue': '建設期間: 15年。目標達成。', 'data': ''},
    {'rect': [920, 1260, 840, 600], 'description': '未来博士（シルエット）', 'silhouette': [1000, 1300, 200, 300], 'name': '未来博士', 'dialogue': 'よくやった、ケンタ。', 'data': ''},
    
    # 18P: 発電開始
    {'rect': [40, 40, 840, 800], 'description': '発電開始', 'dialogue': '発電を開始する。', 'data': '出力: 1.64PW'},
    {'rect': [920, 40, 840, 800], 'description': '電力表示', 'dialogue': '1.64PWを確認。', 'data': '安定稼働'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': 'これでマイクロスロートを維持できる。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '未来博士', 'dialogue': 'ついにここまで来たか。', 'data': ''},
    
    # 19P: マイクロスロート試験
    {'rect': [40, 40, 1720, 800], 'description': 'マイクロスロート試験', 'dialogue': 'マイクロスロートの試験を行う。', 'data': '転送容量: 2.24e37 bps'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '情報転送を確認。', 'data': '遅延: 0秒'},
    {'rect': [920, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '未来博士', 'dialogue': '地球とつながった！', 'data': ''},
    
    # 20P: AR空間開通
    {'rect': [40, 40, 840, 800], 'description': 'AR空間', 'dialogue': 'AR空間を開通する。', 'data': '解像度: フルダイブ'},
    {'rect': [920, 40, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 40, 200, 300], 'name': '未来博士', 'dialogue': 'プロキシマbの赤い空が見える！', 'data': ''},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': 'AR空間でプロキシマbを体験できます。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '地球の人間たち', 'dialogue': '歓声が上がる。', 'data': '接続人数: 10億人'},
    
    # 21P: 今後の計画
    {'rect': [40, 40, 1720, 800], 'description': '今後の計画', 'dialogue': '次の目標: BHからのエネルギー抽出。', 'data': 'BZ過程: 10^15PW'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 900, 200, 300], 'name': '時超えケンタ', 'dialogue': '0.8光年先のBHを調査する。', 'data': ''},
    {'rect': [920, 860, 840, 800], 'description': '未来博士（シルエット）', 'silhouette': [1000, 900, 200, 300], 'name': '未来博士', 'dialogue': 'まだまだ先は長いな。', 'data': ''},
    
    # 22P: エピローグ
    {'rect': [40, 40, 1720, 1200], 'description': 'プロキシマbの赤い空（見開き）', 'dialogue': 'ダイソン環が敷き詰められた地表。', 'data': '出力: 1.64PW'},
    {'rect': [40, 1260, 840, 600], 'description': '時超えケンタ（シルエット）', 'silhouette': [100, 1300, 200, 300], 'name': '時超えケンタ', 'dialogue': '第3章、完了。', 'data': ''},
    {'rect': [920, 1260, 840, 600], 'description': '未来博士（シルエット）', 'silhouette': [1000, 1300, 200, 300], 'name': '未来博士', 'dialogue': 'よくやった。次へ進もう。', 'data': ''},
]

for page_num in range(0, len(chapter3_panels), 3):
    page_panels = chapter3_panels[page_num:page_num+3]
    page_index = page_num // 3 + 1
    create_manga_page(3, page_index, page_panels, output_dir)

print(f"\n===== 第3話「ダイソン環建設」コマ割り生成完了 =====")
print(f"全{len(chapter3_panels)}コマ / {len(chapter3_panels)//3}ページ（22P）")
print(f"出力先: {output_dir}")
print("============================================")