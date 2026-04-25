#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:23:47 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-102: 人工光合成効率 分析 (日本語フォント対応版)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import matplotlib
import os

# 日本語フォント設定
def setup_japanese_font():
    """日本語フォントの設定"""
    try:
        # システムに応じたフォント設定
        import platform
        system = platform.system()
        
        if system == 'Linux':
            # Linux: IPAexゴシック
            font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
            if os.path.exists(font_path):
                matplotlib.font_manager.fontManager.addfont(font_path)
                font_name = matplotlib.font_manager.FontProperties(fname=font_path).get_name()
                matplotlib.rcParams['font.family'] = font_name
                print(f"✓ フォント設定: {font_name}")
                return True
            
            # 代替: Noto Sans CJK
            font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
            if os.path.exists(font_path):
                matplotlib.font_manager.fontManager.addfont(font_path)
                font_name = matplotlib.font_manager.FontProperties(fname=font_path).get_name()
                matplotlib.rcParams['font.family'] = font_name
                print(f"✓ フォント設定: {font_name}")
                return True
        
        elif system == 'Darwin':  # macOS
            matplotlib.rcParams['font.family'] = 'Hiragino Sans'
            print("✓ フォント設定: Hiragino Sans (macOS)")
            return True
        
        elif system == 'Windows':
            matplotlib.rcParams['font.family'] = 'MS Gothic'
            print("✓ フォント設定: MS Gothic (Windows)")
            return True
        
        # フォントが見つからない場合
        print("⚠ 日本語フォントが見つかりません。英語表示に切り替えます。")
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        return False
        
    except Exception as e:
        print(f"⚠ フォント設定エラー: {e}")
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
        return False

# フォント設定を実行
setup_japanese_font()

# マイナス記号の化け防止
matplotlib.rcParams['axes.unicode_minus'] = False

