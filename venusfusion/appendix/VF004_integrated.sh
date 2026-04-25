#!/bin/bash
# VF004_integrated.sh
# MaximaとPythonの連成実行スクリプト

echo "========================================="
echo "VF-004: 連成システム解析 統合実行"
echo "========================================="

# 1. Maxima解析計算の実行
echo "1. Maxima解析計算を実行中..."
maxima -b VF004_analytical.mac > maxima_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "   Maxima実行完了"
else
    echo "   Maxima実行中にエラーが発生しました"
    cat maxima_output.log | tail -20
    exit 1
fi

# 2. Python数値計算・最適化の実行
echo "2. Python数値計算・最適化を実行中..."
python3 VF004_numerical.py > python_output.log 2>&1

if [ $? -eq 0 ]; then
    echo "   Python実行完了"
else
    echo "   Python実行中にエラーが発生しました"
    cat python_output.log | tail -20
    exit 1
fi

# 3. 結果の統合
echo "3. 結果を統合中..."

# MaximaとPythonの結果を結合
if [ -f "VF004_analytical_data.csv" ] && [ -f "VF004_numerical_results.csv" ]; then
    python3 -c "
import pandas as pd
import numpy as np

# データ読み込み
maxima_df = pd.read_csv('VF004_analytical_data.csv')
python_df = pd.read_csv('VF004_numerical_results.csv')

# 共通の時間軸で補間
t_min = max(maxima_df['t'].min(), python_df['t'].min())
t_max = min(maxima_df['t'].max(), python_df['t'].max())
t_common = np.linspace(t_min, t_max, 500)

# 補間
from scipy import interpolate

# Maximaデータ補間
f_A_analytical = interpolate.interp1d(maxima_df['t'], maxima_df['A_analytical'])
f_B_analytical = interpolate.interp1d(maxima_df['t'], maxima_df['B_analytical'])

# Pythonデータ補間
f_A_rk45 = interpolate.interp1d(python_df['t'], python_df['A_rk45'])
f_B_rk45 = interpolate.interp1d(python_df['t'], python_df['B_rk45'])

# 補間値を計算
A_analytical_interp = f_A_analytical(t_common)
B_analytical_interp = f_B_analytical(t_common)
A_rk45_interp = f_A_rk45(t_common)
B_rk45_interp = f_B_rk45(t_common)

# 誤差計算
error_A = np.abs(A_analytical_interp - A_rk45_interp)
error_B = np.abs(B_analytical_interp - B_rk45_interp)

# 結果をDataFrameに保存
result_df = pd.DataFrame({
    't': t_common,
    'A_analytical': A_analytical_interp,
    'B_analytical': B_analytical_interp,
    'A_numerical': A_rk45_interp,
    'B_numerical': B_rk45_interp,
    'error_A': error_A,
    'error_B': error_B
})

result_df.to_csv('VF004_integrated_results.csv', index=False)

# 統計情報を計算
print('統合解析結果:')
print(f'平均誤差 A: {error_A.mean():.6e}')
print(f'平均誤差 B: {error_B.mean():.6e}')
print(f'最大誤差 A: {error_A.max():.6e}')
print(f'最大誤差 B: {error_B.max():.6e}')
print(f'相関係数 A: {np.corrcoef(A_analytical_interp, A_rk45_interp)[0,1]:.6f}')
print(f'相関係数 B: {np.corrcoef(B_analytical_interp, B_rk45_interp)[0,1]:.6f}')
" > integration_output.log 2>&1

    echo "   統合完了: VF004_integrated_results.csv を作成"
else
    echo "   統合エラー: 必要なデータファイルが見つかりません"
fi

# 4. 最終レポート生成
echo "4. 最終レポート生成中..."

python3 -c "
import pandas as pd
import json
from datetime import datetime

# データ読み込み
try:
    integrated_df = pd.read_csv('VF004_integrated_results.csv')
    with open('VF004_optimization_results.json', 'r') as f:
        opt_results = json.load(f)
    with open('VF004_system_info.json', 'r') as f:
        system_info = json.load(f)
    
    # HTMLレポート生成
    html_report = f'''
<!DOCTYPE html>
<html>
<head>
    <title>VF-004 解析レポート</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; }}
        .section {{ margin: 30px 0; padding: 20px; border: 1px solid #ddd; }}
        .result {{ background-color: #f9f9f9; padding: 15px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body>
    <div class=\"header\">
        <h1>VF-004: 連成システム解析レポート</h1>
        <p>生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class=\"section\">
        <h2>1. システムパラメータ</h2>
        <table>
            <tr><th>パラメータ</th><th>値</th></tr>
            <tr><td>α (成長率係数)</td><td>{system_info.get('alpha', 'N/A')}</td></tr>
            <tr><td>β (減衰率係数)</td><td>{system_info.get('beta', 'N/A')}</td></tr>
            <tr><td>γ (結合係数)</td><td>{system_info.get('gamma', 'N/A')}</td></tr>
            <tr><td>δ (外部擾乱係数)</td><td>{system_info.get('delta', 'N/A')}</td></tr>
            <tr><td>初期値 A</td><td>{system_info.get('A0', 'N/A')}</td></tr>
            <tr><td>初期値 B</td><td>{system_info.get('B0', 'N/A')}</td></tr>
        </table>
    </div>
    
    <div class=\"section\">
        <h2>2. 数値解析結果</h2>
        <div class=\"result\">
            <p>平均誤差: A = {integrated_df['error_A'].mean():.6e}, B = {integrated_df['error_B'].mean():.6e}</p>
            <p>最大誤差: A = {integrated_df['error_A'].max():.6e}, B = {integrated_df['error_B'].max():.6e}</p>
        </div>
        <img src=\"VF004_comparison.png\" alt=\"比較プロット\">
    </div>
    
    <div class=\"section\">
        <h2>3. 最適化結果</h2>
        <div class=\"result\">
            <p>最適値: {opt_results.get('optimal_value', 'N/A')}</p>
            <p>最適パラメータ: {opt_results.get('optimal_params', 'N/A')}</p>
        </div>
        <img src=\"VF004_timeseries.png\" alt=\"時系列プロット\">
    </div>
    
    <div class=\"section\">
        <h2>4. 生成ファイル一覧</h2>
        <ul>
            <li>VF004_analytical_data.csv - Maxima解析結果</li>
            <li>VF004_numerical_results.csv - Python数値結果</li>
            <li>VF004_integrated_results.csv - 統合結果</li>
            <li>VF004_optimization_results.json - 最適化結果</li>
            <li>VF004_system_info.json - システム情報</li>
            <li>VF004_*.png - 可視化画像</li>
        </ul>
    </div>
</body>
</html>
'''
    
    with open('VF004_report.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print('HTMLレポートを生成しました: VF004_report.html')
    
except Exception as e:
    print(f'レポート生成エラー: {e}')
"

echo "========================================="
echo "VF-004 統合実行完了!"
echo "========================================="
echo ""
echo "生成されたファイル:"
echo "- VF004_report.html (総合レポート)"
echo "- VF004_integrated_results.csv (統合結果)"
echo "- 各種PNG画像 (解析結果)"
echo ""
echo "Maxima出力: maxima_output.log"
echo "Python出力: python_output.log"

