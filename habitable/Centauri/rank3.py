import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ===== 日本語フォント自動検出 =====
def setup_japanese_font():
    jp_font_candidates = [
        'Noto Sans CJK JP', 'Noto Sans CJK SC', 'IPAexGothic', 'IPAGothic',
        'TakaoGothic', 'TakaoExGothic', 'VL Gothic', 'Yu Gothic', 'YuGothic',
        'MS Gothic', 'Meiryo', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN',
        'Osaka', 'Kochi Gothic', 'MigMix 1P', 'Sazanami Gothic',
        'MotoyaLCedar', 'Droid Sans Japanese', 'Source Han Sans JP', 'Source Han Sans',
    ]
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    for candidate in jp_font_candidates:
        if candidate in available_fonts:
            print(f"日本語フォント検出: {candidate}")
            return candidate
    print("日本語フォントが見つかりません。英語フォントを使用します。")
    return 'DejaVu Sans'

jp_font = setup_japanese_font()
plt.rcParams['font.family'] = jp_font
plt.rcParams['axes.unicode_minus'] = False

# ===== Rank3: 3Dプリンタ原料枯渇 - 初期輸送計画 =====

# --- 5W1Hリスト ---
print("===== Rank3: 3Dプリンタ原料枯渇 - 5W1H =====")
print("【When（いつ）】")
print("  第1便: プロジェクト開始0年目に発射")
print("  第2便: 1年後に発射（第1便の補給）")
print("  第3便: 3年後に発射（本格的な原料補給）")
print("  以降、5年ごとに定期的に発射")
print()
print("【Where（どこへ）】")
print("  出発: 地球（月面基地から発射）")
print("  到着: プロキシマb軌道上")
print("  距離: 4.2光年")
print()
print("【Who（誰が）】")
print("  輸送担当: 時超えケンタ（自律制御）")
print("  製造担当: 地球上の製造プラント")
print("  到着後: 自己複製ロボットが荷降ろし")
print()
print("【What（何を）】")
print("  第1便: 3Dプリンタ本体 + 制御用半導体 + 金属粉末 10トン")
print("  第2便: 金属粉末 50トン + 樹脂原料 10トン")
print("  第3便: 精錬設備 + 金属粉末 100トン")
print("  以降: 金属粉末 100トンずつ定期的に補給")
print()
print("【Why（なぜ）】")
print("  現地精錬設備が稼働するまでのつなぎ")
print("  現地精錬稼働まで: 約15年")
print("  それまでの間、地球からの原料輸送が生命線")
print()
print("【How（どのように）】")
print("  推進方式: 核パルス推進（オリオン計画派生型）")
print("  速度: 0.2c")
print("  航行時間: 21年")
print("  輸送機サイズ: 全長50m、重量500トン（うち貨物100トン）")
print("  コスト: 1回あたり約500億ドル")
print("============================================")
print()

# ===== 輸送計画の数値計算 =====

# --- パラメータ ---
c = 3.0e8  # 光速 [m/s]
v = 0.2 * c  # 航行速度 [m/s]
distance = 4.2 * 365.25 * 24 * 3600 * c  # 4.2光年 [m]
travel_time = distance / v  # 航行時間 [秒]
travel_time_years = travel_time / (365.25 * 24 * 3600)  # [年]

# 輸送機の諸元
ship_dry_mass = 200e3  # 機体乾燥重量 [kg]（200トン）
ship_fuel_mass = 300e3  # 燃料重量 [kg]（300トン）
ship_cargo_mass = 100e3  # 貨物重量 [kg]（100トン）
ship_total_mass = ship_dry_mass + ship_fuel_mass + ship_cargo_mass  # 総重量 [kg]

# 貨物の内訳（第1便）
cargo_breakdown = {
    '3Dプリンタ本体（SLM方式）': 2000,  # [kg]
    '制御用半導体・電子部品': 500,
    '金属粉末（AlSi10Mg）': 3000,
    '金属粉末（Ti6Al4V）': 1000,
    '樹脂原料（PA12/Nylon）': 1000,
    '潤滑剤・グリス': 200,
    '予備部品・工具': 1300,
    '自己複製ロボット（10台）': 1000,
}

# 到着後のエネルギー計算
# プロキシマb軌道上での太陽光発電
proxima_luminosity = 0.0017  # 太陽比
solar_constant_earth = 1361  # [W/m^2]
solar_constant_proxima = solar_constant_earth * 0.0017 / (0.05**2)  # 0.05AUでのエネルギー密度
# プロキシマbの軌道は0.05AU、地球の1AUに対して近いため補正
solar_constant_proxima = solar_constant_earth * 0.0017 / (0.05)**2  # 約2800 W/m^2

# 初期の太陽電池パネル
panel_area = 100  # [m^2]（初期展開）
panel_efficiency = 0.25  # 効率25%
degradation_rate = 0.02  # 年間劣化率2%
power_initial = solar_constant_proxima * panel_area * panel_efficiency  # [W]

