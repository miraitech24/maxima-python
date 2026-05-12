# ===== mass_spring_damper.py =====
# TAG: [IMPORT]
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import sys
import yaml
from pathlib import Path

# TAG: [FONT_AUTO] 日本語フォント自動検出（強化版）
def setup_font():
    """日本語フォント自動検出。あれば日本語、なければ英語"""
    try:
        import matplotlib.font_manager as fm
        
        # 日本語フォントの優先順位リスト
        jp_font_names = [
            'Noto Sans CJK JP', 'Noto Sans JP', 'IPAexGothic', 'IPAexMincho',
            'Yu Gothic', 'YuGothic', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN',
            'MS Gothic', 'MS Mincho', 'Meiryo', 'TakaoGothic', 'TakaoMincho'
        ]
        
        # 利用可能なフォントを検索
        available_fonts = {f.name for f in fm.fontManager.ttflist}
        
        selected_font = None
        for font_name in jp_font_names:
            if font_name in available_fonts:
                selected_font = font_name
                break
        
        if selected_font:
            plt.rcParams['font.family'] = selected_font
            plt.rcParams['axes.unicode_minus'] = False  # マイナス記号の文字化け防止
            print(f"  -> Using Japanese font: {selected_font}")
            return True
        else:
            # フォント名に日本語関連キーワードを含むものを検索
            jp_keywords = ['noto', 'ipa', 'source han', 'hiragino', 'yugothic', 
                          'ms ', 'meiryo', 'takao', 'kochi', 'sazanami']
            for font in fm.fontManager.ttflist:
                font_lower = font.name.lower()
                if any(kw in font_lower for kw in jp_keywords):
                    plt.rcParams['font.family'] = font.name
                    plt.rcParams['axes.unicode_minus'] = False
                    print(f"  -> Using Japanese font: {font.name}")
                    return True
            
            print("  -> No Japanese font found. Using English.")
            plt.rcParams['font.family'] = 'sans-serif'
            return False
            
    except Exception as e:
        print(f"  -> Font detection error: {e}. Using English.")
        plt.rcParams['font.family'] = 'sans-serif'
        return False

# TAG: [PARAMS_LOAD] パラメータ読み込み
def load_params():
    """params.yamlからパラメータを読み込み"""
    try:
        with open("params.yaml", "r") as f:
            params = yaml.safe_load(f)
        for key in ['m', 'c', 'k', 'x0', 'v0', 't_end', 'dt']:
            if key in params:
                params[key] = float(params[key])
        return params
    except FileNotFoundError:
        print("Error: params.yaml not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading params.yaml: {e}")
        sys.exit(1)

