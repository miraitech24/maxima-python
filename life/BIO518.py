import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

# 日本語フォント自動検出
def setup_japanese_font():
    try:
        if os.path.exists('/System/Library/Fonts/ヒラギノ角ゴシック.ttc'):
            plt.rcParams['font.family'] = 'Hiragino Sans'
            return True
        elif os.path.exists('C:/Windows/Fonts/msgothic.ttc'):
            plt.rcParams['font.family'] = 'MS Gothic'
            return True
        elif os.path.exists('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'):
            plt.rcParams['font.family'] = 'IPAexGothic'
            return True
        else:
            plt.rcParams['font.family'] = 'DejaVu Sans'
            return False
    except:
        plt.rcParams['font.family'] = 'DejaVu Sans'
        return False

is_japanese = setup_japanese_font()
lang = 'ja' if is_japanese else 'en'

# .macファイルの生成（修正版：微分を数値的に計算）
def generate_mac_file():
    mac_content = """/* BIO-518: Humanity Preservation Threshold Analysis */
/* 人間性保持限界値の分析 */

/* パラメータ設定 */
x0: 0.5;  /* 閾値中央 */
k: 10.0;  /* 傾きパラメータ */

/* 人間性指数関数 H(x) = 1 / (1 + exp(-k*(x0 - x))) */
H(x) := 1 / (1 + exp(-k * (x0 - x)));

/* 数値微分（解析的微分は関数定義で計算） */
/* dH(x) := k * H(x) * (1 - H(x));  ← 解析的微分を使用 */
dH_analytic(x) := k * H(x) * (1 - H(x));

/* 各改造度での計算 */
alpha_list: [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];

print("=== Humanity Index Calculation ===")$
for a in alpha_list do (
    H_val: H(a),
    dH_val: dH_analytic(a),
    print("alpha=", a, " H=", H_val, " dH/dalpha=", dH_val)
)$

/* 閾値判定 */
threshold: 0.7;
print("=== Threshold Analysis ===")$
print("Threshold: H_critical =", threshold)$

/* 各タスクの改造度 */
tasks: [
    ["BIO-507", 0.15],  /* 老化抑制 */
    ["BIO-502", 0.20],  /* 異種臓器 */
    ["BIO-505", 0.25],  /* 光合成 */
    ["BIO-506", 0.30],  /* 代謝改変 */
    ["BIO-504", 0.35],  /* 宇宙適応 */
    ["BIO-510", 0.40],  /* 集団適応 */
    ["BIO-511", 0.45],  /* 生殖改変 */
    ["BIO-513", 0.50],  /* エネルギー */
    ["BIO-520", 0.55],  /* 社会構造 */
    ["BIO-501", 0.65],  /* BMI接合 */
    ["BIO-503", 0.70],  /* 感覚置換 */
    ["BIO-512", 0.75],  /* 生態系構築 */
    ["BIO-508", 0.85],  /* 記憶転送 */
    ["BIO-509", 0.90],  /* 意識継続性 */
    ["BIO-516", 0.95]   /* 情報生命 */
];

print("")$
print("Task ID | Modification | H(alpha) | Judgment")$
for task in tasks do (
    task_id: task[1],
    mod: task[2],
    H_val: H(mod),
    if H_val >= threshold then
        judgment: "Within"
    else
        judgment: "Beyond",
    print(task_id, " | ", mod, " | ", H_val, " | ", judgment)
)$

/* 解析的な微分の確認 */
print("")$
print("=== Analytical Derivative Verification ===")$
print("dH/dx = k * H * (1 - H)")$
for a in [0.3, 0.5, 0.7, 0.8] do (
    H_a: H(a),
    dH_analytical: k * H_a * (1 - H_a),
    print("alpha=", a, " H=", H_a, " dH/dalpha=", dH_analytical)
)$
"""
    with open('bio518_analysis.mac', 'w', encoding='utf-8') as f:
        f.write(mac_content)
    print("[INFO] .mac file saved: bio518_analysis.mac")

# .macファイル生成
generate_mac_file()

# Maximaで.macファイルを実行
def run_maxima_script():
    try:
        cmd = 'maxima --very-quiet -b bio518_analysis.mac'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("[INFO] Maxima script executed")
        print(result.stdout)
        if result.stderr:
            print("[WARN] Maxima stderr:", result.stderr)
    except Exception as e:
        print(f"[ERROR] Maxima execution failed: {e}")

# メイン計算（Python側でも実行）
print("=" * 60)
if lang == 'ja':
    print("BIO-518: 人間性保持限界値の分析")
else:
    print("BIO-518: Analysis of Humanity Preservation Threshold")
print("=" * 60)

x0 = 0.5
k = 10.0
threshold = 0.7

# 改造度の範囲
x_vals = np.linspace(0, 1, 100)
H_vals = 1 / (1 + np.exp(-k * (x0 - x_vals)))

