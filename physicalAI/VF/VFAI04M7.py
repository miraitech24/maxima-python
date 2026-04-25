#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 08:50:02 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M7: 運用・維持管理計画（600行完全版）
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib

print("=" * 80)
print("VF-AI-04-M7: 運用・維持管理計画")
print("=" * 80)

# 1. フォント設定
print("\n1. フォント設定...")
try:
    available_fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
    jp_fonts = ['IPAexGothic', 'IPAGothic', 'MS Gothic', 'Yu Gothic']
    selected_font = None
    for font in jp_fonts:
        if font in available_fonts:
            selected_font = font
            break
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✓ 日本語フォント: {selected_font}")
        USE_JAPANESE = True
    else:
        plt.rcParams['font.family'] = 'sans-serif'
        print("⚠️ 英語フォントを使用")
        USE_JAPANESE = False
except:
    plt.rcParams['font.family'] = 'sans-serif'
    USE_JAPANESE = False

plt.rcParams.update({'figure.autolayout': True, 'savefig.bbox': 'tight'})

# 2. ファイル確認
print("\n2. ファイル確認...")
files = ['VF_AI_04_M6_results.csv', 'VF_AI_04_M5_results.csv']
for f in files:
    if os.path.exists(f):
        print(f"✓ {f}")
    else:
        print(f"✗ {f}")
        exit(1)

# 3. データ読み込み
print("\n3. データ読み込み...")
m6_data = pd.read_csv('VF_AI_04_M6_results.csv')
m5_data = pd.read_csv('VF_AI_04_M5_results.csv')

# 4. パラメータ設定
print("\n4. パラメータ設定...")
n_sites = 865
construction_years = 300
operational_years = 100

# コスト抽出
def get_value(df, keyword):
    for _, row in df.iterrows():
        if keyword in row['項目']:
            try:
                return float(row['値'].split()[0])
            except:
                return 0.0
    return 0.0

total_cost = get_value(m6_data, '総コスト') * 1e9
if total_cost == 0:
    total_cost = 1e12  # デフォルト値

# 運用パラメータ
params = {
    'power_per_site': 10e12,
    'operational_life': 100,
    'staff_per_site': 5,
    'energy_consumption_rate': 0.05,
    'inflation_rate': 0.02,
}

# 機器寿命
equipment = {
    '熱交換器': 20, '配管系統': 30, 'ポンプ': 10,
    '制御系統': 15, '構造物': 50, '電気系統': 25
}

# コストパラメータ
costs = {
    'staff_salary': 80000,
    'energy_cost': 0.10,
    'maintenance_rate': 0.02,
    'replacement_rate': 0.50,
}

print(f"拠点数: {n_sites}")
print(f"総建設費: ${total_cost/1e9:.2f}B")
print(f"運用期間: {operational_years}年")

# 5. 維持管理コスト計算
print("\n5. 維持管理コスト計算...")

years = list(range(operational_years))
annual_costs = []
cumulative_costs = []
cost_breakdown = []

for year in years:
    # 固定費
    staff_cost = n_sites * params['staff_per_site'] * costs['staff_salary']
    energy_wh = n_sites * params['power_per_site'] * params['energy_consumption_rate'] * 24 * 365
    energy_cost = energy_wh * costs['energy_cost'] / 1000
    routine_cost = total_cost * costs['maintenance_rate'] / operational_years
    
    # 機器交換費
    replacement_cost = 0
    for equip, lifespan in equipment.items():
        if year % lifespan == 0 and year > 0:
            replacement_cost += total_cost * 0.1 * costs['replacement_rate']
    
    # インフレ調整
    inflation = (1 + params['inflation_rate']) ** year
    year_costs = {
        '人件費': staff_cost * inflation,
        'エネルギー費': energy_cost * inflation,
        '定期保守費': routine_cost * inflation,
        '機器交換費': replacement_cost * inflation
    }
    
    total_year = sum(year_costs.values())
    annual_costs.append(total_year)
    cumulative_costs.append(total_year if year == 0 else cumulative_costs[-1] + total_year)
    cost_breakdown.append(year_costs)

print(f"初年度維持費: ${annual_costs[0]/1e9:.2f}B")
print(f"累積維持費: ${cumulative_costs[-1]/1e9:.2f}B")

# 6. エネルギー収支計算
print("\n6. エネルギー収支計算...")

generation = []
consumption = []
net_energy = []
efficiency = []

total_gen = n_sites * params['power_per_site'] * 24 * 365

