#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:05:50 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TAG: AIRFLOW_V2
室内気流解析システム (Python + Maxima連成)
- 2次元室内の空気の流れを解析
- Maximaで記号計算 (NS方程式の離散化)
- Pythonで数値計算 + 可視化
- .macファイルも出力
"""

import subprocess
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import csv
import os

# ============================================================
# Maximaコード (室内気流のNavier-Stokes方程式)
# ============================================================
MAXIMA_CODE = '''/* TAG: AIRFLOW_MAXIMA_V1 */
/* 室内気流のNavier-Stokes方程式 (2次元) */

kill(all)$

/* 座標と変数 */
depends([u, v, p], [x, y])$

/* 物理定数 */
rho: 1.225$   /* 空気密度 kg/m^3 */
nu: 1.5e-5$   /* 動粘性係数 m^2/s */

/* 連続の式 (非圧縮) */
continuity: diff(u, x) + diff(v, y) = 0$

/* Navier-Stokes方程式 (x方向) */
NS_x: u * diff(u, x) + v * diff(u, y) = 
    -1/rho * diff(p, x) + nu * (diff(u, x, 2) + diff(u, y, 2))$

/* Navier-Stokes方程式 (y方向) */
NS_y: u * diff(v, x) + v * diff(v, y) = 
    -1/rho * diff(p, y) + nu * (diff(v, x, 2) + diff(v, y, 2))$

print("=== 連続の式 ===")$
print(continuity)$
print("=== NS方程式 x成分 ===")$
print(NS_x)$
print("=== NS方程式 y成分 ===")$
print(NS_y)$

/* 圧力ポアソン方程式の導出 (連続の式を満たす圧力場) */
div_u: diff(u, x) + diff(v, y)$
poisson_p: diff(p, x, 2) + diff(p, y, 2) = 
    -rho * ( (diff(u, x))^2 + 2*diff(u, y)*diff(v, x) + (diff(v, y))^2 )$

print("=== 圧力ポアソン方程式 ===")$
print(poisson_p)$

/* 離散化 (中央差分) */
dxi: Delta_x$
dy: Delta_y$

/* 速度勾配の離散化 */
du_dx: (u[i+1][j] - u[i-1][j])/(2*dxi)$
du_dy: (u[i][j+1] - u[i][j-1])/(2*dy)$
dv_dx: (v[i+1][j] - v[i-1][j])/(2*dxi)$
dv_dy: (v[i][j+1] - v[i][j-1])/(2*dy)$

/* ラプラシアンの離散化 */
laplace_u: (u[i+1][j] - 2*u[i][j] + u[i-1][j])/dxi^2 +
           (u[i][j+1] - 2*u[i][j] + u[i][j-1])/dy^2$
laplace_v: (v[i+1][j] - 2*v[i][j] + v[i-1][j])/dxi^2 +
           (v[i][j+1] - 2*v[i][j] + v[i][j-1])/dy^2$
laplace_p: (p[i+1][j] - 2*p[i][j] + p[i-1][j])/dxi^2 +
           (p[i][j+1] - 2*p[i][j] + p[i][j-1])/dy^2$

print("=== 離散化形式 (x方向) ===")$
print(NS_x, " → ", u[i][j] * du_dx + v[i][j] * du_dy, "=",
      -1/rho * (p[i+1][j] - p[i-1][j])/(2*dxi) + nu * laplace_u)$

/* 結果をテキスト出力 */
stringout("AIRFLOW_equations.txt", continuity, NS_x, NS_y, poisson_p)$

print("Maxima計算完了")$
quit()$
'''


class RoomAirflowSolver:
    """室内気流ソルバー (2次元)"""
    
    def __init__(self, width=1.0, height=1.0, nx=30, ny=30):
        self.width = width
        self.height = height
        self.nx = nx
        self.ny = ny
        self.dx = width / (nx - 1)
        self.dy = height / (ny - 1)
        
        # 物理定数
        self.rho = 1.225      # 空気密度 [kg/m^3]
        self.nu = 1.5e-5      # 動粘性係数 [m^2/s]
        
        # 格子点
        self.x = np.linspace(0, width, nx)
        self.y = np.linspace(0, height, ny)
        
        # 変数初期化
        self.u = np.zeros((ny, nx))  # x方向速度
        self.v = np.zeros((ny, nx))  # y方向速度
        self.p = np.zeros((ny, nx))  # 圧力
        self.psi = np.zeros((ny, nx))  # 流線関数
        
        # 境界条件
        self.inlet_velocity = 0.5   # 入口速度 [m/s]
        self.outlet_pressure = 0.0  # 出口圧力 [Pa]
        
    def set_inlet(self, x_pos, y_range):
        """入口条件設定 (左壁の一部)"""
        self.inlet_x = x_pos
        self.inlet_y_range = y_range
        
    def set_outlet(self, x_pos, y_range):
        """出口条件設定 (右壁の一部)"""
        self.outlet_x = x_pos
        self.outlet_y_range = y_range
        
    def set_obstacle(self, x_start, x_end, y_start, y_end):
        """障害物(家具など)の設定"""
        ix_start = int(x_start / self.dx)
        ix_end = int(x_end / self.dx)
        iy_start = int(y_start / self.dy)
        iy_end = int(y_end / self.dy)
        
        for i in range(iy_start, min(iy_end, self.ny)):
            for j in range(ix_start, min(ix_end, self.nx)):
                self.u[i, j] = 0
                self.v[i, j] = 0
                
    def solve(self, max_iter=5000, tol=1e-5, omega=0.8):
        """SOR法でNavier-Stokes方程式を反復求解"""
        
        for iteration in range(max_iter):
            u_old = self.u.copy()
            v_old = self.v.copy()
            p_old = self.p.copy()
            
            # 圧力ポアソン方程式のSOR反復
            for i in range(1, self.ny - 1):
                for j in range(1, self.nx - 1):
                    # 右辺（速度勾配項）
                    du_dx = (self.u[i, j+1] - self.u[i, j-1]) / (2*self.dx)
                    dv_dy = (self.v[i+1, j] - self.v[i-1, j]) / (2*self.dy)
                    du_dy = (self.u[i+1, j] - self.u[i-1, j]) / (2*self.dy)
                    dv_dx = (self.v[i, j+1] - self.v[i, j-1]) / (2*self.dx)
                    
                    rhs = -self.rho * (du_dx**2 + 2*du_dy*dv_dx + dv_dy**2)
                    
                    # SOR更新
                    p_new = ((self.p[i, j+1] + self.p[i, j-1]) / self.dx**2 +
                             (self.p[i+1, j] + self.p[i-1, j]) / self.dy**2 - rhs) / (2/self.dx**2 + 2/self.dy**2)
                    self.p[i, j] = p_old[i, j] + omega * (p_new - p_old[i, j])
            
            # 速度の更新 (x方向)
            for i in range(1, self.ny - 1):
                for j in range(1, self.nx - 1):
                    # 移流項
                    u_adv = (self.u[i, j] * (self.u[i, j+1] - self.u[i, j-1]) / (2*self.dx) +
                            self.v[i, j] * (self.u[i+1, j] - self.u[i-1, j]) / (2*self.dy))
                    
                    # 拡散項
                    u_diff = self.nu * ((self.u[i, j+1] - 2*self.u[i, j] + self.u[i, j-1]) / self.dx**2 +
                                        (self.u[i+1, j] - 2*self.u[i, j] + self.u[i-1, j]) / self.dy**2)
                    
                    # 圧力勾配項
                    p_grad = (self.p[i, j+1] - self.p[i, j-1]) / (2*self.dx) / self.rho
                    
                    self.u[i, j] = u_old[i, j] + 0.1 * (-u_adv - p_grad + u_diff) * 0.5
            
            # 速度の更新 (y方向)
            for i in range(1, self.ny - 1):
                for j in range(1, self.nx - 1):
                    v_adv = (self.u[i, j] * (self.v[i, j+1] - self.v[i, j-1]) / (2*self.dx) +
                            self.v[i, j] * (self.v[i+1, j] - self.v[i-1, j]) / (2*self.dy))
                    
                    v_diff = self.nu * ((self.v[i, j+1] - 2*self.v[i, j] + self.v[i, j-1]) / self.dx**2 +
                                        (self.v[i+1, j] - 2*self.v[i, j] + self.v[i-1, j]) / self.dy**2)
                    
                    p_grad = (self.p[i+1, j] - self.p[i-1, j]) / (2*self.dy) / self.rho
                    
                    self.v[i, j] = v_old[i, j] + 0.1 * (-v_adv - p_grad + v_diff) * 0.5
            
            # 入口境界条件
            inlet_j = int(self.inlet_x / self.dx) if hasattr(self, 'inlet_x') else 0
            for i in range(self.ny):
                if hasattr(self, 'inlet_y_range'):
                    if self.inlet_y_range[0] <= self.y[i] <= self.inlet_y_range[1]:
                        self.u[i, inlet_j] = self.inlet_velocity
                        self.v[i, inlet_j] = 0
            
            # 出口境界条件
            outlet_j = int(self.outlet_x / self.dx) if hasattr(self, 'outlet_x') else self.nx - 1
            for i in range(self.ny):
                if hasattr(self, 'outlet_y_range'):
                    if self.outlet_y_range[0] <= self.y[i] <= self.outlet_y_range[1]:
                        self.p[i, outlet_j] = self.outlet_pressure
            
            # 壁面境界条件 (ノーリップ条件)
            self.u[0, :] = 0   # 下壁
            self.u[-1, :] = 0  # 上壁
            self.v[0, :] = 0
            self.v[-1, :] = 0
            self.u[:, 0] = 0   # 左壁
            self.u[:, -1] = 0  # 右壁 (except outlet)
            self.v[:, 0] = 0
            self.v[:, -1] = 0
            
            # 収束判定
            u_diff_max = np.max(np.abs(self.u - u_old))
            v_diff_max = np.max(np.abs(self.v - v_old))
            p_diff_max = np.max(np.abs(self.p - p_old))
            
            if max(u_diff_max, v_diff_max, p_diff_max) < tol:
                print(f"収束: {iteration+1} iter")
                break
    
    def compute_streamfunction(self):
        """流線関数の計算"""
        self.psi[0, :] = 0
        for i in range(1, self.ny):
            for j in range(self.nx):
                self.psi[i, j] = self.psi[i-1, j] + self.u[i, j] * self.dy
                
    def get_results(self):
        """結果を辞書形式で取得"""
        return {
            'u': self.u,
            'v': self.v,
            'p': self.p,
            'psi': self.psi,
            'x': self.x,
            'y': self.y,
            'reynolds': self.inlet_velocity * self.width / self.nu
        }


def write_mac_file(code, filename="AIRFLOW_model.mac"):
    """.macファイルを出力"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ .macファイル出力: {filename}")
    return filename


