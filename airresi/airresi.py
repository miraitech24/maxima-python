#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAG: PROJECTILE_V2
空気抵抗を受ける物体の放物運動解析システム (Python + Maxima連成)
- Maximaで運動方程式の解析解を導出
- Pythonで数値計算・可視化・アニメーション作成
- .macファイルも出力
"""

import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from datetime import datetime, timezone
import csv
import os
import re
import pandas as pd   # ← 追加

# ============================================================
# Maximaコード (運動方程式の解析解導出)
# ============================================================
MAXIMA_CODE = '''/* TAG: PROJECTILE_MAXIMA_V1 */
/* 空気抵抗を受ける物体の放物運動 */
/* 運動方程式: m d^2x/dt^2 = -b dx/dt, m d^2y/dt^2 = -mg - b dy/dt */

kill(all)$

/* 1. 運動方程式の定義 */
eq_x: m * 'diff(x(t), t, 2) = -b * 'diff(x(t), t)$
eq_y: m * 'diff(y(t), t, 2) = -m * g - b * 'diff(y(t), t)$

print("=== 運動方程式 ===")$
print("x方向: ", eq_x)$
print("y方向: ", eq_y)$

/* 2. 初期条件 */
atvalue(x(t), t=0, 0)$
atvalue('diff(x(t),t), t=0, v0 * cos(th))$
atvalue(y(t), t=0, 0)$
atvalue('diff(y(t),t), t=0, v0 * sin(th))$

print("=== 初期条件 ===")$
print("x(0) = 0, x'(0) = v0 cosθ")$
print("y(0) = 0, y'(0) = v0 sinθ")$

/* 3. ラプラス変換で解析解を求める */
sol: desolve([eq_x, eq_y], [x(t), y(t)])$

print("=== 解析解 ===")$
print("x(t) = ", ratsimp(sol[1]))$
print("y(t) = ", ratsimp(sol[2]))$

/* 4. 整理された形式で表示 */
x_sol: sol[1]$
y_sol: sol[2]$

print("=== 整理形式 ===")$
print("x(t) = (m v0 cosθ / b) (1 - e^{-bt/m})")$
print("y(t) = (m/b)(v0 sinθ + mg/b)(1 - e^{-bt/m}) - (mg/b)t")$

/* 5. Python連携用: 数値出力 */
params: [m=0.5, g=9.8, b=0.2, v0=30, th=%pi/4]$

/* ルンゲクッタ法で数値解を計算 */
result: rk([v0*cos(th)*exp(-b*t/m), 
           (v0*sin(th)+m*g/b)*exp(-b*t/m)-m*g/b], 
          [x, y], [0, 0], [t, 0, 5, 0.05]), params$

/* CSV出力 */
out_csv: "trajectory.csv"$
f: openw(out_csv)$
printf(f, "t,x,y~%")$
for row in result do (
    printf(f, "~f,~f,~f~%", row[1], row[2], row[3])
)$
close(f)$

print("=== 計算完了 ===")$
print("CSV出力: ", out_csv)$
quit()$
'''


class ProjectileSolver:
    """空気抵抗を受ける物体の放物運動ソルバー"""
    
    def __init__(self, m=0.5, g=9.8, b=0.2, v0=30, theta_deg=45):
        self.m = m      # 質量 [kg]
        self.g = g      # 重力加速度 [m/s^2]
        self.b = b      # 空気抵抗係数 [kg/s]
        self.v0 = v0    # 初速 [m/s]
        self.theta_deg = theta_deg
        self.theta_rad = np.radians(theta_deg)
        
    def analytic_x(self, t):
        """x方向の解析解: x(t) = (m v0 cosθ / b) (1 - exp(-b t / m))"""
        if self.b == 0:
            return self.v0 * np.cos(self.theta_rad) * t
        return (self.m * self.v0 * np.cos(self.theta_rad) / self.b) * (1 - np.exp(-self.b * t / self.m))
    
    def analytic_y(self, t):
        """y方向の解析解: y(t) = (m/b)(v0 sinθ + mg/b)(1 - exp(-b t/m)) - (mg/b)t"""
        if self.b == 0:
            return self.v0 * np.sin(self.theta_rad) * t - 0.5 * self.g * t**2
        term1 = (self.m / self.b) * (self.v0 * np.sin(self.theta_rad) + self.m * self.g / self.b)
        term2 = 1 - np.exp(-self.b * t / self.m)
        term3 = (self.m * self.g / self.b) * t
        return term1 * term2 - term3
    
    def velocity_x(self, t):
        """x方向速度: vx(t) = v0 cosθ * exp(-b t / m)"""
        if self.b == 0:
            return self.v0 * np.cos(self.theta_rad)
        return self.v0 * np.cos(self.theta_rad) * np.exp(-self.b * t / self.m)
    
    def velocity_y(self, t):
        """y方向速度: vy(t) = (v0 sinθ + mg/b) exp(-b t/m) - mg/b"""
        if self.b == 0:
            return self.v0 * np.sin(self.theta_rad) - self.g * t
        term = (self.v0 * np.sin(self.theta_rad) + self.m * self.g / self.b)
        return term * np.exp(-self.b * t / self.m) - self.m * self.g / self.b
    
    def flight_time(self):
        """飛翔時間 (y(t)=0 となる最小の正の時間)"""
        t = 0
        dt = 0.01
        while t < 10:
            if self.analytic_y(t) < 0:
                return t
            t += dt
        return t
    
    def compute_trajectory(self, t_max=5, dt=0.05):
        """軌道計算"""
        t_vals = np.arange(0, t_max, dt)
        x_vals = [self.analytic_x(t) for t in t_vals]
        y_vals = [self.analytic_y(t) for t in t_vals]
        return t_vals, x_vals, y_vals


def write_mac_file(code, filename="PROJECTILE_model.mac"):
    """.macファイルを出力"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ .macファイル出力: {filename}")
    return filename