# 感度分析（解析的微分を使用）
print("\n--- Sensitivity Analysis ---")
for alpha in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    H_alpha = 1 / (1 + np.exp(-k * (x0 - alpha)))
    dH_dalpha = k * H_alpha * (1 - H_alpha)  # 解析的微分
    if lang == 'ja':
        print(f"改造度 α={alpha:.1f}: H={H_alpha:.4f}, dH/dα={dH_dalpha:.4f}")
    else:
        print(f"Modification α={alpha:.1f}: H={H_alpha:.4f}, dH/dα={dH_dalpha:.4f}")

# 閾値判定
print("\n--- Threshold Analysis ---")
tasks = {
    'BIO-507': 0.15, 'BIO-502': 0.20, 'BIO-505': 0.25, 'BIO-506': 0.30,
    'BIO-504': 0.35, 'BIO-510': 0.40, 'BIO-511': 0.45, 'BIO-513': 0.50,
    'BIO-520': 0.55, 'BIO-501': 0.65, 'BIO-503': 0.70, 'BIO-512': 0.75,
    'BIO-508': 0.85, 'BIO-509': 0.90, 'BIO-516': 0.95
}

if lang == 'ja':
    print(f"{'Task ID':<12} {'改造度':<10} {'人間性指数':<12} {'判定':<10}")
    print("-" * 44)
else:
    print(f"{'Task ID':<12} {'Modification':<12} {'Humanity Index':<14} {'Judgment':<10}")
    print("-" * 48)

within_threshold = []
beyond_threshold = []

for task_id, mod_level in sorted(tasks.items(), key=lambda x: x[1]):
    H_val = 1 / (1 + np.exp(-k * (x0 - mod_level)))
    judgment = "✓ 閾値内" if H_val >= threshold else "✗ 閾値外"
    
    if lang == 'ja':
        print(f"{task_id:<12} {mod_level:<10.2f} {H_val:<12.4f} {judgment:<10}")
    else:
        judgment_en = "Within" if H_val >= threshold else "Beyond"
        print(f"{task_id:<12} {mod_level:<12.2f} {H_val:<14.4f} {judgment_en:<10}")
    
    if H_val >= threshold:
        within_threshold.append(task_id)
    else:
        beyond_threshold.append(task_id)

print("\n--- Summary ---")
if lang == 'ja':
    print(f"閾値内タスク ({len(within_threshold)}件): {', '.join(within_threshold)}")
    print(f"閾値外タスク ({len(beyond_threshold)}件): {', '.join(beyond_threshold)}")
else:
    print(f"Within threshold ({len(within_threshold)} tasks): {', '.join(within_threshold)}")
    print(f"Beyond threshold ({len(beyond_threshold)} tasks): {', '.join(beyond_threshold)}")

# Maximaスクリプトも実行
print("\n" + "=" * 60)
print("Maxima Script Execution:")
print("=" * 60)
run_maxima_script()

# グラフ作成
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# グラフ1: 人間性指数曲線
ax1 = axes[0, 0]
ax1.plot(x_vals, H_vals, 'b-', linewidth=2, label='H(x)' if lang == 'en' else '人間性指数')
ax1.axhline(y=threshold, color='r', linestyle='--', alpha=0.7, 
            label=f'Threshold={threshold}' if lang == 'en' else f'閾値={threshold}')
ax1.axvline(x=x0, color='g', linestyle=':', alpha=0.5, label=f'x₀={x0}')
ax1.fill_between(x_vals, 0, threshold, alpha=0.1, color='red')
ax1.fill_between(x_vals, threshold, 1, alpha=0.1, color='green')
if lang == 'ja':
    ax1.set_xlabel('改造度 (α)')
    ax1.set_ylabel('人間性指数 H(α)')
    ax1.set_title('人間性指数曲線')
else:
    ax1.set_xlabel('Modification Level (α)')
    ax1.set_ylabel('Humanity Index H(α)')
    ax1.set_title('Humanity Index Curve')
ax1.grid(True, alpha=0.3)
ax1.legend()
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)

# グラフ2: 感度分析
ax2 = axes[0, 1]
dH_vals = k * H_vals * (1 - H_vals)
ax2.plot(x_vals, dH_vals, 'r-', linewidth=2, label='dH/dα' if lang == 'en' else '感度')
ax2.axvline(x=x0, color='g', linestyle=':', alpha=0.5, label=f'x₀={x0}')
if lang == 'ja':
    ax2.set_xlabel('改造度 (α)')
    ax2.set_ylabel('感度 dH/dα')
    ax2.set_title('感度分析（微分）')
else:
    ax2.set_xlabel('Modification Level (α)')
    ax2.set_ylabel('Sensitivity dH/dα')
    ax2.set_title('Sensitivity Analysis (Derivative)')
ax2.grid(True, alpha=0.3)
ax2.legend()
ax2.set_xlim(0, 1)