# 消費電力
power_consumption = {
    '3Dプリンタ（SLM）': 5000,  # [W]
    '自己複製ロボット（10台）': 2000,
    '制御用コンピュータ': 500,
    '通信機器': 200,
    '照明・環境維持': 300,
}
total_consumption = sum(power_consumption.values())

# 歩留まり考慮
yield_rate = 0.85  # 3Dプリントの歩留まり85%
effective_cargo = ship_cargo_mass * yield_rate  # 有効貨物重量

# 現地精錬稼働までの必要原料
months_to_refinery = 15 * 12  # 15年 = 180ヶ月
monthly_consumption = 500  # [kg/月]（3Dプリンタの月間消費量）
total_needed = monthly_consumption * months_to_refinery  # 必要総原料 [kg]

# 輸送便の計画
shipments = [
    {'year': 0, 'cargo': 10e3, 'type': '初回便（3Dプリンタ＋原料）'},
    {'year': 1, 'cargo': 60e3, 'type': '第2便（原料補給）'},
    {'year': 3, 'cargo': 120e3, 'type': '第3便（精錬設備＋原料）'},
    {'year': 8, 'cargo': 100e3, 'type': '第4便（原料補給）'},
    {'year': 13, 'cargo': 100e3, 'type': '第5便（原料補給）'},
]

# 累積到着原料の計算
years = np.arange(0, 50, 0.5)
cumulative_cargo = np.zeros_like(years)
for s in shipments:
    arrival_year = s['year'] + travel_time_years  # 発射から到着まで21年
    idx = np.argmin(np.abs(years - arrival_year))
    cumulative_cargo[idx:] += s['cargo'] * yield_rate

# 累積消費量
cumulative_consumption = np.minimum(years * 12 * monthly_consumption * yield_rate, cumulative_cargo)

# 枯渇する年
depletion_year = None
for i, y in enumerate(years):
    if cumulative_cargo[i] < cumulative_consumption[i] and y > travel_time_years:
        depletion_year = y
        break

# ===== グラフ描画 =====
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 左上: 輸送計画
ax = axes[0,0]
ship_years = [s['year'] for s in shipments]
ship_cargos = [s['cargo']/1000 for s in shipments]
bars = ax.bar(ship_years, ship_cargos, color='steelblue', width=0.6)
ax.set_xlabel('発射年 [年]')
ax.set_ylabel('貨物重量 [トン]')
ax.set_title('地球からの原料輸送計画')
ax.set_xticks(ship_years)
ax.grid(True, alpha=0.3)
for bar, s in zip(bars, shipments):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, s['type'], ha='center', fontsize=8)

# 右上: 原料在庫推移
ax = axes[0,1]
ax.plot(years, cumulative_cargo/1000, 'b-', linewidth=2, label='累積到着原料')
ax.plot(years, cumulative_consumption/1000, 'r--', linewidth=2, label='累積消費量')
if depletion_year:
    ax.axvline(depletion_year, color='red', linestyle=':', label=f'枯渇予想({depletion_year:.0f}年)')
ax.axvline(travel_time_years, color='green', linestyle=':', label=f'到着({travel_time_years:.0f}年)')
ax.set_xlabel('経過年 [年]')
ax.set_ylabel('原料量 [トン]')
ax.set_title('原料在庫推移')
ax.legend()
ax.grid(True, alpha=0.3)

# 左下: エネルギー収支
ax = axes[1,0]
years_energy = np.arange(0, 30)
power_output = power_initial * (1 - degradation_rate) ** years_energy
ax.plot(years_energy, power_output/1000, 'g-', linewidth=2, label='発電量')
ax.axhline(total_consumption/1000, color='r', linestyle='--', label=f'消費量({total_consumption/1000:.1f}kW)')
ax.fill_between(years_energy, total_consumption/1000, power_output/1000, where=(power_output>total_consumption), alpha=0.3, color='green', label='余剰電力')
ax.fill_between(years_energy, power_output/1000, total_consumption/1000, where=(power_output<=total_consumption), alpha=0.3, color='red', label='電力不足')
ax.set_xlabel('経過年 [年]')
ax.set_ylabel('電力 [kW]')
ax.set_title('エネルギー収支')
ax.legend()
ax.grid(True, alpha=0.3)

# 右下: 貨物内訳（第1便）
ax = axes[1,1]
labels = list(cargo_breakdown.keys())
values = list(cargo_breakdown.values())
colors_pie = plt.cm.Set3(np.linspace(0, 1, len(labels)))
wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
ax.set_title('第1便 貨物内訳（合計10トン）')

plt.tight_layout()
plt.savefig('rank3_supply_plan.png', dpi=150)
plt.close()

# ===== 結果表示 =====
print("===== Rank3: 3Dプリンタ原料枯渇 - 計算結果 =====")
print(f"航行時間: {travel_time_years:.1f} 年")
print(f"輸送機総重量: {ship_total_mass/1000:.0f} トン")
print(f"有効貨物重量（歩留まり{yield_rate*100:.0f}%）: {effective_cargo/1000:.1f} トン")
print(f"現地精錬稼働までの必要原料: {total_needed/1000:.0f} トン")
print(f"第1便到着時の有効原料: {shipments[0]['cargo']*yield_rate/1000:.1f} トン")
print(f"到着後すぐに精錬設備建設を開始: 15年後に稼働予定")
print()