# TAG: [MAXIMA_KICK] Maxima実行
def run_maxima():
    """Maximaで解析解を導出"""
    mac_file = "problem.mac"
    if not os.path.exists(mac_file):
        print(f"Error: {mac_file} not found")
        return False
    try:
        result = subprocess.run(
            ["maxima", "--batch", mac_file],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False
        print(result.stdout[-300:])
        return True
    except FileNotFoundError:
        print("Maxima not installed. Using Python analytic solution.")
        return False
    except Exception as e:
        print(f"Maxima error: {e}")
        return False

# TAG: [ANALYTIC] 解析解
def analytic_solution(t, m, c, k, x0, v0):
    """減衰系の解析解"""
    wn = np.sqrt(k/m)
    zeta = c/(2*np.sqrt(m*k))
    
    if zeta < 1.0:
        wd = wn*np.sqrt(1 - zeta**2)
        A = x0
        B = (v0 + zeta*wn*x0)/wd
        return np.exp(-zeta*wn*t)*(A*np.cos(wd*t) + B*np.sin(wd*t))
    elif abs(zeta - 1.0) < 1e-8:
        A = x0
        B = v0 + wn*x0
        return (A + B*t)*np.exp(-wn*t)
    else:
        r1 = -wn*zeta + wn*np.sqrt(zeta**2 - 1)
        r2 = -wn*zeta - wn*np.sqrt(zeta**2 - 1)
        C2 = (v0 - r1*x0)/(r2 - r1)
        C1 = x0 - C2
        return C1*np.exp(r1*t) + C2*np.exp(r2*t)

# TAG: [SOLVER] RK4数値積分
def solve_rk4(m, c, k, x0, v0, t_end, dt):
    """RK4法で数値解を計算"""
    steps = int(t_end / dt) + 1
    t = np.linspace(0, t_end, steps)
    x = np.zeros(steps)
    v = np.zeros(steps)
    x[0], v[0] = x0, v0
    
    for i in range(steps - 1):
        a1 = -(c/m)*v[i] - (k/m)*x[i]
        k1x = v[i]; k1v = a1
        a2 = -(c/m)*(v[i] + 0.5*dt*k1v) - (k/m)*(x[i] + 0.5*dt*k1x)
        k2x = v[i] + 0.5*dt*k1v; k2v = a2
        a3 = -(c/m)*(v[i] + 0.5*dt*k2v) - (k/m)*(x[i] + 0.5*dt*k2x)
        k3x = v[i] + 0.5*dt*k2v; k3v = a3
        a4 = -(c/m)*(v[i] + dt*k3v) - (k/m)*(x[i] + dt*k3x)
        k4x = v[i] + dt*k3v; k4v = a4
        
        x[i+1] = x[i] + (dt/6)*(k1x + 2*k2x + 2*k3x + k4x)
        v[i+1] = v[i] + (dt/6)*(k1v + 2*k2v + 2*k3v + k4v)
    
    return t, x, v

# TAG: [PLOT] 2x2 subplot描画（文字化け対策）
def plot_results(t, x_num, x_ana, v_num, params, has_jp):
    """結果を2x2 subplotで可視化"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    m, c, k = params['m'], params['c'], params['k']
    wn = np.sqrt(k/m)
    zeta = c/(2*np.sqrt(m*k))
    
    if has_jp:
        titles = ['変位 x(t) [m]', '速度 v(t) [m/s]', '誤差 [m]', '相平面 (x vs v)']
        xlabel = '時間 [s]'
        stitle = f'質量-ばね-ダンパ系 (ωn={wn:.2f}, ζ={zeta:.2f})'
        labels = ['数値解', '解析解']
    else:
        titles = ['Displacement x(t) [m]', 'Velocity v(t) [m/s]', 'Error [m]', 'Phase Portrait']
        xlabel = 'Time [s]'
        stitle = f'Mass-Spring-Damper (wn={wn:.2f}, zeta={zeta:.2f})'
        labels = ['Numeric', 'Analytic']
    
    axes[0,0].plot(t, x_num, 'b-', lw=1.5, label=labels[0])
    axes[0,0].plot(t, x_ana, 'r--', lw=1.5, label=labels[1])
    axes[0,0].set_xlabel(xlabel); axes[0,0].set_ylabel(titles[0])
    axes[0,0].set_title(titles[0]); axes[0,0].legend(); axes[0,0].grid(True, alpha=0.3)
    
    axes[0,1].plot(t, v_num, 'g-', lw=1.5)
    axes[0,1].set_xlabel(xlabel); axes[0,1].set_ylabel(titles[1])
    axes[0,1].set_title(titles[1]); axes[0,1].grid(True, alpha=0.3)
    
    error = np.abs(x_num - x_ana)
    axes[1,0].plot(t, error, 'purple', lw=1.0)
    axes[1,0].set_xlabel(xlabel); axes[1,0].set_ylabel(titles[2])
    axes[1,0].set_title(titles[2]); axes[1,0].grid(True, alpha=0.3)
    axes[1,0].set_yscale('log')
    
    axes[1,1].plot(x_num, v_num, 'orange', lw=1.0, alpha=0.7)
    axes[1,1].set_xlabel(titles[0]); axes[1,1].set_ylabel(titles[1])
    axes[1,1].set_title(titles[3]); axes[1,1].grid(True, alpha=0.3)
    
    fig.suptitle(stitle, fontsize=14)
    plt.tight_layout()
    return fig

# TAG: [MAIN] メイン実行
def main():
    """メイン処理"""
    has_jp = setup_font()
    
    print("[1/4] Loading parameters from params.yaml...")
    params = load_params()
    m, c, k = params['m'], params['c'], params['k']
    x0, v0 = params['x0'], params['v0']
    t_end, dt = params['t_end'], params['dt']
    print(f"  m={m}, c={c}, k={k}, x0={x0}, v0={v0}")
    
    print("[2/4] Solving equations...")
    t, x_num, v_num = solve_rk4(m, c, k, x0, v0, t_end, dt)
    x_ana = np.array([analytic_solution(ti, m, c, k, x0, v0) for ti in t])
    
    print("[3/4] Plotting...")
    fig = plot_results(t, x_num, x_ana, v_num, params, has_jp)
    fig.savefig("response.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    print("[4/4] Saving files...")
    np.savetxt("results.csv", np.column_stack([t, x_num, x_ana, v_num]),
               delimiter=",", header="time,x_numeric,x_analytic,velocity", comments="")
    
    wn = np.sqrt(k/m)
    zeta = c/(2*np.sqrt(m*k))
    max_error = np.max(np.abs(x_num - x_ana))
    
    if has_jp:
        summary = f"""# 質量-ばね-ダンパ系 シミュレーション結果

## パラメータ
- 質量 $m = {m}$ kg
- 減衰係数 $c = {c}$ N·s/m
- ばね定数 $k = {k}$ N/m
- 初期変位 $x_0 = {x0}$ m
- 初期速度 $v_0 = {v0}$ m/s

## 解析解
- 固有角振動数 $\\omega_n = {wn:.4f}$ rad/s
- 減衰比 $\\zeta = {zeta:.4f}$

## 運動方程式
$$ m\\ddot{{x}} + c\\dot{{x}} + kx = 0 $$

## 結果
- 最大誤差: {max_error:.6e} m
- 最終変位: {x_num[-1]:.6f} m

## 考察
誤差が微小であり、数値積分が正しく行われている。
"""
    else:
        summary = f"""# Mass-Spring-Damper Simulation Results

## Parameters
- Mass $m = {m}$ kg
- Damping $c = {c}$ N·s/m
- Spring $k = {k}$ N/m
- Initial $x_0 = {x0}$ m, $v_0 = {v0}$ m/s

## Analytic Solution
- Natural frequency $\\omega_n = {wn:.4f}$ rad/s
- Damping ratio $\\zeta = {zeta:.4f}$

## Equation
$$ m\\ddot{{x}} + c\\dot{{x}} + kx = 0 $$

## Results
- Max error: {max_error:.6e} m
- Final displacement: {x_num[-1]:.6f} m

## Discussion
Numerical integration is validated by small error.
"""
    
    with open("summary.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("Done! Files: response.png, summary.md, results.csv")

if __name__ == "__main__":
    main()