for year in years:
    deg = 0.005
    annual_gen = total_gen * (1 - deg) ** year
    self_cons = annual_gen * params['energy_consumption_rate']
    maint_energy = annual_gen * 0.01
    total_cons = self_cons + maint_energy
    net = annual_gen - total_cons
    eff = net / annual_gen if annual_gen > 0 else 0
    
    generation.append(annual_gen)
    consumption.append(total_cons)
    net_energy.append(net)
    efficiency.append(eff)

print(f"初年度発電量: {generation[0]/1e15:.1f} PWh")
print(f"平均効率: {np.mean(efficiency)*100:.1f}%")

# 7. 人員計画
print("\n7. 人員計画作成...")

total_staff = []
staff_by_cat = {'制御': [], '保守': [], '技術': [], '管理': []}

base = {
    '制御': 50,
    '保守': n_sites * params['staff_per_site'],
    '技術': 200,
    '管理': 100
}

for year in years:
    auto = max(0.7, 1 - year * 0.003)
    year_staff = {}
    total = 0
    
    for cat, num in base.items():
        if cat == '技術':
            adj = num * (1 + year * 0.01)
        elif cat == '保守':
            adj = num * auto
        else:
            adj = num
        
        year_staff[cat] = int(adj)
        total += adj
        staff_by_cat[cat].append(adj)
    
    total_staff.append(total)

print(f"初年度要員: {total_staff[0]:.0f}人")
print(f"最終年度要員: {total_staff[-1]:.0f}人")

# 8. リスク分析
print("\n8. リスク分析...")

risks = {'機器故障': 0.01, '自然災害': 0.001, '人為誤り': 0.02}
cum_risk = 1 - (1 - sum(risks.values())) ** operational_years
expected_loss = cum_risk * total_cost * 0.1

print(f"累積リスク: {cum_risk*100:.1f}%")
print(f"想定損失: ${expected_loss/1e9:.2f}B")

# 9. 可視化
print("\n9. 可視化作成...")

if USE_JAPANESE:
    TEXT = {
        'title': 'VF-AI-04-M7: 運用・維持管理計画',
        'cost': '維持管理コスト',
        'energy': 'エネルギー収支',
        'staff': '人員計画',
        'risk': 'リスク分析',
        'year': '年',
        'cost_unit': 'コスト (BUSD)',
        'energy_unit': 'エネルギー (PWh)',
        'staff_unit': '要員数'
    }
else:
    TEXT = {
        'title': 'VF-AI-04-M7: Operations & Maintenance',
        'cost': 'Maintenance Costs',
        'energy': 'Energy Balance',
        'staff': 'Staffing Plan',
        'risk': 'Risk Analysis',
        'year': 'Year',
        'cost_unit': 'Cost (BUSD)',
        'energy_unit': 'Energy (PWh)',
        'staff_unit': 'Staff'
    }

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(TEXT['title'], fontsize=16, y=0.98)

# グラフ1: コスト
ax = axes[0, 0]
annual_b = np.array(annual_costs) / 1e9
cum_b = np.array(cumulative_costs) / 1e9
ax.plot(years, annual_b, 'b-', linewidth=2, label='年間')
ax.plot(years, cum_b, 'r-', linewidth=2, label='累積')
ax.fill_between(years, 0, annual_b, alpha=0.2, color='blue')
ax.set_xlabel(TEXT['year'], fontsize=12)
ax.set_ylabel(TEXT['cost_unit'], fontsize=12)
ax.set_title(TEXT['cost'], fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# グラフ2: エネルギー
ax = axes[0, 1]
gen_pwh = np.array(generation) / 1e15
net_pwh = np.array(net_energy) / 1e15
ax.plot(years, gen_pwh, 'g-', linewidth=2, label='発電量')
ax.plot(years, net_pwh, 'b-', linewidth=2, label='正味')
ax.fill_between(years, 0, gen_pwh, alpha=0.2, color='green')
ax.set_xlabel(TEXT['year'], fontsize=12)
ax.set_ylabel(TEXT['energy_unit'], fontsize=12)
ax.set_title(TEXT['energy'], fontsize=13)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# グラフ3: 人員
ax = axes[1, 0]
ax.plot(years, total_staff, color='purple', linewidth=2)  # 修正: 'purple'のみ
ax.fill_between(years, 0, total_staff, alpha=0.2, color='purple')
ax.set_xlabel(TEXT['year'], fontsize=12)
ax.set_ylabel(TEXT['staff_unit'], fontsize=12)
ax.set_title(TEXT['staff'], fontsize=13)
ax.grid(True, alpha=0.3)

# グラフ4: リスク
ax = axes[1, 1]
risk_names = list(risks.keys())
risk_vals = list(risks.values())
bars = ax.bar(risk_names, risk_vals, color=['red', 'orange', 'yellow'])
ax.set_ylabel('年間確率', fontsize=12)
ax.set_title(TEXT['risk'], fontsize=13)
ax.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, risk_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.05,
            f'{val*100:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('VF_AI_04_M7_results.png', dpi=150)
print("✓ グラフ保存: VF_AI_04_M7_results.png")

# 10. 詳細グラフ
fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle(TEXT['title'] + ' - 詳細', fontsize=16, y=0.98)

# 詳細1: コスト内訳
ax = axes2[0, 0]
first_costs = cost_breakdown[0]
cats = list(first_costs.keys())
vals = [v/1e9 for v in first_costs.values()]
bars = ax.bar(cats, vals, color=['blue', 'green', 'orange', 'red'])
ax.set_ylabel('BUSD', fontsize=12)
ax.set_title('初年度コスト内訳', fontsize=13)
ax.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02,
            f'{val:.2f}', ha='center', va='bottom', fontsize=9)

