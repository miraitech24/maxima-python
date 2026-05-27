import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ===== 日本語フォント自動検出 =====
def setup_japanese_font():
    jp_font_candidates = [
        'Noto Sans CJK JP', 'IPAexGothic', 'IPAGothic',
        'TakaoGothic', 'Yu Gothic', 'YuGothic', 'MS Gothic',
        'Meiryo', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN',
        'Osaka', 'Kochi Gothic', 'MigMix 1P', 'Sazanami Gothic',
        'Source Han Sans JP', 'Source Han Sans',
    ]
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for candidate in jp_font_candidates:
        if candidate in available_fonts:
            plt.rcParams['font.family'] = candidate
            plt.rcParams['axes.unicode_minus'] = False
            print(f"日本語フォント検出: {candidate}")
            return
    print("日本語フォントが見つかりません。英語フォントを使用します。")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

setup_japanese_font()

# ===== C012: 複数ワームホール同時開口の干渉制御 =====
# 物理定数
c = 2.99792458e8
G = 6.67430e-11
hbar = 1.054571817e-34

# ワームホールパラメータ
r0 = 1.0  # スロート半径 [m]
rho_neg = 4.815e42  # 負のエネルギー密度 [J/m^3]

# ---- 1. 単一WHの曲率 ----
curvature_single = 1.0 / r0**2
print(f"単一WHの曲率: {curvature_single:.2e} 1/m^2")

# ---- 2. 複数WH間の干渉 ----
distances = np.logspace(0, 4, 100)  # 1m〜10km
N_wh_values = [10, 50, 100, 200, 500]

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 2-1: 距離と干渉強度
ax = axes[0, 0]
for N in N_wh_values[:3]:
    interference = N**2 / distances**2
    ax.loglog(distances, interference, label=f'N={N}本')
ax.axhline(curvature_single, color='r', linestyle='--', label=f'単一WH曲率 ({curvature_single:.1e})')
ax.set_xlabel('WH間距離 [m]')
ax.set_ylabel('干渉強度 [1/m^2]')
ax.set_title('WH間距離と干渉強度の関係')
ax.legend()
ax.grid(True, which='both', alpha=0.3)

# 2-2: 安定WH数 vs 距離
ax = axes[0, 1]
N_max = np.sqrt(curvature_single * distances**2)
ax.loglog(distances, N_max, 'b-', linewidth=2)
ax.fill_between(distances, 0, N_max, alpha=0.3, label='安定領域')
ax.set_xlabel('WH間距離 [m]')
ax.set_ylabel('最大安定WH数 [本]')
ax.set_title('距離に対する最大安定WH数')
ax.legend()
ax.grid(True, which='both', alpha=0.3)

# ---- 3. 量子もつれチャネルの干渉 ----
# チャネル容量の計算
f_signal = 1.0e12  # 信号周波数 [Hz]
T_noise = 2.7  # 宇宙背景温度 [K]
k_B = 1.380649e-23

# シャノン容量
SNR = 1.0e6  # 信号対雑音比
channel_capacity = f_signal * np.log2(1 + SNR)

# 多重化効率
N_channels = np.arange(1, 101)
multiplex_efficiency = 1.0 / (1 + 0.01 * (N_channels - 1))  # 干渉による効率低下

ax = axes[1, 0]
ax.plot(N_channels, multiplex_efficiency * 100, 'b-', linewidth=2)
ax.set_xlabel('同時通信チャネル数')
ax.set_ylabel('チャネル効率 [%]')
ax.set_title('量子もつれチャネルの多重化効率')
ax.grid(True, alpha=0.3)

# ---- 4. 時空歪みの空間分布 ----
ax = axes[1, 1]
x = np.linspace(-10, 10, 200)
y = np.linspace(-10, 10, 200)
X, Y = np.meshgrid(x, y)

# 3つのWHを配置
wh_positions = [(-3, 0), (3, 0), (0, 3)]
distortion = np.zeros_like(X)
for px, py in wh_positions:
    r = np.sqrt((X - px)**2 + (Y - py)**2)
    distortion += 1.0 / (r**2 + 0.5)  # 曲率寄与

contour = ax.contourf(X, Y, distortion, levels=20, cmap='hot')
for px, py in wh_positions:
    ax.plot(px, py, 'c*', markersize=15, label=f'WH ({px}, {py})')
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_title('複数WHによる時空歪み分布')
ax.set_aspect('equal')
plt.colorbar(contour, ax=ax, label='時空歪み [1/m^2]')

plt.tight_layout()
plt.savefig('c012_wh_interference.png', dpi=150)
plt.close()

# ---- 結果表示 ----
print("\n===== C012: 複数ワームホール同時開口の干渉制御 =====")
print(f"スロート半径: {r0} m")
print(f"単一WH曲率: {curvature_single:.2e} 1/m^2")

# 距離ごとの最大安定WH数
for d in [10, 100, 1000]:
    Nmax = int(np.sqrt(curvature_single * d**2))
    print(f"距離{d:5d}mでの最大安定WH数: {Nmax} 本")

# 量子チャネル
print(f"\n量子チャネル容量: {channel_capacity:.2e} bps")
print(f"100チャネル多重化時の効率: {multiplex_efficiency[-1]*100:.1f}%")

# 最適配置の提案
print(f"\n--- 最適配置提案 ---")
print(f"推奨WH間距離: 100m以上")
print(f"最大同時運用可能WH数: {int(np.sqrt(curvature_single * 100**2))} 本")
print(f"時空歪みの許容範囲: 単一WH曲率の10倍以下")
print("================================================")