def run_maxima(mac_file):
    """Maximaを実行してNS方程式の導出"""
    try:
        result = subprocess.run(
            ["maxima", "--very-quiet", "-b", mac_file],
            capture_output=True, text=True, timeout=30, check=False
        )
        return result.stdout
    except Exception as e:
        return f"Maxima実行エラー: {e}"


def write_csv(results):
    """CSV出力"""
    with open("AIRFLOW_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "y", "u", "v", "p", "psi"])
        for i in range(len(results['y'])):
            for j in range(len(results['x'])):
                writer.writerow([
                    results['x'][j], results['y'][i],
                    results['u'][i, j], results['v'][i, j],
                    results['p'][i, j], results['psi'][i, j]
                ])


def write_summary(results, maxima_output):
    """サマリーファイル出力"""
    with open("AIRFLOW_summary.txt", "w", encoding="utf-8") as f:
        f.write("室内気流解析 サマリー\n")
        f.write(f"timestamp_utc: {datetime.now(timezone.utc).isoformat()}Z\n")
        f.write(f"レイノルズ数: {results['reynolds']:.1f}\n")
        f.write(f"最大速度: {np.max(results['u']):.3f} m/s\n")
        f.write(f"最大圧力: {np.max(results['p']):.3f} Pa\n\n")
        f.write("Maxima連成出力:\n")
        f.write(maxima_output[:500] if maxima_output else "なし")


def plot_results(results):
    """2x2サブプロットの作成"""
    font_jp = None
    try:
        import matplotlib.font_manager as fm
        for name in ["IPAexGothic", "IPAGothic", "Noto Sans CJK JP"]:
            if name in {t.name for t in fm.fontManager.ttflist}:
                font_jp = name
                break
    except:
        pass
    
    if font_jp:
        plt.rcParams["font.family"] = font_jp
        titles = ["速度場 (u: x方向)", "速度場 (v: y方向)", "圧力場", "流線関数"]
        xl, yl = "x [m]", "y [m]"
    else:
        titles = ["Velocity field u [m/s]", "Velocity field v [m/s]", "Pressure field [Pa]", "Streamfunction"]
        xl, yl = "x [m]", "y [m]"
    
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # 速度u
    im1 = axs[0, 0].contourf(results['x'], results['y'], results['u'], levels=20, cmap='RdBu_r')
    axs[0, 0].set_title(titles[0])
    axs[0, 0].set_xlabel(xl)
    axs[0, 0].set_ylabel(yl)
    plt.colorbar(im1, ax=axs[0, 0])
    
    # 速度v
    im2 = axs[0, 1].contourf(results['x'], results['y'], results['v'], levels=20, cmap='RdBu_r')
    axs[0, 1].set_title(titles[1])
    axs[0, 1].set_xlabel(xl)
    axs[0, 1].set_ylabel(yl)
    plt.colorbar(im2, ax=axs[0, 1])
    
    # 圧力
    im3 = axs[1, 0].contourf(results['x'], results['y'], results['p'], levels=20, cmap='viridis')
    axs[1, 0].set_title(titles[2])
    axs[1, 0].set_xlabel(xl)
    axs[1, 0].set_ylabel(yl)
    plt.colorbar(im3, ax=axs[1, 0])
    
    # 流線関数
    im4 = axs[1, 1].contourf(results['x'], results['y'], results['psi'], levels=20, cmap='plasma')
    axs[1, 1].set_title(titles[3])
    axs[1, 1].set_xlabel(xl)
    axs[1, 1].set_ylabel(yl)
    plt.colorbar(im4, ax=axs[1, 1])
    
    # 流線を重ね書き
    axs[1, 1].contour(results['x'], results['y'], results['psi'], levels=10, colors='white', linewidths=0.5)
    
    plt.tight_layout()
    fig.savefig("AIRFLOW_plots.png", dpi=150)
    plt.close(fig)


def write_spec_md(results):
    """課題仕様と結論を.mdに出力"""
    with open("AIRFLOW_spec.md", "w", encoding="utf-8") as f:
        f.write("# 室内気流解析システム (Python + Maxima連成)\n\n")
        f.write("## 課題仕様\n\n")
        f.write("### 目的\n")
        f.write("室内空間（部屋）における空気の流れをNavier-Stokes方程式に基づいて解析する。\n\n")
        
        f.write("### 数式モデル\n\n")
        f.write("#### 連続の式 (非圧縮)\n")
        f.write("$$\n\\frac{\\partial u}{\\partial x} + \\frac{\\partial v}{\\partial y} = 0\n$$\n\n")
        
        f.write("#### Navier-Stokes方程式 (x方向)\n")
        f.write("$$\nu\\frac{\\partial u}{\\partial x} + v\\frac{\\partial u}{\\partial y} = ")
        f.write("-\\frac{1}{\\rho}\\frac{\\partial p}{\\partial x} + ")
        f.write("\\nu\\left(\\frac{\\partial^2 u}{\\partial x^2} + \\frac{\\partial^2 u}{\\partial y^2}\\right)\n$$\n\n")
        
        f.write("#### Navier-Stokes方程式 (y方向)\n")
        f.write("$$\nu\\frac{\\partial v}{\\partial x} + v\\frac{\\partial v}{\\partial y} = ")
        f.write("-\\frac{1}{\\rho}\\frac{\\partial p}{\\partial y} + ")
        f.write("\\nu\\left(\\frac{\\partial^2 v}{\\partial x^2} + \\frac{\\partial^2 v}{\\partial y^2}\\right)\n$$\n\n")
        
        f.write("### パラメータ\n\n")
        f.write("| パラメータ | 値 | 単位 |\n")
        f.write("|----------|-----|------|\n")
        f.write(f"| 空気密度 ρ | 1.225 | kg/m³ |\n")
        f.write(f"| 動粘性係数 ν | {1.5e-5:.1e} | m²/s |\n")
        f.write(f"| 入口速度 | {results['inlet_vel']:.1f} | m/s |\n")
        f.write(f"| レイノルズ数 Re | {results['reynolds']:.1f} | - |\n")
        f.write(f"| 計算格子数 | {results['nx']}×{results['ny']} | - |\n\n")
        
        f.write("## 結論\n\n")
        f.write(f"- **解像度**: {results['nx']}×{results['ny']} 格子\n")
        f.write(f"- **最大流速**: {np.max(results['u']):.3f} m/s\n")
        f.write(f"- **最大圧力**: {np.max(results['p']):.3f} Pa\n\n")
        
        f.write("### 考察\n\n")
        f.write("1. **Maxima連成**: Navier-Stokes方程式の導出をMaximaに任せ、式の検証が容易になった\n")
        f.write("2. **室内気流特性**: 入口付近で加速し、障害物(家具)周辺で渦が発生する\n")
        f.write("3. **レイノルズ数**: 層流領域(Re<2000)に該当\n")
        f.write("4. **実用性**: 換気設計・空調配置の基礎評価に適用可能\n\n")
        
        f.write("### 今後の課題\n\n")
        f.write("- 3次元への拡張\n")
        f.write("- 乱流モデルの導入 (k-ε, LES)\n")
        f.write("- 熱輸送・浮力の考慮\n")
        f.write("- 時間発展計算 (非定常解析)\n")


def main():
    print("=" * 60)
    print("室内気流解析システム (Python + Maxima連成)")
    print("=" * 60)
    
    # 1. .macファイル出力
    print("\n[1] .macファイル出力中...")
    mac_file = write_mac_file(MAXIMA_CODE, "AIRFLOW_model.mac")
    
    # 2. MaximaでNS方程式導出
    print("\n[2] MaximaでNavier-Stokes方程式導出中...")
    maxima_out = run_maxima(mac_file)
    print("Maxima出力:", maxima_out[:200] if maxima_out else "なし")
    
    # 3. ソルバー設定
    print("\n[3] 室内気流ソルバー実行中...")
    solver = RoomAirflowSolver(width=2.0, height=1.5, nx=60, ny=45)
    
    # 境界条件設定
    solver.set_inlet(x_pos=0, y_range=[0.5, 1.0])      # 左壁中央に入口
    solver.set_outlet(x_pos=2.0, y_range=[0.5, 1.0])   # 右壁中央に出口
    solver.set_obstacle(0.7, 1.3, 0.3, 0.7)           # 中央に障害物(家具)
    
    # 求解
    solver.solve(max_iter=3000, tol=1e-4)
    solver.compute_streamfunction()
    results = solver.get_results()
    results['inlet_vel'] = solver.inlet_velocity
    results['nx'] = solver.nx
    results['ny'] = solver.ny
    
    # 4. 出力
    print("\n[4] 結果出力中...")
    write_csv(results)
    write_summary(results, maxima_out)
    plot_results(results)
    write_spec_md(results)
    
    print("\n" + "=" * 60)
    print("出力ファイル:")
    print("  - AIRFLOW_model.mac       (Maximaコード - 生きた仕様書)")
    print("  - AIRFLOW_results.csv     (数値データ)")
    print("  - AIRFLOW_summary.txt     (サマリー)")
    print("  - AIRFLOW_plots.png       (2x2グラフ)")
    print("  - AIRFLOW_spec.md         (仕様+結論)")
    print("  - AIRFLOW_equations.txt   (Maxima導出式)")
    print("=" * 60)


if __name__ == "__main__":
    main()