# 詳細2: 効率推移
ax = axes2[0, 1]
eff_pct = np.array(efficiency) * 100
ax.plot(years, eff_pct, 'b-', linewidth=2)
ax.fill_between(years, 0, eff_pct, alpha=0.2, color='blue')
ax.set_xlabel(TEXT['year'], fontsize=12)
ax.set_ylabel('効率 (%)', fontsize=12)
ax.set_title('エネルギー効率', fontsize=13)
ax.grid(True, alpha=0.3)

# 詳細3: 人員内訳
ax = axes2[1, 0]
first_staff = {k: v[0] for k, v in staff_by_cat.items()}
cats = list(first_staff.keys())
vals = list(first_staff.values())
bars = ax.bar(cats, vals, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
ax.set_ylabel('人数', fontsize=12)
ax.set_title('初年度人員内訳', fontsize=13)
ax.grid(True, alpha=0.3, axis='y')
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02,
            f'{int(val)}', ha='center', va='bottom', fontsize=9)

# 詳細4: 累積リスク
ax = axes2[1, 1]
cum_risks = []
for y in range(1, operational_years+1):
    cr = 1 - (1 - sum(risks.values())) ** y
    cum_risks.append(cr * 100)
ax.plot(range(1, operational_years+1), cum_risks, 'r-', linewidth=2)
ax.fill_between(range(1, operational_years+1), 0, cum_risks, alpha=0.2, color='red')
ax.set_xlabel(TEXT['year'], fontsize=12)
ax.set_ylabel('確率 (%)', fontsize=12)
ax.set_title('累積リスク確率', fontsize=13)
ax.grid(True, alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('VF_AI_04_M7_detailed.png', dpi=150)
print("✓ 詳細グラフ保存: VF_AI_04_M7_detailed.png")

# 11. 結果出力
print("\n10. 結果出力...")

# コストデータ
costs_df = pd.DataFrame({
    'year': years,
    'annual_cost_BUSD': [c/1e9 for c in annual_costs],
    'cumulative_cost_BUSD': [c/1e9 for c in cumulative_costs],
    'staff_cost_BUSD': [b['人件費']/1e9 for b in cost_breakdown],
    'energy_cost_BUSD': [b['エネルギー費']/1e9 for b in cost_breakdown],
    'maintenance_cost_BUSD': [b['定期保守費']/1e9 for b in cost_breakdown],
    'replacement_cost_BUSD': [b['機器交換費']/1e9 for b in cost_breakdown]
})
costs_df.to_csv('VF_AI_04_M7_costs.csv', index=False)
print("✓ コストデータ保存")

# エネルギーデータ
energy_df = pd.DataFrame({
    'year': years,
    'generation_PWh': [g/1e15 for g in generation],
    'consumption_PWh': [c/1e15 for c in consumption],
    'net_energy_PWh': [n/1e15 for n in net_energy],
    'efficiency_%': [e*100 for e in efficiency]
})
energy_df.to_csv('VF_AI_04_M7_energy.csv', index=False)
print("✓ エネルギーデータ保存")

# 人員データ
staff_df = pd.DataFrame({
    'year': years,
    'total_staff': total_staff,
    'control_staff': staff_by_cat['制御'],
    'maintenance_staff': staff_by_cat['保守'],
    'technical_staff': staff_by_cat['技術'],
    'management_staff': staff_by_cat['管理']
})
staff_df.to_csv('VF_AI_04_M7_staff.csv', index=False)
print("✓ 人員データ保存")

# 機器交換スケジュール
equipment_schedule = []
for equip, lifespan in equipment.items():
    for year in range(lifespan, operational_years, lifespan):
        equipment_schedule.append({
            'equipment': equip,
            'year': year,
            'lifespan': lifespan
        })
equip_df = pd.DataFrame(equipment_schedule)
equip_df.to_csv('VF_AI_04_M7_equipment.csv', index=False)
print("✓ 機器スケジュール保存")

# リスクデータ
risk_df = pd.DataFrame({
    'risk_type': list(risks.keys()),
    'annual_probability': list(risks.values()),
    'impact': ['中', '高', '中']
})
risk_df.to_csv('VF_AI_04_M7_risks.csv', index=False)
print("✓ リスクデータ保存")

# 総合レポート
with open('VF_AI_04_M7_report.txt', 'w', encoding='utf-8') as f:
    f.write("VF-AI-04-M7: 運用・維持管理計画 総合レポート\n")
    f.write("="*70 + "\n\n")
    
    f.write("1. 基本情報\n")
    f.write(f"   拠点数: {n_sites}\n")
    f.write(f"   運用期間: {operational_years}年\n")
    f.write(f"   総建設費: ${total_cost/1e9:.2f}B\n\n")
    
    f.write("2. 維持管理コスト\n")
    f.write(f"   初年度: ${annual_costs[0]/1e9:.2f}B\n")
    f.write(f"   累積({operational_years}年): ${cumulative_costs[-1]/1e9:.2f}B\n")
    f.write(f"   建設費比: {cumulative_costs[-1]/total_cost*100:.1f}%\n\n")
    
    f.write("3. エネルギー収支\n")
    f.write(f"   初年度発電量: {generation[0]/1e15:.1f} PWh\n")
    f.write(f"   初年度正味: {net_energy[0]/1e15:.1f} PWh\n")
    f.write(f"   平均効率: {np.mean(efficiency)*100:.1f}%\n\n")
    
    f.write("4. 人員計画\n")
    f.write(f"   初年度: {total_staff[0]:.0f}人\n")
    f.write(f"   最終年度: {total_staff[-1]:.0f}人\n")
    f.write(f"   削減率: {(1-total_staff[-1]/total_staff[0])*100:.1f}%\n\n")
    
    f.write("5. 機器寿命\n")
    for equip, lifespan in equipment.items():
        f.write(f"   {equip}: {lifespan}年\n")
    f.write("\n")
    
    f.write("6. リスク分析\n")
    f.write(f"   年間総リスク: {sum(risks.values())*100:.1f}%\n")
    f.write(f"   累積リスク: {cum_risk*100:.1f}%\n")
    f.write(f"   想定損失: ${expected_loss/1e9:.2f}B\n\n")
    
    f.write("7. 課題と対策\n")
    f.write("   [課題] 高額な維持費\n")
    f.write("   [対策] 自動化、予防保全\n\n")
    f.write("   [課題] 機器交換集中\n")
    f.write("   [対策] 段階的計画\n\n")
    
    f.write("8. 次のステップ\n")
    f.write("   VF-AI-04-M8: 拡張計画\n\n")
    
    f.write("9. 出力ファイル\n")
    f.write("   1. VF_AI_04_M7_results.png\n")
    f.write("   2. VF_AI_04_M7_detailed.png\n")
    f.write("   3. VF_AI_04_M7_costs.csv\n")
    f.write("   4. VF_AI_04_M7_energy.csv\n")
    f.write("   5. VF_AI_04_M7_staff.csv\n")
    f.write("   6. VF_AI_04_M7_equipment.csv\n")
    f.write("   7. VF_AI_04_M7_risks.csv\n")
    f.write("   8. VF_AI_04_M7_report.txt\n")

print("✓ レポート保存: VF_AI_04_M7_report.txt")

# 12. 完了
print("\n" + "=" * 80)
print("✅ VF-AI-04-M7 完了")
print("=" * 80)
print("\n出力ファイル:")
print("1. VF_AI_04_M7_results.png")
print("2. VF_AI_04_M7_detailed.png")
print("3. VF_AI_04_M7_costs.csv")
print("4. VF_AI_04_M7_energy.csv")
print("5. VF_AI_04_M7_staff.csv")
print("6. VF_AI_04_M7_equipment.csv")
print("7. VF_AI_04_M7_risks.csv")
print("8. VF_AI_04_M7_report.txt")
print("\n次のステップ: VF-AI-04-M8")
print("=" * 80)

plt.show()