# ---- サマリーファイル出力 ----
with open('c012_summary.md', 'w', encoding='utf-8') as f:
    f.write("# C012: 複数ワームホール同時開口の干渉制御\n\n")
    f.write("## 計算目的\n\n")
    f.write("複数のマイクロスロート（ワームホール）を同時に運用する際の、\n")
    f.write("互いの時空的干渉を解析し、安定運用のための条件を導出する。\n\n")
    f.write("## 物理モデル\n\n")
    f.write("### 1. 曲率干渉\n\n")
    f.write("各ワームホールの時空曲率は $1/r_0^2$ で表される。\n")
    f.write("複数WHが近接すると、互いの曲率が干渉し合い、安定性が低下する。\n\n")
    f.write("### 2. 量子もつれチャネル\n\n")
    f.write("量子もつれを利用した通信チャネルは、チャネル数が増えると\n")
    f.write("干渉により効率が低下する。\n\n")
    f.write("### 3. 時空歪み分布\n\n")
    f.write("複数のWHが作る時空歪みの空間分布を可視化し、\n")
    f.write("最適な配置を検討する。\n\n")
    f.write("## 計算結果\n\n")
    f.write(f"- スロート半径: {r0} m\n")
    f.write(f"- 単一WH曲率: {curvature_single:.2e} 1/m^2\n")
    f.write(f"- 距離10mでの最大安定WH数: {int(np.sqrt(curvature_single * 10**2))} 本\n")
    f.write(f"- 距離100mでの最大安定WH数: {int(np.sqrt(curvature_single * 100**2))} 本\n")
    f.write(f"- 距離1000mでの最大安定WH数: {int(np.sqrt(curvature_single * 1000**2))} 本\n\n")
    f.write("## グラフ説明\n\n")
    f.write("1. **WH間距離と干渉強度**: 距離が離れるほど干渉が弱まる。\n")
    f.write("2. **距離に対する最大安定WH数**: 距離の2乗に比例して増加。\n")
    f.write("3. **量子もつれチャネルの多重化効率**: チャネル数増加で効率低下。\n")
    f.write("4. **複数WHによる時空歪み分布**: 3つのWH周辺の歪みを可視化。\n\n")
    f.write("## 結論\n\n")
    f.write("複数のワームホールを安定運用するには、\n")
    f.write("WH間距離を100m以上確保し、同時運用数を100本以下に制限する必要がある。\n")
    f.write("量子もつれチャネルの多重化には、周波数分割や時分割多重が有効。\n")

# ---- CSV結果ファイル出力 ----
with open('c012_results.csv', 'w', encoding='utf-8') as f:
    f.write("距離[m],最大安定WH数[本]\n")
    for d in [1, 5, 10, 50, 100, 500, 1000]:
        Nmax = int(np.sqrt(curvature_single * d**2))
        f.write(f"{d},{Nmax}\n")

print("グラフ: c012_wh_interference.png")
print("サマリー: c012_summary.md")
print("CSV: c012_results.csv")

# ---- Maximaコード生成（c012.mac） ----
mac_code = """/* ===== C012: 複数ワームホール同時開口の干渉制御 ===== */
/* Maxima解析コード */
/* 
 * 目的: 複数のマイクロスロート（ワームホール）を同時に運用する際の
 *       互いの時空的干渉を解析し、安定運用のための条件を導出する。
 * 
 * 物理モデル:
 *   各ワームホールの時空曲率は 1/r0^2 で表される。
 *   複数WHが近接すると、互いの曲率が干渉し合い、安定性が低下する。
 *   干渉項は距離の逆二乗で減衰する。
 */

/* 物理定数 */
c: 2.99792458e8;    /* 光速 [m/s] */
G: 6.67430e-11;     /* 重力定数 [m^3/kg/s^2] */
hbar: 1.054571817e-34;  /* プランク定数 [J*s] */

/* ワームホールパラメータ */
r0: 1.0;            /* スロート半径 [m] */
rhoneg: 4.815e42;   /* 負のエネルギー密度 [J/m^3] */

/* 1. 単一WHの曲率 */
curvatureSingle: 1 / r0^2;
print("単一WHの曲率:", curvatureSingle, "1/m^2");

/* 2. 複数WH間の干渉 */
/* 干渉項: N^2 / d^2 （N: WH数, d: WH間距離） */
/* 安定条件: curvatureSingle > N^2 / d^2 */
/* 最大安定WH数: N_max = sqrt(curvatureSingle * d^2) */

/* 距離dにおける最大安定WH数 */
d: 100;  /* WH間距離 [m] */
Nmax: sqrt(curvatureSingle * d^2);
print("距離", d, "mでの最大安定WH数:", Nmax, "本");

/* 3. 異なる距離での最大安定WH数 */
for d in [10, 50, 100, 500, 1000] do (
    Nmax: sqrt(curvatureSingle * d^2),
    print("距離", d, "m: 最大", floor(Nmax), "本")
);

/* 4. 量子もつれチャネルの干渉 */
/* チャネル容量: C = f * log2(1 + SNR) */
fsignal: 1.0e12;    /* 信号周波数 [Hz] */
SNR: 1.0e6;         /* 信号対雑音比 */
channelCapacity: fsignal * log(1 + SNR) / log(2);
print("量子チャネル容量:", channelCapacity, "bps");

/* 5. 多重化効率 */
/* 効率 = 1 / (1 + 0.01 * (N - 1)) */
Nch: 100;           /* 同時チャネル数 */
efficiency: 1 / (1 + 0.01 * (Nch - 1));
print("100チャネル多重化効率:", efficiency * 100, "%");

/* 6. 結論 */
print("===== 解析結果 =====");
print("推奨WH間距離: 100m以上");
print("最大同時運用可能WH数:", floor(sqrt(curvatureSingle * 100^2)), "本");
print("====================");
"""

with open('c012.mac', 'w', encoding='utf-8') as f:
    f.write(mac_code)

print("Maximaコード: c012.mac")