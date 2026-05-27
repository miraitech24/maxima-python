import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ===== 日本語フォント自動検出 =====
def setup_japanese_font():
    """日本語フォントを自動検出し、なければ英語フォントを使用"""
    # 日本語フォントの候補リスト
    jp_font_candidates = [
        'Noto Sans CJK JP',
        'Noto Sans CJK SC',
        'IPAexGothic',
        'IPAGothic',
        'TakaoGothic',
        'TakaoExGothic',
        'VL Gothic',
        'Yu Gothic',
        'YuGothic',
        'MS Gothic',
        'Meiryo',
        'Hiragino Sans',
        'Hiragino Kaku Gothic ProN',
        'Osaka',
        'Kochi Gothic',
        'MigMix 1P',
        'Sazanami Gothic',
        'MotoyaLCedar',
        'Droid Sans Japanese',
        'Source Han Sans JP',
        'Source Han Sans',
    ]
    
    # 利用可能なフォントを取得
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 日本語フォントを検索
    for candidate in jp_font_candidates:
        if candidate in available_fonts:
            print(f"日本語フォント検出: {candidate}")
            return candidate
    
    # 日本語フォントが見つからない場合、英語フォントを使用
    print("日本語フォントが見つかりません。英語フォントを使用します。")
    return 'DejaVu Sans'

# フォント設定
jp_font = setup_japanese_font()
plt.rcParams['font.family'] = jp_font
plt.rcParams['axes.unicode_minus'] = False  # マイナス記号の文字化け防止

# ===== C003: マイクロスロート経由情報転送帯域上限（AR解像度制約） =====

# --- 物理定数 ---
c = 2.99792458e8       # 光速 [m/s]
h = 6.62607015e-34     # プランク定数 [J·s]
kB = 1.380649e-23      # ボルツマン定数 [J/K]

# --- 人間の視覚パラメータ ---
fov_h = 120            # 水平視野角 [度]
fov_v = 90             # 垂直視野角 [度]
angular_resolution = 1.0 / 60  # 人間の角度分解能 [度]（1分角）
color_depth = 24       # 色深度 [bit]（RGB各8bit）
frame_rate = 60        # フレームレート [fps]

# --- AR解像度の計算 ---
# 視野全体の画素数
pixels_h = int(fov_h / angular_resolution)
pixels_v = int(fov_v / angular_resolution)
total_pixels = pixels_h * pixels_v

# 1フレームあたりのデータ量
bits_per_frame = total_pixels * color_depth

# 1秒あたりの必要帯域（非圧縮）
bandwidth_raw = bits_per_frame * frame_rate  # [bps]

# --- 圧縮率の考慮 ---
# 動画圧縮（H.265想定）で 1/100 程度に圧縮可能
compression_ratio = 100
bandwidth_compressed = bandwidth_raw / compression_ratio

# --- マイクロスロートの転送容量 ---
# #3004の結果: 2.24e37 bps
micro_throat_capacity = 2.243583478202148e37  # [bps]

# --- AR転送に必要な帯域の割合 ---
usage_ratio = bandwidth_compressed / micro_throat_capacity

# --- 結果表示 ---
print("===== C003: マイクロスロート経由情報転送帯域上限 =====")
print(f"水平視野角: {fov_h} 度")
print(f"垂直視野角: {fov_v} 度")
print(f"角度分解能: {angular_resolution} 度")
print(f"総画素数: {total_pixels:,} ピクセル")
print(f"1フレームあたりのデータ量: {bits_per_frame:,} bit")
print(f"非圧縮時必要帯域: {bandwidth_raw:.2e} bps")
print(f"圧縮後必要帯域: {bandwidth_compressed:.2e} bps")
print(f"マイクロスロート容量: {micro_throat_capacity:.2e} bps")
print(f"使用率: {usage_ratio:.2e} %")
print(f"→ AR転送に必要な帯域はマイクロスロート容量の {usage_ratio:.2e} %")
print(f"→ 余裕を持って転送可能")