def run_maxima(mac_file, timeout=30):
    """Maximaを実行"""
    try:
        result = subprocess.run(
            ["maxima", "--very-quiet", "-b", mac_file],
            capture_output=True, text=True, timeout=timeout, check=False
        )
        if result.returncode != 0:
            print(f"Maxima警告: リターンコード {result.returncode}")
            if result.stderr:
                print(f"エラー出力: {result.stderr[:200]}")
        return result.stdout
    except Exception as e:
        return f"Maxima実行エラー: {e}"


def load_maxima_csv(filename="trajectory.csv"):
    """Maxima生成CSVを読み込む"""
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, 'r') as f:
            content = f.read()
        # 数字以外の文字を削除（カンマと改行は保持）
        clean_content = re.sub(r'[^0-9\.\,\-\n]', '', content)
        # 行ごとにパース
        data = []
        for line in clean_content.strip().split('\n'):
            if line and ',' in line:
                parts = line.split(',')
                if len(parts) >= 3:
                    try:
                        t = float(parts[0])
                        x = float(parts[1])
                        y = float(parts[2])
                        data.append([t, x, y])
                    except:
                        pass
        return data
    except Exception as e:
        print(f"CSV読み込みエラー: {e}")
        return None


def write_csv(t_vals, x_vals, y_vals):
    """CSV出力"""
    with open("PROJECTILE_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["t", "x", "y", "vx", "vy"])
        for t, x, y in zip(t_vals, x_vals, y_vals):
            vx = 0  # 後で計算可能
            vy = 0
            writer.writerow([t, x, y, vx, vy])


def write_summary(solver, maxima_output):
    """サマリーファイル出力"""
    with open("PROJECTILE_summary.txt", "w", encoding="utf-8") as f:
        f.write("空気抵抗を受ける物体の放物運動解析 サマリー\n")
        f.write(f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}Z\n\n")
        f.write("=== 物理パラメータ ===\n")
        f.write(f"質量 m = {solver.m} kg\n")
        f.write(f"重力加速度 g = {solver.g} m/s²\n")
        f.write(f"空気抵抗係数 b = {solver.b} kg/s\n")
        f.write(f"初速 v0 = {solver.v0} m/s\n")
        f.write(f"投射角 θ = {solver.theta_deg}°\n\n")
        
        f.write("=== 計算結果 ===\n")
        t_flight = solver.flight_time()
        x_max = solver.analytic_x(t_flight) if t_flight > 0 else 0
        f.write(f"飛翔時間: {t_flight:.2f} s\n")
        f.write(f"到達距離: {x_max:.2f} m\n\n")
        
        f.write("=== Maxima解析出力 ===\n")
        f.write(maxima_output[:500] if maxima_output else "なし")


def get_font():
    """日本語フォントを自動検出"""
    try:
        import matplotlib.font_manager as fm
        for name in ["IPAexGothic", "IPAGothic", "Noto Sans CJK JP", "Yu Gothic", "MS Gothic"]:
            if name in {t.name for t in fm.fontManager.ttflist}:
                return name
    except Exception:
        pass
    return None


def plot_results(solver, t_vals, x_vals, y_vals):
    """2x2サブプロットの作成"""
    font = get_font()
    if font:
        plt.rcParams["font.family"] = font
        titles = ["放物軌道", "速度の時間変化", "空気抵抗の影響比較", "エネルギー変化"]
        xlab1, xlab2 = "x [m]", "時間 t [s]"
        ylab1, ylab2 = "y [m]", "速度 [m/s]"
        legend_no_resist = "抵抗なし"
        legend_with_resist = "抵抗あり"
    else:
        plt.rcParams["font.family"] = "sans-serif"
        titles = ["Projectile trajectory", "Velocity vs time", "Effect of air resistance", "Energy change"]
        xlab1, xlab2 = "x [m]", "Time t [s]"
        ylab1, ylab2 = "y [m]", "Velocity [m/s]"
        legend_no_resist = "No resistance"
        legend_with_resist = "With resistance"
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"空気抵抗を受ける放物運動 (v0={solver.v0}m/s, θ={solver.theta_deg}°, b={solver.b})", fontsize=14)
    
    # グラフ1: 軌道
    axs[0, 0].plot(x_vals, y_vals, 'b-', lw=2, label=legend_with_resist)
    axs[0, 0].scatter([x_vals[0]], [y_vals[0]], c='green', s=50, label='発射点', zorder=5)
    axs[0, 0].scatter([x_vals[-1]], [y_vals[-1]], c='red', s=50, label='着地点', zorder=5)
    axs[0, 0].set_xlabel(xlab1)
    axs[0, 0].set_ylabel(ylab1)
    axs[0, 0].set_title(titles[0])
    axs[0, 0].grid(True, alpha=0.3)
    axs[0, 0].legend()
    axs[0, 0].set_aspect('equal')
    
    # グラフ2: 速度成分
    vx_vals = [solver.velocity_x(t) for t in t_vals]
    vy_vals = [solver.velocity_y(t) for t in t_vals]
    v_vals = [np.sqrt(vx**2 + vy**2) for vx, vy in zip(vx_vals, vy_vals)]
    axs[0, 1].plot(t_vals, vx_vals, 'r-', lw=2, label='vx')
    axs[0, 1].plot(t_vals, vy_vals, 'g-', lw=2, label='vy')
    axs[0, 1].plot(t_vals, v_vals, 'b--', lw=2, label='速度')
    axs[0, 1].set_xlabel(xlab2)
    axs[0, 1].set_ylabel(ylab2)
    axs[0, 1].set_title(titles[1])
    axs[0, 1].legend()
    axs[0, 1].grid(True, alpha=0.3)
    
    # グラフ3: 空気抵抗の影響比較
    solver_no_resist = ProjectileSolver(m=solver.m, g=solver.g, b=0, v0=solver.v0, theta_deg=solver.theta_deg)
    _, x_no, y_no = solver_no_resist.compute_trajectory(t_max=5, dt=0.05)
    axs[1, 0].plot(x_vals, y_vals, 'b-', lw=2, label=legend_with_resist)
    axs[1, 0].plot(x_no, y_no, 'r--', lw=2, label=legend_no_resist)
    axs[1, 0].set_xlabel(xlab1)
    axs[1, 0].set_ylabel(ylab1)
    axs[1, 0].set_title(titles[2])
    axs[1, 0].legend()
    axs[1, 0].grid(True, alpha=0.3)
    axs[1, 0].set_aspect('equal')
    
    # グラフ4: エネルギー変化
    ke_vals = [0.5 * solver.m * v**2 for v in v_vals]
    pe_vals = [solver.m * solver.g * y for y in y_vals]
    total_e = [ke + pe for ke, pe in zip(ke_vals, pe_vals)]
    axs[1, 1].plot(t_vals, ke_vals, 'r-', lw=2, label='運動エネルギー')
    axs[1, 1].plot(t_vals, pe_vals, 'g-', lw=2, label='位置エネルギー')
    axs[1, 1].plot(t_vals, total_e, 'b--', lw=2, label='全エネルギー')
    axs[1, 1].set_xlabel(xlab2)
    axs[1, 1].set_ylabel("エネルギー [J]")
    axs[1, 1].set_title(titles[3])
    axs[1, 1].legend()
    axs[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig("PROJECTILE_plots.png", dpi=150, bbox_inches='tight')
    plt.close(fig)


def create_animation(df, output_file="projectile_motion.gif"):
    """アニメーションGIF作成"""
    if df is None or len(df) < 2:
        print("アニメーション: データ不足")
        return
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(0, df['x'].max() * 1.1 if df['x'].max() > 0 else 100)
    ax.set_ylim(0, df['y'].max() * 1.1 if df['y'].max() > 0 else 50)
    ax.set_xlabel("Distance x [m]")
    ax.set_ylabel("Height y [m]")
    ax.set_title("Projectile motion with air resistance")
    ax.grid(True, linestyle=':')
    
    line, = ax.plot([], [], 'b-', lw=2, label='Trajectory')
    point, = ax.plot([], [], 'ro', markersize=8, label='Projectile')
    ax.legend()
    
    def update(frame):
        line.set_data(df['x'][:frame], df['y'][:frame])
        if frame > 0:
            point.set_data([df['x'].iloc[frame-1]], [df['y'].iloc[frame-1]])
        return line, point
    
    ani = FuncAnimation(fig, update, frames=len(df), interval=30, blit=True, repeat=False)
    
    try:
        ani.save(output_file, writer=PillowWriter(fps=30))
        print(f"✅ アニメーション保存: {output_file}")
    except Exception as e:
        print(f"アニメーション保存エラー: {e}")
    
    plt.close(fig)


def write_spec_md(solver, maxima_output):
    """課題仕様と結論を.mdに出力"""
    t_flight = solver.flight_time()
    x_max = solver.analytic_x(t_flight) if t_flight > 0 else 0
    
    with open("PROJECTILE_spec.md", "w", encoding="utf-8") as f:
        f.write("# 空気抵抗を受ける物体の放物運動解析システム\n\n")
        f.write("## 課題仕様\n\n")
        
        f.write("### 目的\n")
        f.write("速度に比例する空気抵抗 $F = -bv$ を受ける物体の放物運動を解析する。\n")
        f.write("Maximaで運動方程式の解析解を導出し、Pythonで数値計算・可視化を行う。\n\n")
        
        f.write("### 数式モデル\n\n")
        f.write("#### 運動方程式\n")
        f.write("$$\n")
        f.write("m\\frac{d^2x}{dt^2} = -b\\frac{dx}{dt}\n")
        f.write("$$\n\n")
        f.write("$$\n")
        f.write("m\\frac{d^2y}{dt^2} = -mg - b\\frac{dy}{dt}\n")
        f.write("$$\n\n")
        
        f.write("#### 初期条件\n")
        f.write("$$\n")
        f.write("x(0)=0,\\quad \\dot{x}(0)=v_0\\cos\\theta,\\quad ")
        f.write("y(0)=0,\\quad \\dot{y}(0)=v_0\\sin\\theta\n")
        f.write("$$\n\n")
        
        f.write("#### 解析解\n")
        f.write("$$\n")
        f.write("x(t) = \\frac{m v_0 \\cos\\theta}{b} \\left(1 - e^{-bt/m}\\right)\n")
        f.write("$$\n\n")
        f.write("$$\n")
        f.write("y(t) = \\frac{m}{b}\\left(v_0\\sin\\theta + \\frac{mg}{b}\\right)\\left(1 - e^{-bt/m}\\right) - \\frac{mg}{b}t\n")
        f.write("$$\n\n")
        
        f.write("### パラメータ\n\n")
        f.write("| パラメータ | 値 | 単位 | 説明 |\n")
        f.write("|----------|-----|------|------|\n")
        f.write(f"| m | {solver.m} | kg | 質量 |\n")
        f.write(f"| g | {solver.g} | m/s² | 重力加速度 |\n")
        f.write(f"| b | {solver.b} | kg/s | 空気抵抗係数 |\n")
        f.write(f"| v0 | {solver.v0} | m/s | 初速 |\n")
        f.write(f"| θ | {solver.theta_deg} | deg | 投射角 |\n\n")
        
        f.write("## 結論\n\n")
        
        f.write(f"### 計算結果\n\n")
        f.write(f"- **飛翔時間**: {t_flight:.2f} 秒\n")
        f.write(f"- **到達距離**: {x_max:.2f} m\n\n")
        
        f.write("### 物理的考察\n\n")
        f.write("1. **空気抵抗の効果**:\n")
        f.write("   - 抵抗なしの場合、軌道は放物線\n")
        f.write("   - 抵抗がある場合、軌道は非対称で到達距離が減少\n")
        f.write("   - 速度が指数関数的に減衰する\n\n")
        
        f.write("2. **終端速度**:\n")
        f.write("   - y方向の終端速度: $v_{term} = mg/b$\n")
        f.write(f"   - 本例では $v_{{term}} = {solver.m * solver.g / solver.b:.1f}$ m/s\n\n")
        
        f.write("3. **エネルギー散逸**:\n")
        f.write("   - 空気抵抗により力学的エネルギーが減少\n")
        f.write("   - 損失は熱として散逸\n\n")
        
        f.write("### Maxima連成の効果\n\n")
        f.write("1. **記号計算**: 微分方程式の解析解を正確に導出\n")
        f.write("2. **検証可能性**: 導出過程が.macファイルとして残る\n")
        f.write("3. **再現性**: 誰でも同じ計算を再現可能\n\n")
        
        f.write("### 今後の課題\n\n")
        f.write("- 空気抵抗の速度2乗則 ($F = -cv^2$) への拡張\n")
        f.write("- 風の影響を考慮した3次元運動\n")
        f.write("- 回転効果（マグヌス効果）の導入\n")


def main():
    print("=" * 60)
    print("空気抵抗を受ける物体の放物運動解析システム")
    print("(Python + Maxima連成)")
    print("=" * 60)
    
    # 1. .macファイル出力
    print("\n[1] .macファイル出力中...")
    mac_file = write_mac_file(MAXIMA_CODE, "PROJECTILE_model.mac")
    
    # 2. Maxima実行
    print("\n[2] Maximaで解析解導出中...")
    maxima_out = run_maxima(mac_file)
    print("Maxima出力:", maxima_out[:300] if maxima_out else "なし")
    
    # 3. Maxima生成CSV読み込み
    print("\n[3] Maxima生成CSV読み込み中...")
    maxima_data = load_maxima_csv("trajectory.csv")
    if maxima_data:
        print(f"  {len(maxima_data)} データ点読み込み")
    
    # 4. Pythonソルバー実行
    print("\n[4] Pythonソルバー実行中...")
    solver = ProjectileSolver(m=0.5, g=9.8, b=0.2, v0=30, theta_deg=45)
    t_vals, x_vals, y_vals = solver.compute_trajectory(t_max=5, dt=0.05)
    print(f"  軌道計算完了: {len(t_vals)} 点")
    
    # 5. 出力
    print("\n[5] 結果出力中...")
    write_csv(t_vals, x_vals, y_vals)
    write_summary(solver, maxima_out)
    plot_results(solver, t_vals, x_vals, y_vals)
    write_spec_md(solver, maxima_out)
    
    # 6. アニメーション作成
    print("\n[6] アニメーション作成中...")
    if maxima_data:
        # pandas DataFrameに変換
        df = pd.DataFrame(maxima_data, columns=['t', 'x', 'y'])
        create_animation(df, "projectile_motion.gif")
    else:
        df = pd.DataFrame({'t': t_vals, 'x': x_vals, 'y': y_vals})
        create_animation(df, "projectile_motion.gif")
    
    print("\n" + "=" * 60)
    print("出力ファイル:")
    print("  - PROJECTILE_model.mac        (Maximaコード - 生きた仕様書)")
    print("  - PROJECTILE_results.csv      (軌道数値データ)")
    print("  - PROJECTILE_summary.txt      (サマリー)")
    print("  - PROJECTILE_plots.png        (2x2グラフ)")
    print("  - PROJECTILE_spec.md          (仕様+結論)")
    print("  - projectile_motion.gif       (アニメーション)")
    print("  - trajectory.csv              (Maxima生成軌道)")
    print("=" * 60)


if __name__ == "__main__":
    main()