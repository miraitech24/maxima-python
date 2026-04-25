#!/bin/bash
# VF004_integrated_fixed.sh
# 統合実行スクリプト（修正版）

echo "========================================="
echo "VF-004: 連成システム解析 統合実行"
echo "========================================="

# 出力ディレクトリの作成
mkdir -p results
mkdir -p plots

# 1. Maxima解析計算の実行（存在する場合）
echo "1. Maxima解析計算を実行中..."
if [ -f "VF004_analytical.mac" ]; then
    maxima -b VF004_analytical.mac > maxima_output.log 2>&1
    
    if [ $? -eq 0 ]; then
        echo "   Maxima実行完了"
        # 生成されたファイルをチェック
        if [ -f "VF004_analytical_data.csv" ]; then
            echo "   Maximaデータファイルを検出: VF004_analytical_data.csv"
            mv VF004_analytical_data.csv results/ 2>/dev/null
        else
            echo "   警告: VF004_analytical_data.csvが生成されていません"
        fi
    else
        echo "   Maxima実行中にエラーが発生しました"
        cat maxima_output.log | tail -20
    fi
else
    echo "   Maximaファイルが見つかりません（スキップ）"
fi

# 2. Python数値計算の実行
echo "2. Python数値計算を実行中..."
if [ -f "VF004_fixed_fonts.py" ]; then
    python3 VF004_fixed_fonts.py > python_output.log 2>&1
elif [ -f "VF004_numerical.py" ]; then
    python3 VF004_numerical.py > python_output.log 2>&1
else
    echo "   Pythonファイルが見つかりません"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo "   Python実行完了"
    # 生成されたファイルをチェックして移動
    for file in VF004_*.csv VF004_*.json VF004_*.png; do
        if [ -f "$file" ]; then
            echo "   移動: $file"
            mv "$file" results/ 2>/dev/null || mv "$file" plots/ 2>/dev/null
        fi
    done
else
    echo "   Python実行中にエラーが発生しました"
    cat python_output.log | tail -20
    exit 1
fi

# 3. 結果の統合（必要なファイルがあれば）
echo "3. 結果を統合中..."

if [ -f "results/VF004_analytical_data.csv" ] && [ -f "results/VF004_basic_results.csv" ]; then
    echo "   統合解析を実行..."
    
    python3 -c "
import pandas as pd
import numpy as np
from scipy import interpolate
import os
import json

print('統合解析開始...')

# データ読み込み
maxima_path = 'results/VF004_analytical_data.csv'
python_path = 'results/VF004_basic_results.csv'

