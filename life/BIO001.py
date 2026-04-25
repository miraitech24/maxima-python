#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 13:13:59 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-001: 微生物宇宙普遍性確率 計算（文字化け修正版）
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json
from datetime import datetime

# 文字化け解決済み環境の設定を適用
# 以下のいずれかの方法で日本語フォントを設定

# 方法1: フォントマネージャーを使用
import matplotlib.font_manager as fm
import matplotlib

# 利用可能な日本語フォントを探す
def setup_japanese_font():
    """日本語フォントの設定"""
    try:
        # IPAexゴシック（一般的な日本語フォント）
        font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            font_name = fm.FontProperties(fname=font_path).get_name()
            matplotlib.rcParams['font.family'] = font_name
            print(f"✓ フォント設定: {font_name}")
            return True
        
        # 他の一般的な日本語フォント
        font_candidates = [
            '/usr/share/fonts/truetype/takao-gothic/TakaoGothic.ttf',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc',  # macOS
            'C:/Windows/Fonts/msgothic.ttc',  # Windows
        ]
        
        for font_path in font_candidates:
            if os.path.exists(font_path):
                fm.fontManager.addfont(font_path)
                font_name = fm.FontProperties(fname=font_path).get_name()
                matplotlib.rcParams['font.family'] = font_name
                print(f"✓ フォント設定: {font_name}")
                return True
        
        # フォントが見つからない場合
        print("⚠ 日本語フォントが見つかりません。英語表示にフォールバックします。")
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        return False
        
    except Exception as e:
        print(f"⚠ フォント設定エラー: {e}")
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        return False

# 方法2: rcParamsを直接設定（環境に合わせて変更）
def setup_font_simple():
    """シンプルなフォント設定"""
    try:
        # 環境に合わせて設定
        import platform
        system = platform.system()
        
        if system == 'Linux':
            matplotlib.rcParams['font.family'] = 'IPAexGothic'
        elif system == 'Darwin':  # macOS
            matplotlib.rcParams['font.family'] = 'Hiragino Sans'
        elif system == 'Windows':
            matplotlib.rcParams['font.family'] = 'MS Gothic'
        else:
            matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        
        print(f"✓ システム: {system}, フォント: {matplotlib.rcParams['font.family']}")
        return True
    except:
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        return False

# フォント設定の実行
import os
setup_japanese_font()  # または setup_font_simple()

# マイナス記号の化け防止
matplotlib.rcParams['axes.unicode_minus'] = False

