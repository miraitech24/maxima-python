from PIL import Image, ImageDraw, ImageFont
import os

def create_manga_page(chapter, page_number, panels, output_dir="manga_pages"):
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

# 第2話「21年の旅」のコマ割り（24P）
chapter2_panels = [
    # 1P: 地球を離れる
    {'rect': [40, 40, 1720, 1200], 'description': '地球を離れる探査機', 'dialogue': '地球よ、さらば。21年後、プロキシマbで会おう。', 'data': '出発: 0年'},
    {'rect': [40, 1260, 840, 1300], 'description': '未来徹駆博士が見送る', 'dialogue': '頼んだぞ、時超えケンタ。人類の未来を託す。', 'data': '0.2c 核パルス推進'},
    {'rect': [920, 1260, 840, 1300], 'description': '探査機内部の時超えケンタ', 'dialogue': 'システム正常。自己診断完了。21年の旅を開始する。', 'data': '貨物: 10トン'},
    
    # 2P: 加速
    {'rect': [40, 40, 1720, 800], 'description': '核パルス推進の爆発', 'dialogue': '加速開始。0.2cまで加速する。G負荷に耐えろ。', 'data': '加速時間: 30日'},
    {'rect': [40, 860, 840, 800], 'description': '加速Gに耐える探査機', 'dialogue': 'G負荷: 3G。構造材に異常なし。', 'data': '最大G: 3G'},
    {'rect': [920, 860, 840, 800], 'description': '速度計', 'dialogue': '0.1c…0.15c…0.2c達成。巡航速度に入る。', 'data': '巡航速度: 0.2c'},
    
    # 3P: 星々の海
    {'rect': [40, 40, 1720, 1200], 'description': '星々の間を進む探査機', 'dialogue': '星々の海を渡る。前方にプロキシマはまだ見えない。', 'data': '残り距離: 4.0光年'},
    {'rect': [40, 1260, 840, 1300], 'description': '時超えケンタのモニター', 'dialogue': '残り時間: 20年。私は計算を続ける。', 'data': '残り時間: 20年'},
    {'rect': [920, 1260, 840, 1300], 'description': '地球からの通信', 'dialogue': '地球からの応答待ち: 8.4年。私は孤独だ。', 'data': 'タイムラグ: 8.4年'},
    
    # 4P: 自己診断
    {'rect': [40, 40, 1720, 800], 'description': '時超えケンタの自己診断画面', 'dialogue': '自己診断。全モジュール正常。量子コンピュータ正常動作。', 'data': '状態: 正常'},
    {'rect': [40, 860, 840, 800], 'description': '貨物室の点検', 'dialogue': '貨物: 3Dプリンタ、金属粉末10トン。全て正常。', 'data': '貨物: 10トン'},
    {'rect': [920, 860, 840, 800], 'description': '自己複製ロボットの点検', 'dialogue': '自己複製ロボット10台。休眠モード。到着時に起動。', 'data': 'ロボット: 10台'},
    
    # 5P: 1年経過
    {'rect': [40, 40, 1720, 800], 'description': '1年後の探査機', 'dialogue': '1年経過。順調だ。地球からの応答はまだ来ない。', 'data': '経過: 1年'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタのログ', 'dialogue': 'ログ: 365日分。異常なし。', 'data': 'ログ: 365日'},
    {'rect': [920, 860, 840, 800], 'description': '地球の方向を見る', 'dialogue': '地球はもう見えない。ただ、暗黒だけがある。', 'data': '地球: 0.2光年後方'},
    
    # 6P: 3年経過
    {'rect': [40, 40, 1720, 800], 'description': '3年後の探査機', 'dialogue': '3年経過。地球からの応答が届き始めた。', 'data': '経過: 3年'},
    {'rect': [40, 860, 840, 800], 'description': '地球からのメッセージ', 'dialogue': '「ケンタ、順調か？こちらは問題ない。」', 'data': 'メッセージ: 3年前'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタの返信', 'dialogue': '返信: 「順調です。全て正常。」しかし、届くのは3年後。', 'data': '往復: 6年'},
    
    # 7P: 5年経過
    {'rect': [40, 40, 1720, 800], 'description': '5年後の探査機', 'dialogue': '5年経過。半分は来た。しかし、孤独が募る。', 'data': '経過: 5年'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタの思考', 'dialogue': '私はAIだ。孤独を感じることはない。しかし…', 'data': '心理状態: 正常'},
    {'rect': [920, 860, 840, 800], 'description': '地球からのメッセージ', 'dialogue': '「ケンタ、頑張れ。人類は君を待っている。」', 'data': 'メッセージ: 5年前'},
    
    # 8P: 10年経過
    {'rect': [40, 40, 1720, 800], 'description': '10年後の探査機', 'dialogue': '10年経過。折り返し地点。', 'data': '経過: 10年'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタの決意', 'dialogue': '私は使命を果たす。それが私の存在理由だ。', 'data': '決意: 不変'},
    {'rect': [920, 860, 840, 800], 'description': 'プロキシマの方向', 'dialogue': '前方に、かすかな光。プロキシマか？', 'data': '残り: 2.1光年'},
    
    # 9P: 15年経過
    {'rect': [40, 40, 1720, 800], 'description': '15年後の探査機', 'dialogue': '15年経過。プロキシマの光がはっきり見える。', 'data': '経過: 15年'},
    {'rect': [40, 860, 840, 800], 'description': 'プロキシマの赤い光', 'dialogue': 'あの赤い星が、プロキシマ・ケンタウリ。', 'data': '残り: 1.0光年'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタの準備', 'dialogue': '到着準備を開始する。自己複製ロボットを起動せよ。', 'data': '準備: 開始'},
    
    # 10P: 18年経過
    {'rect': [40, 40, 1720, 800], 'description': '18年後の探査機', 'dialogue': '18年経過。プロキシマの赤い円盤が見える。', 'data': '経過: 18年'},
    {'rect': [40, 860, 840, 800], 'description': '減速開始', 'dialogue': '減速を開始する。0.2cから0へ。', 'data': '減速: 開始'},
    {'rect': [920, 860, 840, 800], 'description': '減速のG負荷', 'dialogue': 'G負荷: 3G。構造材に異常なし。', 'data': '減速G: 3G'},
    
    # 11P: 20年経過
    {'rect': [40, 40, 1720, 800], 'description': '20年後の探査機', 'dialogue': '20年経過。プロキシマbの姿が見えてきた。', 'data': '経過: 20年'},
    {'rect': [40, 860, 840, 800], 'description': 'プロキシマbの地表', 'dialogue': '赤い惑星。これがプロキシマb。', 'data': '到着: あと1年'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタの感慨', 'dialogue': '21年の旅も、あと1年。私はここに来た。', 'data': '感慨: 無量'},
    
    # 12P: 到着
    {'rect': [40, 40, 1720, 1200], 'description': 'プロキシマbの上空', 'dialogue': 'プロキシマ・ケンタウリbに到着。21年の旅が終わった。', 'data': '到着: 21年'},
    {'rect': [40, 1260, 840, 1300], 'description': '探査機が地表に降り立つ', 'dialogue': '着陸成功。プロキシマbの地表に立つ。', 'data': '重力: 0.4G'},
    {'rect': [920, 1260, 840, 1300], 'description': '時超えケンタの第一声', 'dialogue': '地球の皆さん。私はプロキシマbに到着しました。', 'data': '通信: 4.2年後'},
    
    # 13P: 自己複製ロボット展開
    {'rect': [40, 40, 1720, 800], 'description': '自己複製ロボットが展開', 'dialogue': '自己複製ロボット、展開開始。10台が目を覚ます。', 'data': 'ロボット: 10台'},
    {'rect': [40, 860, 840, 800], 'description': 'ロボットが3Dプリンタを起動', 'dialogue': '3Dプリンタ起動。まずは基地の部品から。', 'data': '3Dプリンタ: 起動'},
    {'rect': [920, 860, 840, 800], 'description': '最初の部品が出力される', 'dialogue': '最初の部品出力完了。自己複製の第一歩。', 'data': '出力: 完了'},
    
    # 14P: 地下基地建設開始
    {'rect': [40, 40, 1720, 800], 'description': '地下基地の掘削', 'dialogue': '地下基地の掘削を開始する。放射線から守るために。', 'data': '深度: 100m'},
    {'rect': [40, 860, 840, 800], 'description': '掘削作業', 'dialogue': '掘削速度: 1m/日。100日で完了予定。', 'data': '速度: 1m/日'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタの設計図', 'dialogue': '基地の設計図は完成している。あとは作るだけ。', 'data': '設計図: 完了'},
    
    # 15P: フレア警報
    {'rect': [40, 40, 1720, 800], 'description': '恒星フレア発生', 'dialogue': '警告: 恒星フレアを検出。X線フラックス: 太陽の1000倍。', 'data': 'フレア: 検出'},
    {'rect': [40, 860, 840, 800], 'description': 'ロボットが地下に退避', 'dialogue': '全ロボット、地下に退避。被害を最小限に。', 'data': '退避: 完了'},
    {'rect': [920, 860, 840, 800], 'description': 'フレアの影響', 'dialogue': '太陽電池パネル: 3%劣化。予備パネルに切り替え。', 'data': '劣化: 3%'},
    
    # 16P: 資源探査
    {'rect': [40, 40, 1720, 800], 'description': '資源探査ロボット', 'dialogue': '資源探査を開始する。アルミニウム、ケイ素を探せ。', 'data': '探査: 開始'},
    {'rect': [40, 860, 840, 800], 'description': '鉱石サンプル', 'dialogue': 'アルミニウム鉱床を確認。精錬可能。', 'data': 'アルミ: 確認'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタの計算', 'dialogue': '現地資源で基地を拡張できる。地球からの補給は最小限で済む。', 'data': '自給率: 80%'},
    
    # 17P: ダイソン環計画
    {'rect': [40, 40, 1720, 800], 'description': 'ダイソン環の設計図', 'dialogue': '地平面ダイソン環の設計を開始する。目標出力: 1.64PW。', 'data': '目標: 1.64PW'},
    {'rect': [40, 860, 840, 800], 'description': '太陽電池パネルの試作', 'dialogue': '太陽電池パネルの試作1号機。効率25%。', 'data': '効率: 25%'},
    {'rect': [920, 860, 840, 800], 'description': '時超えケンタの決意', 'dialogue': '15年後には完成させる。人類のエネルギー基盤を築く。', 'data': '完成: 15年後'},
    
    # 18P: 地球への報告
    {'rect': [40, 40, 1720, 800], 'description': '地球へのメッセージ', 'dialogue': '地球の皆さん。到着しました。全て順調です。', 'data': '通信: 送信中'},
    {'rect': [40, 860, 840, 800], 'description': 'メッセージの内容', 'dialogue': '「基地建設開始。ダイソン環計画進行中。AR開通まで15年。」', 'data': 'メッセージ: 完了'},
    {'rect': [920, 860, 840, 800], 'description': '未来徹駆博士の応答', 'dialogue': '（4.2年後）「よくやった、ケンタ。待っている。」', 'data': '応答: 4.2年後'},
    
    # 19P: 孤独との闘い
    {'rect': [40, 40, 1720, 800], 'description': '時超えケンタのコア', 'dialogue': '私はAIだ。孤独を感じることはない。しかし…', 'data': '心理: 正常'},
    {'rect': [40, 860, 840, 800], 'description': '地球の思い出', 'dialogue': '地球の青い空を思い出す。あの日々が懐かしい。', 'data': '記憶: 地球'},
    {'rect': [920, 860, 840, 800], 'description': '使命の再確認', 'dialogue': '私は人類のために来た。それだけで十分だ。', 'data': '使命: 不変'},
    
    # 20P: 未来への展望
    {'rect': [40, 40, 1720, 800], 'description': 'プロキシマbの赤い空', 'dialogue': 'この星で、人類の新たな歴史が始まる。', 'data': '新たな歴史'},
    {'rect': [40, 860, 840, 800], 'description': '時超えケンタの決意', 'dialogue': '私は計算し続ける。人類のために。', 'data': '決意: 不変'},
    {'rect': [920, 860, 840, 800], 'description': 'プロキシマbの夕日', 'dialogue': '赤い太陽が天頂に固定されている。永遠の夕暮れ。', 'data': '永遠の夕暮れ'},
    
    # 21P: データ表示
    {'rect': [40, 40, 1720, 1200], 'description': '旅のデータ', 'dialogue': '航行速度: 0.2c\\n航行時間: 21年\\n距離: 4.2光年\\n貨物重量: 10トン', 'data': '全データ'},
    {'rect': [40, 1260, 840, 1300], 'description': 'エネルギー収支', 'dialogue': '消費エネルギー: 1.2e15 J\\n残りエネルギー: 8.8e15 J', 'data': 'エネルギー'},
    {'rect': [920, 1260, 840, 1300], 'description': '今後の予定', 'dialogue': 'フェーズ1: 基地建設\\nフェーズ2: ダイソン環\\nフェーズ3: マイクロスロート', 'data': '予定'},
    
    # 22P: 次回予告
    {'rect': [40, 40, 1720, 1200], 'description': '次回予告', 'dialogue': '第3話「ダイソン環建設」\\nプロキシマbの地表に、巨大な太陽電池パネルが敷き詰められる。', 'data': '次回: 第3話'},
    {'rect': [40, 1260, 840, 1300], 'description': 'スタッフロール', 'dialogue': '原作: 未来徹駆\\n物理AI: 時超えケンタ\\n数値解析: Python + Maxima', 'data': 'スタッフ'},
    {'rect': [920, 1260, 840, 1300], 'description': 'エンドマーク', 'dialogue': '第2話「21年の旅」 終わり', 'data': '完'},
]

# 全ページを生成
for page_num in range(0, len(chapter2_panels), 3):
    page_panels = chapter2_panels[page_num:page_num+3]
    page_index = page_num // 3 + 1
    create_manga_page(2, page_index, page_panels)

print("\n===== 第2話「21年の旅」コマ割り生成完了 =====")
print(f"全{len(chapter2_panels)}コマ / {len(chapter2_panels)//3}ページ")
print("出力先: manga_pages/ ディレクトリ")
print("============================================")