class Bio102SimpleAnalyzer:
    def __init__(self):
        self.results = {}
        self.stages = {}
    
    def load_results(self, filename='bio102_simple_results.txt'):
        """結果を読み込み"""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        self.results[key] = float(value)
            
            # 段階効率を整理
            self.stages = {
                '光吸収': self.results.get('stage_absorption', 0),
                '電荷分離・輸送': self.results.get('stage_charge', 0),
                '触媒反応': self.results.get('stage_catalyst', 0),
                '過電圧': self.results.get('stage_overpotential', 0),
                'システム': self.results.get('stage_system', 0)
            }
            
            print("✓ 結果を読み込みました")
            
        except FileNotFoundError:
            print("⚠ ファイルが見つかりません。デフォルト値を使用します")
            self._set_defaults()
    
    def _set_defaults(self):
        """デフォルト値"""
        self.results = {
            'total_efficiency': 0.127,
            'photon_energy_550nm_J': 3.61e-19
        }
        self.stages = {
            '光吸収': 0.95,
            '電荷分離・輸送': 0.65,
            '触媒反応': 0.81,
            '過電圧': 0.75,
            'システム': 0.95
        }
    
    def analyze(self):
        """分析実行"""
        print("\n" + "="*60)
        print("BIO-102: 人工光合成効率 分析")
        print("="*60)
        
        total_eff = self.results.get('total_efficiency', 0)
        
        print(f"\n総合効率: {total_eff:.4f} ({total_eff*100:.2f}%)")
        
        print("\n段階別効率:")
        print("-"*40)
        cumulative = 1.0
        for stage, eff in self.stages.items():
            cumulative *= eff
            print(f"  {stage:15} : {eff:.3f} ({eff*100:.1f}%) → 累積: {cumulative:.3f}")
        
        print(f"\n計算総合: {cumulative:.4f}")
        print(f"Maxima総合: {total_eff:.4f}")
        
        return total_eff
    
    def plot_with_fallback(self):
        """フォールバック付き可視化"""
        try:
            self._plot_japanese()
        except:
            print("⚠ 日本語表示に失敗。英語表示に切り替えます。")
            self._plot_english()
    
    def _plot_japanese(self):
        """日本語表示の可視化"""
        stages = list(self.stages.keys())
        efficiencies = list(self.stages.values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 1. 段階別効率
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax1.bar(stages, efficiencies, color=colors, edgecolor='black')
        ax1.set_ylabel('効率', fontsize=12)
        ax1.set_title('段階別効率', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, 1.0)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # 数値を追加
        for bar, eff in zip(bars, efficiencies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{eff:.2f}', ha='center', va='bottom')
        
        # 2. 累積効率
        ax2.plot(stages, np.cumprod(efficiencies), 'o-', linewidth=2, markersize=8)
        ax2.fill_between(range(len(stages)), 0, np.cumprod(efficiencies), alpha=0.3)
        ax2.set_xticks(range(len(stages)))
        ax2.set_xticklabels(stages, rotation=45)
        ax2.set_ylabel('累積効率', fontsize=12)
        ax2.set_title('累積効率の推移', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle('BIO-102: 人工光合成効率分析', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def _plot_english(self):
        """英語表示の可視化"""
        # 英語ラベルに変換
        stage_labels = {
            '光吸収': 'Absorption',
            '電荷分離・輸送': 'Charge Separation/Transport',
            '触媒反応': 'Catalyst Reaction',
            '過電圧': 'Overpotential',
            'システム': 'System'
        }
        
        stages_en = [stage_labels.get(stage, stage) for stage in self.stages.keys()]
        efficiencies = list(self.stages.values())
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 1. Stage efficiencies
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        bars = ax1.bar(stages_en, efficiencies, color=colors, edgecolor='black')
        ax1.set_ylabel('Efficiency', fontsize=12)
        ax1.set_title('Stage Efficiencies', fontsize=14, fontweight='bold')
        ax1.set_ylim(0, 1.0)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add values
        for bar, eff in zip(bars, efficiencies):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{eff:.2f}', ha='center', va='bottom')
        
        # 2. Cumulative efficiency
        ax2.plot(stages_en, np.cumprod(efficiencies), 'o-', linewidth=2, markersize=8)
        ax2.fill_between(range(len(stages_en)), 0, np.cumprod(efficiencies), alpha=0.3)
        ax2.set_xticks(range(len(stages_en)))
        ax2.set_xticklabels(stages_en, rotation=45)
        ax2.set_ylabel('Cumulative Efficiency', fontsize=12)
        ax2.set_title('Cumulative Efficiency Trend', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle('BIO-102: Artificial Photosynthesis Efficiency Analysis', 
                    fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def compare_with_natural(self):
        """自然光合成との比較"""
        natural = 0.012  # 1.2%
        artificial = self.results.get('total_efficiency', 0.127)
        
        print("\n" + "="*60)
        print("自然光合成 vs 人工光合成")
        print("="*60)
        
        print(f"\n自然光合成 (BIO-101): {natural:.4f} ({natural*100:.2f}%)")
        print(f"人工光合成 (BIO-102): {artificial:.4f} ({artificial*100:.2f}%)")
        print(f"効率比: {artificial/natural:.1f}倍")
        
        # 可視化（フォールバック付き）
        try:
            self._plot_comparison_japanese(natural, artificial)
        except:
            self._plot_comparison_english(natural, artificial)
    
    def _plot_comparison_japanese(self, natural, artificial):
        """日本語比較グラフ"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        categories = ['自然光合成\n(BIO-101)', '人工光合成\n(BIO-102)', '理論的限界']
        values = [natural, artificial, 0.30]
        colors = ['#2ECC71', '#3498DB', '#E74C3C']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
        ax.set_ylabel('効率', fontsize=12)
        ax.set_title('光合成効率の比較', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 0.35)
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                   f'{val:.3f}\n({val*100:.1f}%)', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def _plot_comparison_english(self, natural, artificial):
        """英語比較グラフ"""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        categories = ['Natural\n(BIO-101)', 'Artificial\n(BIO-102)', 'Theoretical Limit']
        values = [natural, artificial, 0.30]
        colors = ['#2ECC71', '#3498DB', '#E74C3C']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Efficiency', fontsize=12)
        ax.set_title('Photosynthesis Efficiency Comparison', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 0.35)
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                   f'{val:.3f}\n({val*100:.1f}%)', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def save(self):
        """結果を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        output = {
            'calculation': 'BIO-102',
            'timestamp': timestamp,
            'total_efficiency': self.results.get('total_efficiency', 0),
            'stages': self.stages,
            'comparison': {
                'natural': 0.012,
                'artificial': self.results.get('total_efficiency', 0),
                'ratio': self.results.get('total_efficiency', 0) / 0.012
            }
        }
        
        filename = f'BIO102_results_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n結果を {filename} に保存しました")
        return filename
    
    def run(self):
        """メイン実行"""
        print("="*60)
        print("BIO-102: 人工光合成効率 分析開始")
        print("="*60)
        
        # 結果読み込み
        self.load_results()
        
        # 分析
        self.analyze()
        
        # 可視化（自動フォールバック）
        print("\n可視化生成中...")
        self.plot_with_fallback()
        
        # 比較
        self.compare_with_natural()
        
        # 保存
        self.save()
        
        print("\n" + "="*60)
        print("分析完了")
        print("="*60)

# メイン実行
if __name__ == "__main__":
    analyzer = Bio102SimpleAnalyzer()
    analyzer.run()