class Bio001Calculator:
    def __init__(self):
        self.N_stars = 2.0e11
        self.f_habitable = 0.22
        self.n_habitable = 1.2
        self.alpha_prior = 1
        self.beta_prior = 1
        self.solar_success = 1
        self.solar_trials = 8
    
    def bayesian_probability(self):
        """ベイズ更新による生命発生確率"""
        alpha = self.alpha_prior + self.solar_success
        beta = self.beta_prior + self.solar_trials - self.solar_success
        mean = alpha / (alpha + beta)
        ci_lower = stats.beta.ppf(0.025, alpha, beta)
        ci_upper = stats.beta.ppf(0.975, alpha, beta)
        return mean, ci_lower, ci_upper
    
    def monte_carlo(self, n=10000):
        """モンテカルロシミュレーション"""
        np.random.seed(42)
        
        f_h_samples = np.random.normal(self.f_habitable, 0.05, n)
        f_h_samples = np.clip(f_h_samples, 0, 1)
        
        n_h_samples = np.random.lognormal(np.log(self.n_habitable), 0.3, n)
        
        f_l_samples = np.random.beta(
            self.alpha_prior + self.solar_success,
            self.beta_prior + self.solar_trials - self.solar_success,
            n
        )
        
        P_samples = f_l_samples
        
        return {
            'samples': P_samples,
            'mean': np.mean(P_samples),
            'std': np.std(P_samples),
            'ci_lower': np.percentile(P_samples, 2.5),
            'ci_upper': np.percentile(P_samples, 97.5),
            'num_samples': n
        }
    
    def plot_results_simple(self, mc_results):
        """シンプルな可視化（文字化け対策済み）"""
        samples = mc_results['samples']
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # 1. ヒストグラム
        ax1 = axes[0]
        ax1.hist(samples, bins=50, density=True, alpha=0.7, 
                color='skyblue', edgecolor='black')
        ax1.axvline(mc_results['mean'], color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {mc_results["mean"]:.4f}')
        ax1.axvspan(mc_results['ci_lower'], mc_results['ci_upper'], 
                   alpha=0.2, color='green', label='95% CI')
        ax1.set_xlabel('Probability')
        ax1.set_ylabel('Density')
        ax1.set_title('BIO-001: Microbial Universality Probability')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 箱ひげ図と統計値
        ax2 = axes[1]
        # 箱ひげ図
        bp = ax2.boxplot(samples, vert=True, patch_artist=True,
                        boxprops=dict(facecolor='lightgreen', alpha=0.7))
        ax2.set_ylabel('Probability Value')
        ax2.set_title('Statistical Distribution')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 統計値をテキストで表示
        stats_text = f"""Statistics:
Mean: {mc_results['mean']:.6f}
Std: {mc_results['std']:.6f}
95% CI: [{mc_results['ci_lower']:.6f}, {mc_results['ci_upper']:.6f}]"""
        
        ax2.text(1.5, 0.5, stats_text, transform=ax2.transAxes,
                fontsize=10, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.suptitle('BIO-001 Analysis Results', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def plot_results_japanese(self, mc_results):
        """日本語表示の可視化（フォント設定が正しければ）"""
        samples = mc_results['samples']
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # 1. ヒストグラム
        ax1 = axes[0]
        n, bins, patches = ax1.hist(samples, bins=50, density=True, 
                                   alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(mc_results['mean'], color='red', linestyle='--', 
                   linewidth=2, label=f'平均: {mc_results["mean"]:.4f}')
        ax1.axvspan(mc_results['ci_lower'], mc_results['ci_upper'], 
                   alpha=0.2, color='green', label='95%信頼区間')
        ax1.set_xlabel('微生物宇宙普遍性確率')
        ax1.set_ylabel('確率密度')
        ax1.set_title('BIO-001: モンテカルロシミュレーション結果')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 箱ひげ図と統計値
        ax2 = axes[1]
        bp = ax2.boxplot(samples, vert=True, patch_artist=True,
                        boxprops=dict(facecolor='lightgreen', alpha=0.7))
        ax2.set_ylabel('確率値')
        ax2.set_title('統計的分布')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 統計値をテキストで表示
        stats_text = f"""統計的要約:
平均値: {mc_results['mean']:.6f}
標準偏差: {mc_results['std']:.6f}
95%信頼区間: [{mc_results['ci_lower']:.6f}, {mc_results['ci_upper']:.6f}]"""
        
        ax2.text(1.5, 0.5, stats_text, transform=ax2.transAxes,
                fontsize=10, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.suptitle('BIO-001: 微生物宇宙普遍性確率 分析結果', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def save_results(self, results):
        """結果を保存（JSONエラー対策済み）"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'BIO001_results_{timestamp}.json'
        
        # JSONシリアライズ可能なデータに変換
        output = {
            'timestamp': timestamp,
            'bayesian': {
                'mean': float(results['bayesian']['mean']),
                'ci_lower': float(results['bayesian']['ci'][0]),
                'ci_upper': float(results['bayesian']['ci'][1])
            },
            'monte_carlo': {
                'mean': float(results['monte_carlo']['mean']),
                'std': float(results['monte_carlo']['std']),
                'ci_lower': float(results['monte_carlo']['ci_lower']),
                'ci_upper': float(results['monte_carlo']['ci_upper']),
                'num_samples': int(results['monte_carlo']['num_samples']),
                'samples': results['monte_carlo']['samples'].tolist()  # リストに変換
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"結果を {filename} に保存しました")
        return filename
    
    def run(self, use_japanese=True):
        """メイン実行"""
        print("=" * 60)
        print("BIO-001: 微生物宇宙普遍性確率 計算")
        print("=" * 60)
        
        # 現在のフォント設定を表示
        print(f"現在のフォント設定: {matplotlib.rcParams['font.family']}")
        
        # 計算
        f_life, ci_low, ci_high = self.bayesian_probability()
        mc_results = self.monte_carlo(10000)
        
        print(f"\n1. ベイズ分析:")
        print(f"   確率: {f_life:.4f}")
        print(f"   95%CI: [{ci_low:.4f}, {ci_high:.4f}]")
        
        print(f"\n2. モンテカルロシミュレーション:")
        print(f"   平均: {mc_results['mean']:.6f}")
        print(f"   標準偏差: {mc_results['std']:.6f}")
        print(f"   95%CI: [{mc_results['ci_lower']:.6f}, {mc_results['ci_upper']:.6f}]")
        
        # 可視化
        print(f"\n3. 可視化生成中...")
        if use_japanese:
            try:
                self.plot_results_japanese(mc_results)
            except:
                print("⚠ 日本語表示に失敗しました。英語表示に切り替えます。")
                self.plot_results_simple(mc_results)
        else:
            self.plot_results_simple(mc_results)
        
        # 結果を保存
        results = {
            'bayesian': {'mean': f_life, 'ci': [ci_low, ci_high]},
            'monte_carlo': mc_results
        }
        
        self.save_results(results)
        
        return results

# テスト用：フォント設定の確認
def check_fonts():
    """利用可能なフォントを確認"""
    print("\n利用可能なフォント:")
    fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 日本語フォントを探す
    japanese_fonts = []
    for font in fonts:
        if any(keyword in font.lower() for keyword in ['gothic', 'ゴシック', 'mincho', '明朝', 'jp', 'japanese']):
            japanese_fonts.append(font)
    
    print(f"日本語フォント候補 ({len(japanese_fonts)}個):")
    for font in sorted(set(japanese_fonts))[:10]:  # 最初の10個
        print(f"  - {font}")
    
    if len(japanese_fonts) == 0:
        print("日本語フォントが見つかりませんでした。")

# メイン実行
if __name__ == "__main__":
    # フォント確認（オプション）
    # check_fonts()
    
    # 計算の実行
    calc = Bio001Calculator()
    
    # 日本語表示を試みる（失敗したら自動で英語にフォールバック）
    results = calc.run(use_japanese=True)
    
    print("\n" + "=" * 60)
    print("計算完了")
    print("=" * 60)