if os.path.exists(maxima_path) and os.path.exists(python_path):
    maxima_df = pd.read_csv(maxima_path)
    python_df = pd.read_csv(python_path)
    
    print(f'Maximaデータ: {len(maxima_df)} 行')
    print(f'Pythonデータ: {len(python_df)} 行')
    
    # 共通の時間軸で補間
    t_min = max(maxima_df['t'].min(), python_df['t'].min())
    t_max = min(maxima_df['t'].max(), python_df['t'].max())
    
    if t_min < t_max:
        t_common = np.linspace(t_min, t_max, 500)
        
        # Maximaデータ補間
        if 'A_analytical' in maxima_df.columns:
            f_A_analytical = interpolate.interp1d(maxima_df['t'], maxima_df['A_analytical'], 
                                                 bounds_error=False, fill_value='extrapolate')
            A_analytical_interp = f_A_analytical(t_common)
        else:
            A_analytical_interp = np.zeros_like(t_common)
            
        if 'B_analytical' in maxima_df.columns:
            f_B_analytical = interpolate.interp1d(maxima_df['t'], maxima_df['B_analytical'],
                                                 bounds_error=False, fill_value='extrapolate')
            B_analytical_interp = f_B_analytical(t_common)
        else:
            B_analytical_interp = np.zeros_like(t_common)
        
        # Pythonデータ補間
        f_A_numerical = interpolate.interp1d(python_df['t'], python_df['A'],
                                            bounds_error=False, fill_value='extrapolate')
        f_B_numerical = interpolate.interp1d(python_df['t'], python_df['B'],
                                            bounds_error=False, fill_value='extrapolate')
        
        A_numerical_interp = f_A_numerical(t_common)
        B_numerical_interp = f_B_numerical(t_common)
        
        # 誤差計算
        error_A = np.abs(A_analytical_interp - A_numerical_interp)
        error_B = np.abs(B_analytical_interp - B_numerical_interp)
        
        # 結果をDataFrameに保存
        result_df = pd.DataFrame({
            't': t_common,
            'A_analytical': A_analytical_interp,
            'B_analytical': B_analytical_interp,
            'A_numerical': A_numerical_interp,
            'B_numerical': B_numerical_interp,
            'error_A': error_A,
            'error_B': error_B
        })
        
        result_df.to_csv('results/VF004_integrated_results.csv', index=False)
        
        # 統計情報を計算
        stats = {
            'mean_error_A': float(error_A.mean()),
            'mean_error_B': float(error_B.mean()),
            'max_error_A': float(error_A.max()),
            'max_error_B': float(error_B.max()),
            'correlation_A': float(np.corrcoef(A_analytical_interp, A_numerical_interp)[0,1]),
            'correlation_B': float(np.corrcoef(B_analytical_interp, B_numerical_interp)[0,1]),
            'integration_date': pd.Timestamp.now().isoformat()
        }
        
        with open('results/VF004_integration_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print('統合完了！')
        print(f'平均誤差 A: {stats[\"mean_error_A\"]:.6e}')
        print(f'平均誤差 B: {stats[\"mean_error_B\"]:.6e}')
        print(f'最大誤差 A: {stats[\"max_error_A\"]:.6e}')
        print(f'最大誤差 B: {stats[\"max_error_B\"]:.6e}')
        print(f'相関係数 A: {stats[\"correlation_A\"]:.6f}')
        print(f'相関係数 B: {stats[\"correlation_B\"]:.6f}')
        
        # 比較プロット
        import matplotlib
        matplotlib.use('Agg')  # GUIバックエンドを使用しない
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        
        # システムAの比較
        plt.subplot(2, 2, 1)
        plt.plot(t_common, A_analytical_interp, 'b-', label='Maxima (Analytical)', linewidth=2)
        plt.plot(t_common, A_numerical_interp, 'r--', label='Python (Numerical)', linewidth=2, alpha=0.7)
        plt.xlabel('Time')
        plt.ylabel('System A')
        plt.title('System A: Analytical vs Numerical')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # システムBの比較
        plt.subplot(2, 2, 2)
        plt.plot(t_common, B_analytical_interp, 'b-', label='Maxima (Analytical)', linewidth=2)
        plt.plot(t_common, B_numerical_interp, 'r--', label='Python (Numerical)', linewidth=2, alpha=0.7)
        plt.xlabel('Time')
        plt.ylabel('System B')
        plt.title('System B: Analytical vs Numerical')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 誤差プロット
        plt.subplot(2, 2, 3)
        plt.semilogy(t_common, error_A, 'g-', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Error (log scale)')
        plt.title('Error in System A')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 4)
        plt.semilogy(t_common, error_B, 'g-', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel('Error (log scale)')
        plt.title('Error in System B')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('plots/VF004_integrated_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print('比較プロットを保存: plots/VF004_integrated_comparison.png')
    else:
        print('警告: 時間軸が重なっていません')
        print(f'Maxima時間範囲: {maxima_df[\"t\"].min()} - {maxima_df[\"t\"].max()}')
        print(f'Python時間範囲: {python_df[\"t\"].min()} - {python_df[\"t\"].max()}')
else:
    print('必要なデータファイルが見つかりません')
    print(f'Maximaファイル: {os.path.exists(maxima_path)}')
    print(f'Pythonファイル: {os.path.exists(python_path)}')
" > integration_output.log 2>&1
    
    echo "   統合完了"
else
    echo "   統合スキップ: 必要なデータファイルが不足しています"
    echo "   必要なファイル:"
    echo "     - results/VF004_analytical_data.csv (Maxima出力)"
    echo "     - results/VF004_basic_results.csv (Python出力)"
    echo "   現在のファイル:"
    ls -la results/*.csv 2>/dev/null || echo "     (CSVファイルなし)"
fi

# 4. 結果レポート生成
echo "4. 結果レポート生成中..."

python3 -c "
import json
import pandas as pd
import os
from datetime import datetime

print('レポート生成開始...')

# 結果ディレクトリのファイルを確認
result_files = {}
for root, dirs, files in os.walk('results'):
    for file in files:
        result_files[file] = os.path.join(root, file)

for root, dirs, files in os.walk('plots'):
    for file in files:
        result_files[file] = os.path.join(root, file)

print(f'検出されたファイル数: {len(result_files)}')

# レポートHTML生成
html_report = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VF-004 解析レポート</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .result-box {
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 10px 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .file-list {
            background-color: #fff;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin: 10px 0;
        }
        .plot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .status-success {
            color: #27ae60;
            font-weight: bold;
        }
        .status-warning {
            color: #f39c12;
            font-weight: bold;
        }
        .status-error {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>VF-004: 連成システム解析レポート</h1>
        <p>生成日時: ''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
    </div>
'''

# システム情報
if 'VF004_system_info.json' in result_files:
    try:
        with open(result_files['VF004_system_info.json'], 'r') as f:
            system_info = json.load(f)
        
        html_report += '''
    <div class="section">
        <h2>1. システムパラメータ</h2>
        <table>
            <tr><th>パラメータ</th><th>値</th><th>説明</th></tr>
            <tr><td>α (alpha)</td><td>{:.4f}</td><td>成長率係数</td></tr>
            <tr><td>β (beta)</td><td>{:.4f}</td><td>減衰率係数</td></tr>
            <tr><td>γ (gamma)</td><td>{:.4f}</td><td>結合係数</td></tr>
            <tr><td>δ (delta)</td><td>{:.4f}</td><td>外部擾乱係数</td></tr>
            <tr><td>初期値 A</td><td>{:.2f}</td><td>システムAの初期値</td></tr>
            <tr><td>初期値 B</td><td>{:.2f}</td><td>システムBの初期値</td></tr>
            <tr><td>シミュレーション時間</td><td>{:.1f}</td><td>終了時間</td></tr>
        </table>
    </div>
'''.format(
    system_info.get('alpha', 0),
    system_info.get('beta', 0),
    system_info.get('gamma', 0),
    system_info.get('delta', 0),
    system_info.get('A0', 0),
    system_info.get('B0', 0),
    system_info.get('t_end', 0)
)
    except:
        html_report += '''
    <div class="section">
        <h2>1. システムパラメータ</h2>
        <p class="status-warning">システム情報を読み込めませんでした</p>
    </div>
'''

# 統計情報
if 'VF004_statistics.json' in result_files:
    try:
        with open(result_files['VF004_statistics.json'], 'r') as f:
            stats = json.load(f)
        
        html_report += '''
    <div class="section">
        <h2>2. シミュレーション統計</h2>
        <div class="result-box">
            <h3>数値計算結果</h3>
            <table>
                <tr><th>指標</th><th>システム A</th><th>システム B</th></tr>
                <tr><td>最終値</td><td>{:.4e}</td><td>{:.4e}</td></tr>
                <tr><td>最大値</td><td>{:.4e}</td><td>{:.4e}</td></tr>
                <tr><td>積分値 (面積)</td><td>{:.4e}</td><td>{:.4e}</td></tr>
            </table>
        </div>
    </div>
'''.format(
    stats.get('A_final', 0),
    stats.get('B_final', 0),
    stats.get('A_max', 0),
    stats.get('B_max', 0),
    stats.get('A_area', 0),
    stats.get('B_area', 0)
)
    except:
        pass

# 統合結果
if 'VF004_integration_stats.json' in result_files:
    try:
        with open(result_files['VF004_integration_stats.json'], 'r') as f:
            int_stats = json.load(f)
        
        html_report += '''
    <div class="section">
        <h2>3. 解析解と数値解の比較</h2>
        <div class="result-box">
            <h3>誤差統計</h3>
            <table>
                <tr><th>指標</th><th>システム A</th><th>システム B</th></tr>
                <tr><td>平均誤差</td><td>{:.4e}</td><td>{:.4e}</td></tr>
                <tr><td>最大誤差</td><td>{:.4e}</td><td>{:.4e}</td></tr>
                <tr><td>相関係数</td><td>{:.6f}</td><td>{:.6f}</td></tr>
            </table>
        </div>
'''
        if 'VF004_integrated_comparison.png' in result_files:
            html_report += '''
        <div class="plot-grid">
            <div>
                <h4>比較プロット</h4>
                <img src="../plots/VF004_integrated_comparison.png" alt="比較プロット">
            </div>
        </div>
'''
        html_report += '''
    </div>
'''.format(
    int_stats.get('mean_error_A', 0),
    int_stats.get('mean_error_B', 0),
    int_stats.get('max_error_A', 0),
    int_stats.get('max_error_B', 0),
    int_stats.get('correlation_A', 0),
    int_stats.get('correlation_B', 0)
)
    except:
        pass

# プロット画像
html_report += '''
    <div class="section">
        <h2>4. 可視化結果</h2>
        <div class="plot-grid">
'''

plot_files = [f for f in result_files.keys() if f.endswith('.png')]
for plot_file in plot_files:
    if plot_file != 'VF004_integrated_comparison.png':  # すでに表示済み
        rel_path = os.path.relpath(result_files[plot_file], '.')
        html_report += '''
            <div>
                <h4>{}</h4>
                <img src="{}" alt="{}">
            </div>
'''.format(plot_file.replace('_', ' ').replace('.png', ''), rel_path, plot_file)

html_report += '''
        </div>
    </div>
'''

# ファイル一覧
html_report += '''
    <div class="section">
        <h2>5. 生成ファイル一覧</h2>
        <div class="file-list">
            <h3>データファイル (results/)</h3>
            <ul>
'''

data_files = [f for f in result_files.keys() if f.endswith(('.csv', '.json'))]
for data_file in sorted(data_files):
    file_path = result_files[data_file]
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    html_report += '''
                <li>{} ({:.1f} KB)</li>
'''.format(data_file, file_size / 1024)

html_report += '''
            </ul>
            <h3>画像ファイル (plots/)</h3>
            <ul>
'''

for plot_file in sorted(plot_files):
    file_path = result_files[plot_file]
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    html_report += '''
                <li>{} ({:.1f} KB)</li>
'''.format(plot_file, file_size / 1024)

html_report += '''
            </ul>
        </div>
    </div>
</body>
</html>
'''

# レポート保存
with open('VF004_report.html', 'w', encoding='utf-8') as f:
    f.write(html_report)

print('レポート生成完了: VF004_report.html')
"

# 5. 最終メッセージ
echo ""
echo "========================================="
echo "VF-004 統合実行完了!"
echo "========================================="
echo ""
echo "結果ディレクトリ:"
echo "  results/ - データファイル (CSV, JSON)"
echo "  plots/   - 画像ファイル (PNG)"
echo ""
echo "メインレポート:"
echo "  VF004_report.html - Webブラウザで開けます"
echo ""
echo "ログファイル:"
echo "  maxima_output.log    - Maxima実行ログ"
echo "  python_output.log    - Python実行ログ"
echo "  integration_output.log - 統合処理ログ"
echo ""
echo "実行時間: $(date)"