# グラフ3: タスク別人間性指数
ax3 = axes[1, 0]
task_names = list(tasks.keys())
task_mods = list(tasks.values())
task_H = [1 / (1 + np.exp(-k * (x0 - m))) for m in task_mods]
colors = ['green' if h >= threshold else 'red' for h in task_H]
bars = ax3.barh(task_names, task_H, color=colors, alpha=0.7)
ax3.axvline(x=threshold, color='blue', linestyle='--', linewidth=2, 
            label=f'Threshold={threshold}' if lang == 'en' else f'閾値={threshold}')
if lang == 'ja':
    ax3.set_xlabel('人間性指数')
    ax3.set_title('タスク別人間性指数')
else:
    ax3.set_xlabel('Humanity Index')
    ax3.set_title('Humanity Index by Task')
ax3.grid(True, alpha=0.3, axis='x')
ax3.legend()
ax3.set_xlim(0, 1)

# グラフ4: 改造度 vs 人間性指数
ax4 = axes[1, 1]
scatter = ax4.scatter(task_mods, task_H, c=task_H, cmap='RdYlGn', s=100, alpha=0.8)
ax4.plot([0, 1], [0, 1], 'k--', alpha=0.3, label='y=x')
ax4.axhline(y=threshold, color='blue', linestyle='--', alpha=0.7, 
            label=f'Threshold={threshold}' if lang == 'en' else f'閾値={threshold}')
for i, task_id in enumerate(task_names):
    ax4.annotate(task_id, (task_mods[i], task_H[i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=8)
if lang == 'ja':
    ax4.set_xlabel('改造度 (α)')
    ax4.set_ylabel('人間性指数 H(α)')
    ax4.set_title('改造度 vs 人間性指数')
else:
    ax4.set_xlabel('Modification Level (α)')
    ax4.set_ylabel('Humanity Index H(α)')
    ax4.set_title('Modification vs Humanity Index')
ax4.grid(True, alpha=0.3)
ax4.legend()
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
plt.colorbar(scatter, ax=ax4, label='H' if lang == 'en' else '人間性指数')

plt.tight_layout()
plt.savefig('bio518_humanity_threshold.png', dpi=150, bbox_inches='tight')
print(f"\n[INFO] Graph saved: bio518_humanity_threshold.png")

# CSV結果出力
with open('bio518_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if lang == 'ja':
        writer.writerow(['Task ID', '改造度', '人間性指数', '判定'])
    else:
        writer.writerow(['Task ID', 'Modification', 'Humanity Index', 'Judgment'])
    for task_id, mod_level in sorted(tasks.items(), key=lambda x: x[1]):
        H_val = 1 / (1 + np.exp(-k * (x0 - mod_level)))
        judgment = "Within" if H_val >= threshold else "Beyond"
        writer.writerow([task_id, f"{mod_level:.2f}", f"{H_val:.4f}", judgment])

print(f"[INFO] CSV saved: bio518_results.csv")

# サマリーファイル
with open('bio518_summary.md', 'w', encoding='utf-8') as f:
    f.write("# BIO-518: Humanity Preservation Threshold Analysis\n\n")
    f.write("## Model\n\n")
    f.write("$$H(\\alpha) = \\frac{1}{1 + e^{-k(\\alpha_0 - \\alpha)}}$$\n\n")
    f.write(f"- Threshold central: $\\alpha_0 = {x0}$\n")
    f.write(f"- Slope: $k = {k}$\n")
    f.write(f"- Humanity threshold: $H_{{\\text{{critical}}}} = {threshold}$\n\n")
    f.write("## Sensitivity\n\n")
    f.write("$$\\frac{dH}{d\\alpha} = k \\cdot H \\cdot (1 - H)$$\n\n")
    f.write("## Results\n\n")
    f.write(f"- Within threshold: {len(within_threshold)} tasks\n")
    f.write(f"- Beyond threshold: {len(beyond_threshold)} tasks\n\n")
    f.write("### Within Threshold Tasks\n")
    for t in within_threshold:
        f.write(f"- {t}\n")
    f.write("\n### Beyond Threshold Tasks\n")
    for t in beyond_threshold:
        f.write(f"- {t}\n")
    f.write("\n## Graph Description\n\n")
    f.write("### Figure 1: Humanity Index Curve\n")
    f.write("Shows the sigmoid function H(α) with threshold line at H=0.7.\n")
    f.write("Green region: within threshold, Red region: beyond threshold.\n\n")
    f.write("### Figure 2: Sensitivity Analysis\n")
    f.write("Derivative dH/dα showing maximum sensitivity at α₀=0.5.\n\n")
    f.write("### Figure 3: Humanity Index by Task\n")
    f.write("Horizontal bar chart showing each task's humanity index.\n")
    f.write("Green bars: within threshold, Red bars: beyond threshold.\n\n")
    f.write("### Figure 4: Modification vs Humanity Index\n")
    f.write("Scatter plot with color gradient showing task distribution.\n")
    f.write("Color: green (high humanity) to red (low humanity).\n")

print(f"[INFO] Summary saved: bio518_summary.md")
plt.show()