# --- グラフ: 圧縮率と必要帯域の関係 ---
compression_ratios = np.logspace(0, 3, 100)  # 1倍〜1000倍
bandwidths = bandwidth_raw / compression_ratios

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 左: 圧縮率 vs 必要帯域
axes[0].loglog(compression_ratios, bandwidths, 'b-', linewidth=2)
axes[0].axhline(micro_throat_capacity, color='r', linestyle='--', label=f'マイクロスロート容量 ({micro_throat_capacity:.1e} bps)')
axes[0].axvline(compression_ratio, color='g', linestyle=':', label=f'想定圧縮率 ({compression_ratio}倍)')
axes[0].set_xlabel('圧縮率')
axes[0].set_ylabel('必要帯域 [bps]')
axes[0].set_title('圧縮率と必要帯域の関係')
axes[0].legend()
axes[0].grid(True, which='both', alpha=0.3)

# 右: 視野角と必要画素数の関係
fovs = np.linspace(10, 180, 100)
pixels = (fovs / angular_resolution)**2
bandwidths_fov = pixels * color_depth * frame_rate / compression_ratio

axes[1].semilogy(fovs, bandwidths_fov, 'b-', linewidth=2)
axes[1].axhline(micro_throat_capacity, color='r', linestyle='--', label=f'マイクロスロート容量')
axes[1].axvline(fov_h, color='g', linestyle=':', label=f'想定視野角 ({fov_h}度)')
axes[1].set_xlabel('視野角 [度]')
axes[1].set_ylabel('必要帯域 [bps]')
axes[1].set_title('視野角と必要帯域の関係')
axes[1].legend()
axes[1].grid(True, which='both', alpha=0.3)

plt.tight_layout()
plt.savefig('c003_ar_bandwidth.png', dpi=150)
plt.close()

# --- サマリーファイル出力 ---
with open('c003_summary.md', 'w', encoding='utf-8') as f:
    f.write("# C003: マイクロスロート経由情報転送帯域上限（AR解像度制約）\n\n")
    f.write("## 計算結果\n\n")
    f.write(f"- 水平視野角: {fov_h} 度\n")
    f.write(f"- 垂直視野角: {fov_v} 度\n")
    f.write(f"- 角度分解能: {angular_resolution} 度\n")
    f.write(f"- 総画素数: {total_pixels:,} ピクセル\n")
    f.write(f"- 非圧縮時必要帯域: {bandwidth_raw:.2e} bps\n")
    f.write(f"- 圧縮後必要帯域: {bandwidth_compressed:.2e} bps\n")
    f.write(f"- マイクロスロート容量: {micro_throat_capacity:.2e} bps\n")
    f.write(f"- 使用率: {usage_ratio:.2e} %\n\n")
    f.write("## 考察\n\n")
    f.write("AR転送に必要な帯域はマイクロスロート容量に対して極めて小さく、")
    f.write("余裕を持って転送可能である。\n")
    f.write("圧縮率100倍を想定しても、マイクロスロートの容量はAR転送に十分すぎる。\n")

# --- CSV結果ファイル出力 ---
with open('c003_results.csv', 'w', encoding='utf-8') as f:
    f.write("項目,値,単位\n")
    f.write(f"水平視野角,{fov_h},度\n")
    f.write(f"垂直視野角,{fov_v},度\n")
    f.write(f"角度分解能,{angular_resolution},度\n")
    f.write(f"総画素数,{total_pixels},ピクセル\n")
    f.write(f"非圧縮時必要帯域,{bandwidth_raw:.2e},bps\n")
    f.write(f"圧縮後必要帯域,{bandwidth_compressed:.2e},bps\n")
    f.write(f"マイクロスロート容量,{micro_throat_capacity:.2e},bps\n")
    f.write(f"使用率,{usage_ratio:.2e},%\n")

print("グラフ: c003_ar_bandwidth.png")
print("サマリー: c003_summary.md")
print("CSV: c003_results.csv")
print("============================================")