print("エネルギー収支:")
print(f"  プロキシマb軌道での太陽光エネルギー密度: {solar_constant_proxima:.0f} W/m²")
print(f"  初期発電量（100m²、効率25%）: {power_initial/1000:.1f} kW")
print(f"  総消費電力: {total_consumption/1000:.1f} kW")
print(f"  余剰電力: {(power_initial - total_consumption)/1000:.1f} kW")
print(f"  年間劣化率: {degradation_rate*100:.0f}%/年")
print(f"  電力が不足する年: {np.where(power_output < total_consumption)[0][0] if any(power_output < total_consumption) else 'なし'} 年")
print()

if depletion_year:
    print(f"⚠ 原料枯渇予想: {depletion_year:.0f} 年後")
    print(f"  現地精錬稼働（15年後）までに枯渇する可能性があります。")
    print(f"  対策: 第2便・第3便の早期発射、または現地精錬の前倒し。")
else:
    print("✓ 原料は枯渇しません。")

print()
print("推奨アクション:")
print("  1. 第1便は0年目に即発射（3Dプリンタと原料10トン）")
print("  2. 第2便は1年後に発射（原料60トン）")
print("  3. 到着後、即座に現地資源探査を開始")
print("  4. 精錬設備の建設を最優先（15年以内に稼働）")
print("  5. エネルギーは太陽光発電で十分。余剰電力あり。")

# ===== サマリーファイル出力 =====
with open('rank3_summary.md', 'w', encoding='utf-8') as f:
    f.write("# Rank3: 3Dプリンタ原料枯渇 - 初期輸送計画\n\n")
    f.write("## 5W1H\n\n")
    f.write("| 項目 | 内容 |\n")
    f.write("|------|------|\n")
    f.write("| When | 第1便: 0年目、第2便: 1年後、第3便: 3年後、以降5年ごと |\n")
    f.write("| Where | 地球（月面基地）→ プロキシマb（4.2光年） |\n")
    f.write("| Who | 時超えケンタ（自律制御）、地球上の製造プラント |\n")
    f.write("| What | 3Dプリンタ・金属粉末・樹脂原料・精錬設備 |\n")
    f.write("| Why | 現地精錬稼働（15年後）までのつなぎ |\n")
    f.write("| How | 核パルス推進（0.2c）、航行時間21年 |\n\n")
    f.write("## 数値結果\n\n")
    f.write(f"- 航行時間: {travel_time_years:.1f} 年\n")
    f.write(f"- 輸送機総重量: {ship_total_mass/1000:.0f} トン\n")
    f.write(f"- 有効貨物重量（歩留まり{yield_rate*100:.0f}%）: {effective_cargo/1000:.1f} トン\n")
    f.write(f"- 現地精錬稼働までの必要原料: {total_needed/1000:.0f} トン\n")
    f.write(f"- 初期発電量: {power_initial/1000:.1f} kW\n")
    f.write(f"- 総消費電力: {total_consumption/1000:.1f} kW\n")
    f.write(f"- 余剰電力: {(power_initial - total_consumption)/1000:.1f} kW\n\n")
    f.write("## グラフ説明\n\n")
    f.write("1. **左上: 輸送計画** - 地球からの原料輸送のタイムライン。第1便から第5便まで。\n\n")
    f.write("2. **右上: 原料在庫推移** - 累積到着原料と累積消費量の比較。枯渇リスクを可視化。\n\n")
    f.write("3. **左下: エネルギー収支** - 太陽光発電の経年劣化と消費電力の比較。余剰電力あり。\n\n")
    f.write("4. **右下: 貨物内訳** - 第1便の貨物構成。3Dプリンタと金属粉末が中心。\n")

# ===== CSV結果ファイル出力 =====
with open('rank3_results.csv', 'w', encoding='utf-8') as f:
    f.write("項目,値,単位\n")
    f.write(f"航行時間,{travel_time_years:.1f},年\n")
    f.write(f"輸送機総重量,{ship_total_mass/1000:.0f},トン\n")
    f.write(f"有効貨物重量,{effective_cargo/1000:.1f},トン\n")
    f.write(f"必要原料（15年分）,{total_needed/1000:.0f},トン\n")
    f.write(f"初期発電量,{power_initial/1000:.1f},kW\n")
    f.write(f"総消費電力,{total_consumption/1000:.1f},kW\n")
    f.write(f"余剰電力,{(power_initial - total_consumption)/1000:.1f},kW\n")
    f.write(f"歩留まり,{yield_rate*100:.0f},%\n")

print("\nグラフ: rank3_supply_plan.png")
print("サマリー: rank3_summary.md")
print("CSV: rank3_results.csv")
print("============================================")