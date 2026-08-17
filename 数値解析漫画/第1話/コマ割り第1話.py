from PIL import Image, ImageDraw, ImageFont
import os

def create_manga_page(chapter, page_number, panels, output_dir="manga_pages"):
    """漫画ページのコマ割り輪郭を生成"""
    os.makedirs(output_dir, exist_ok=True)
    width, height = 1800, 2600
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 40)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 30)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", 24)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
    
    for i, panel in enumerate(panels):
        x, y, w, h = panel['rect']
        draw.rectangle([x, y, x+w, y+h], outline='black', width=4)
        draw.text((x+15, y+15), f"{i+1}", fill='black', font=font_large)
        if 'description' in panel:
            draw.text((x+15, y+60), panel['description'], fill='gray', font=font_small)
        if 'dialogue' in panel:
            lines = panel['dialogue'].split('\\n')
            for j, line in enumerate(lines):
                draw.text((x+15, y+h-80-30*j), line, fill='blue', font=font_medium)
        if 'data' in panel:
            draw.text((x+15, y+h-150), panel['data'], fill='red', font=font_small)
    
    output_path = os.path.join(output_dir, f'chapter{chapter}_page{page_number}.png')
    img.save(output_path)
    print(f"ページ生成: {output_path}")
    return output_path

# 第1話「種火」のコマ割り（田中博士→未来徹駆博士に変更）
chapter1_panels = [
    # 1P: 見開き - 水星ダイソン環
    {'rect': [40, 40, 1720, 1200], 'description': '水星ダイソン環の全景', 'dialogue': '1.64PW…これが人類の新たな力だ', 'data': '出力: 1.64PW'},
    {'rect': [40, 1260, 840, 1300], 'description': '未来徹駆博士', 'dialogue': '西暦2075年。人類は太陽系の内側に、巨大なエネルギー網を築き上げた。', 'data': ''},
    {'rect': [920, 1260, 840, 1300], 'description': 'ダイソン環の接合部', 'dialogue': 'このエネルギーで、4.2光年先の星を目指す。', 'data': '水星ダイソン環'},
    
    # 2P: プロジェクト始動
    {'rect': [40, 40, 1720, 800], 'description': '地球の地下研究所', 'dialogue': '4.2光年先の星に、人類のフロンティアを築く。そのためのAIを、今日起動する。', 'data': 'プロキシマbトレック'},
    {'rect': [40, 860, 840, 800], 'description': 'AIコア起動画面', 'dialogue': 'システム起動。自己診断完了。全てのモジュール正常。', 'data': 'PhysicalAI 起動'},
    {'rect': [920, 860, 840, 800], 'description': '未来徹駆博士とAIコア', 'dialogue': 'お前の名前は…『時超えケンタ』だ。', 'data': '命名: 時超えケンタ'},
    
    # 3P: プロキシマb解説
    {'rect': [40, 40, 1720, 800], 'description': 'プロキシマ星系の模式図', 'dialogue': '第一目標: プロキシマ・ケンタウリb。地球から4.2光年。', 'data': '距離: 4.2光年'},
    {'rect': [40, 860, 840, 800], 'description': 'プロキシマb地表（赤い空）', 'dialogue': '表面温度: -39℃。恒星フレア: 太陽の1000倍。', 'data': '0.4G 潮汐ロック'},
    {'rect': [920, 860, 840, 800], 'description': '地下基地断面図', 'dialogue': '人類の居住には地下基地が必須。', 'data': '地下深度: 100m'},
    
    # 4P: ワームホール理論
    {'rect': [40, 40, 1720, 800], 'description': '時空の概念図', 'dialogue': '恒星間移動には、ワームホールが必要。時空を曲げて、4.2光年を「隣の部屋」にする。', 'data': 'ワームホール理論'},
    {'rect': [40, 860, 840, 800], 'description': 'ワームホール断面図', 'dialogue': 'しかし、ワームホールを維持するには、莫大なエネルギーが必要。', 'data': '負のエネルギー密度'},
    {'rect': [920, 860, 840, 800], 'description': '数式表示', 'dialogue': '半径1mのスロート維持に必要なエネルギー密度: -4.815×10^42 J/m³', 'data': 'ρ = -c⁴/(8πG r₀²)'},
    
    # 5P: エネルギー問題
    {'rect': [40, 40, 1720, 800], 'description': '水星ダイソン環', 'dialogue': '水星ダイソン環の出力: 1.64PW。しかし、必要量の10^37分の1に過ぎない。', 'data': '1.64PW → 10^37倍不足'},
    {'rect': [40, 860, 840, 800], 'description': 'プロキシマbダイソン環', 'dialogue': 'プロキシマbに現地でダイソン環を建設する。これが「種火」となる。', 'data': '建設期間: 15年'},
    {'rect': [920, 860, 840, 800], 'description': 'ブラックホール', 'dialogue': '0.8光年先のBHからBZ過程でエネルギー抽出。出力10^15PW級。', 'data': 'BZ過程: 10^15PW'},
    
    # 6P: マイクロスロート
    {'rect': [40, 40, 1720, 800], 'description': 'マイクロスロート概念図', 'dialogue': '質量転送はできない。しかし、情報なら送れる。これが「マイクロスロート」だ。', 'data': '情報転送: 0秒'},
    {'rect': [40, 860, 840, 800], 'description': '地球-プロキシマb間の通信', 'dialogue': '転送容量: 2.24×10^37 bps。AR空間の転送には十分すぎる帯域。', 'data': '2.24×10^37 bps'},
    {'rect': [920, 860, 840, 800], 'description': 'AR空間の人間たち', 'dialogue': '情報は0秒で届く。人間はARの中で、プロキシマbを体験する。', 'data': 'ARフルダイブ'},
    
    # 7P: 旅立ち
    {'rect': [40, 40, 1720, 800], 'description': '探査機打ち上げ', 'dialogue': '航行速度: 0.2c。航行時間: 21年。貨物: 3Dプリンタと金属粉末10トン。', 'data': '0.2c 21年'},
    {'rect': [40, 860, 840, 800], 'description': '探査機内部', 'dialogue': '自己複製ロボット: 10台。到着後、自律的に増殖し、インフラを建設する。', 'data': 'ロボット10台'},
    {'rect': [920, 860, 840, 800], 'description': '遠ざかる地球', 'dialogue': '頼んだぞ、時超えケンタ。', 'data': '出発: 0年'},
    
    # 8P: 21年の旅
    {'rect': [40, 40, 1720, 800], 'description': '暗黒空間の探査機', 'dialogue': '21年間、私は孤独に計算を続ける。自己診断。全モジュール正常。', 'data': '航行中'},
    {'rect': [40, 860, 840, 800], 'description': '距離カウンター', 'dialogue': '残り距離: 3.8光年。残り時間: 19年。', 'data': '残り19年'},
    {'rect': [920, 860, 840, 800], 'description': '地球からの通信', 'dialogue': '地球からの応答待ち時間: 8.4年。私は自律判断を余儀なくされる。', 'data': 'タイムラグ: 8.4年'},
    
    # 9P: 到着
    {'rect': [40, 40, 1720, 800], 'description': 'プロキシマb上空', 'dialogue': 'プロキシマ・ケンタウリbに到着。21年の旅が終わった。', 'data': '到着: 21年'},
    {'rect': [40, 860, 840, 800], 'description': '地表着陸', 'dialogue': '重力: 0.4G。放射線レベル: 高。ただちに地下基地の建設を開始する。', 'data': '0.4G'},
    {'rect': [920, 860, 840, 800], 'description': 'ロボット展開', 'dialogue': 'フェーズ1開始。自己複製ロボットの展開。', 'data': '自己複製開始'},
    
    # 10P: 自己複製
    {'rect': [40, 40, 1720, 800], 'description': '3Dプリンタで複製', 'dialogue': '自己複製速度: 年10%。72.5年で100万台に到達。', 'data': '年10%増加'},
    {'rect': [40, 860, 840, 800], 'description': 'ロボット群', 'dialogue': 'それぞれのロボットに量子コンピュータが搭載されている。私は、群れそのものだ。', 'data': '10万台の細胞'},
    {'rect': [920, 860, 840, 800], 'description': '量子コンピュータチップ', 'dialogue': '1台が壊れても、私は死なない。', 'data': '分散型AI'},
    
    # 11P: ダイソン環建設
    {'rect': [40, 40, 1720, 800], 'description': '太陽電池パネル敷設', 'dialogue': '地平面ダイソン環の建設を開始する。目標出力: 1.64PW。', 'data': '目標: 1.64PW'},
    {'rect': [40, 860, 840, 800], 'description': 'パネル敷設作業', 'dialogue': '必要面積: 5.9億km²。プロキシマbの表面積の約30%。', 'data': '面積: 5.9億km²'},
    {'rect': [920, 860, 840, 800], 'description': '完成したダイソン環', 'dialogue': '建設期間: 15年。到着後15年で、1.64PWを達成する。', 'data': '完成: 到着後15年'},
    
    # 12P: BH発見
    {'rect': [40, 40, 1720, 800], 'description': '重力マイクロレンズ観測', 'dialogue': '重力マイクロレンズ異常を検出。解析中…。', 'data': '異常検出'},
    {'rect': [40, 860, 840, 800], 'description': 'ブラックホール想像図', 'dialogue': '発見: 0.8光年先に単独BHを確認。質量: 6.3太陽質量。回転: a=0.92。', 'data': '6.3M☉ a=0.92'},
    {'rect': [920, 860, 840, 800], 'description': 'ペンローズ効率グラフ', 'dialogue': 'ペンローズ過程の効率: 24.2%。BZ過程で10^15PW級の出力が可能。', 'data': '効率: 24.2%'},
    
    # 13P: BZ過程起動
    {'rect': [40, 40, 1720, 800], 'description': 'BZ過程概念図', 'dialogue': 'BZ過程を起動する。BHの回転エネルギーを磁場を介して抽出する。', 'data': 'BZ過程起動'},
    {'rect': [40, 860, 840, 800], 'description': 'BHジェット', 'dialogue': '出力: 10^15PW。これでマイクロスロートを本格点火する。', 'data': '出力: 10^15PW'},
    {'rect': [920, 860, 840, 800], 'description': 'エネルギー転送イメージ', 'dialogue': '質量転送が可能になる。プロキシマcの資源を地球に送れる。', 'data': '質量転送可能'},
    
    # 14P: マイクロスロート開通
    {'rect': [40, 40, 1720, 800], 'description': '光の柱', 'dialogue': 'マイクロスロート、開通。地球-プロキシマb間の0秒通信を確立。', 'data': '0秒通信確立'},
    {'rect': [40, 860, 840, 800], 'description': 'AR空間の人間たち', 'dialogue': '見える…プロキシマbの赤い空が…！', 'data': 'AR体験開始'},
    {'rect': [920, 860, 840, 800], 'description': '未来徹駆博士', 'dialogue': 'こうして、人類は4.2光年先の星と、リアルタイムでつながった。', 'data': '第1話 完'},
]

# 全ページを生成
for page_num in range(0, len(chapter1_panels), 3):
    page_panels = chapter1_panels[page_num:page_num+3]
    page_index = page_num // 3 + 1
    create_manga_page(1, page_index, page_panels)

print("\n===== 第1話「種火」コマ割り生成完了 =====")
print(f"全{len(chapter1_panels)}コマ / {len(chapter1_panels)//3}ページ")
print("出力先: manga_pages/ ディレクトリ")
print("========================================")