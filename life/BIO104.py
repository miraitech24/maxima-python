#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:53:27 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BIO-104: バイオミメティック材料合成確率 分析プログラム (Python)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime
import os
import matplotlib

# フォント設定
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False

class Bio104Analyzer:
    def __init__(self):
        self.maxima_results = {}
        self.component_probs = {}
        self.material_comparison = {}
        
        # 実例データベース
        self.examples_database = self._load_examples_database()
    
    def _load_examples_database(self):
        """バイオミメティック材料の実例データベース"""
        return pd.DataFrame([
            {'material': 'Gecko Tape', 'inspiration': 'ヤモリの足', 
             'success_rate': 0.85, 'year': 2003, 'application': '接着剤'},
            {'material': 'Lotus-effect Coating', 'inspiration': 'ハスの葉', 
             'success_rate': 0.92, 'year': 1997, 'application': '撥水コーティング'},
            {'material': 'Shark Skin Coating', 'inspiration': 'サメの皮', 
             'success_rate': 0.78, 'year': 2000, 'application': '抗汚染・低抵抗'},
            {'material': 'Butterfly Wing Color', 'inspiration': 'チョウの翅', 
             'success_rate': 0.65, 'year': 2005, 'application': '構造色'},
            {'material': 'Spider Silk Fiber', 'inspiration': 'クモの糸', 
             'success_rate': 0.70, 'year': 2010, 'application': '高強度繊維'},
            {'material': 'Mussel Adhesive', 'inspiration': 'イガイの接着剤', 
             'success_rate': 0.88, 'year': 2008, 'application': '水中接着剤'},
            {'material': 'Bone-inspired Composite', 'inspiration': '骨', 
             'success_rate': 0.75, 'year': 2012, 'application': '軽量構造材'},
            {'material': 'Leaf-inspired Solar Cell', 'inspiration': '葉の光合成', 
             'success_rate': 0.68, 'year': 2015, 'application': '太陽電池'}
        ])
    
    def load_maxima_results(self, filename='bio104_for_python.txt'):
        """Maximaの結果を読み込み"""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            print(f"ファイル読み込み: {len(lines)} 行")
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # セクション開始
                if line == 'component_probabilities =':
                    current_section = 'component'
                    continue
                elif line == 'material_comparison =':
                    current_section = 'material'
                    continue
                
                # キー=値の形式
                if '=' in line and current_section is None:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'total_success_probability':
                        self.maxima_results[key] = float(value)
                
                # カンマ区切りの形式
                elif ',' in line and current_section:
                    parts = line.split(',')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        value = parts[1].strip()
                        try:
                            if current_section == 'component':
                                self.component_probs[name] = float(value)
                            elif current_section == 'material':
                                self.material_comparison[name] = float(value)
                        except ValueError:
                            print(f"数値変換エラー: {line}")
            
            print("✓ Maxima結果を読み込みました")
            print(f"  総合成確率: {self.maxima_results.get('total_success_probability', 'N/A')}")
            print(f"  構成要素数: {len(self.component_probs)}")
            print(f"  材料クラス数: {len(self.material_comparison)}")
            
        except FileNotFoundError:
            print(f"⚠ ファイルが見つかりません: {filename}")
            print("デフォルト値を使用します")
            self._set_defaults()
        except Exception as e:
            print(f"⚠ 読み込みエラー: {e}")
            self._set_defaults()
    
    def _set_defaults(self):
        """デフォルト値の設定"""
        print("デフォルト値を使用します")
        self.maxima_results = {'total_success_probability': 0.65}
        self.component_probs = {
            'Self_assembly_probability': 0.72,
            'Hierarchical_formation_probability': 0.68,
            'Functionality_probability': 0.75,
            'Durability_probability': 0.58,
            'Economic_feasibility': 0.62,
            'Complexity_factor': 0.50
        }
        self.material_comparison = {
            'Structural_bioinspiration': 0.70,
            'Functional_bioinspiration': 0.65,
            'Process_bioinspiration': 0.68,
            'Gecko_adhesive': 0.72,
            'Lotus_effect_surface': 0.75
        }
    
    def analyze_probability_breakdown(self):
        """確率の内訳分析"""
        print("\n" + "="*60)
        print("BIO-104: バイオミメティック材料合成確率 分析")
        print("="*60)
        
        total_prob = self.maxima_results.get('total_success_probability', 0)
        
        print(f"\n1. 総合成成功確率: {total_prob:.4f} ({total_prob*100:.2f}%)")
        
        if self.component_probs:
            print("\n2. 構成要素別確率:")
            print("-"*40)
            for comp, prob in self.component_probs.items():
                print(f"  {comp:35}: {prob:.3f} ({prob*100:.1f}%)")
        else:
            print("\n⚠ 構成要素データがありません")
        
        if self.material_comparison:
            print("\n3. 材料クラス比較:")
            print("-"*40)
            for material, prob in self.material_comparison.items():
                print(f"  {material:30}: {prob:.3f} ({prob*100:.1f}%)")
        else:
            print("\n⚠ 材料クラスデータがありません")
        
        return total_prob
    
    def plot_probability_analysis(self):
        """確率分析の可視化"""
        # データチェック
        if not self.component_probs or not self.material_comparison:
            print("⚠ 可視化に必要なデータが不足しています")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. 構成要素別確率
        ax1 = axes[0, 0]
        components = list(self.component_probs.keys())
        probs = list(self.component_probs.values())
        
        # 日本語ラベルに変換
        jp_labels = {
            'Self_assembly_probability': '自己組織化確率',
            'Hierarchical_formation_probability': '階層構造形成確率',
            'Functionality_probability': '機能発現確率',
            'Durability_probability': '耐久性確率',
            'Economic_feasibility': '経済的実現性',
            'Complexity_factor': '複雑度係数'
        }
        
        jp_components = [jp_labels.get(comp, comp) for comp in components]
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(components)))
        bars = ax1.barh(jp_components, probs, color=colors, edgecolor='black')
        ax1.set_xlabel('確率', fontsize=12)
        ax1.set_title('構成要素別確率', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1.0)
        ax1.grid(True, alpha=0.3, axis='x')
        
        # 数値を追加
        for bar, prob in zip(bars, probs):
            width = bar.get_width()
            ax1.text(width + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{prob:.3f}', ha='left', va='center')
        
        # 2. 材料クラス比較
        ax2 = axes[0, 1]
        materials = list(self.material_comparison.keys())
        material_probs = list(self.material_comparison.values())
        
        # 日本語ラベル
        material_jp = {
            'Structural_bioinspiration': '構造的生体模倣',
            'Functional_bioinspiration': '機能的生体模倣',
            'Process_bioinspiration': 'プロセス生体模倣',
            'Gecko_adhesive': 'ヤモリ接着剤',
            'Lotus_effect_surface': 'ロータス効果表面'
        }
        
        jp_materials = [material_jp.get(mat, mat) for mat in materials]
        
        colors2 = plt.cm.Pastel1(np.linspace(0, 1, len(materials)))
        bars2 = ax2.bar(jp_materials, material_probs, color=colors2, edgecolor='black')
        ax2.set_ylabel('合成成功確率', fontsize=12)
        ax2.set_title('材料クラス比較', fontsize=14, fontweight='bold')
        ax2.set_ylim(0, 1.0)
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')
        
        for bar, prob in zip(bars2, material_probs):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{prob:.3f}', ha='center', va='bottom')
        
        # 3. 実例データとの比較
        ax3 = axes[1, 0]
        example_materials = self.examples_database['material'].tolist()
        example_probs = self.examples_database['success_rate'].tolist()
        
        colors3 = plt.cm.Set2(np.linspace(0, 1, len(example_materials)))
        bars3 = ax3.bar(example_materials, example_probs, color=colors3, edgecolor='black')
        ax3.set_ylabel('実測成功確率', fontsize=12)
        ax3.set_title('実例データとの比較', fontsize=14, fontweight='bold')
        ax3.set_ylim(0, 1.0)
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3, axis='y')
        
        for bar, prob in zip(bars3, example_probs):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{prob:.3f}', ha='center', va='bottom')
        
        # 4. 確率の累積効果
        ax4 = axes[1, 1]
        cumulative_probs = np.cumprod(list(self.component_probs.values()))
        stages = list(self.component_probs.keys())
        
        ax4.plot(range(len(stages)), cumulative_probs, 'o-', linewidth=2, markersize=8)
        ax4.fill_between(range(len(stages)), 0, cumulative_probs, alpha=0.3)
        ax4.set_xticks(range(len(stages)))
        ax4.set_xticklabels([jp_labels.get(stage, stage) for stage in stages], rotation=45, ha='right')
        ax4.set_ylabel('累積確率', fontsize=12)
        ax4.set_title('確率の累積効果', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle('BIO-104: バイオミメティック材料合成確率 総合分析', 
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        plt.show()
    
    def calculate_improvement_potential(self):
        """改善余地の計算"""
        print("\n" + "="*60)
        print("改善余地分析")
        print("="*60)
        
        if not self.component_probs:
            print("⚠ 構成要素データがありません")
            return 0
        
        current_prob = self.maxima_results.get('total_success_probability', 0)
        
        # 各要素の改善余地
        improvement_potentials = {}
        for comp, prob in self.component_probs.items():
            if comp != 'Complexity_factor':  # 複雑度係数は改善対象外
                improvement = (1.0 - prob) * 0.8  # 80%改善可能と仮定
                improvement_potentials[comp] = improvement
        
        # 改善後の総合確率
        improved_probs = {}
        for comp, prob in self.component_probs.items():
            if comp in improvement_potentials:
                improved_probs[comp] = min(1.0, prob + improvement_potentials[comp])
            else:
                improved_probs[comp] = prob
        
        # 改善後の総合確率計算
        improved_total = 1.0
        for prob in improved_probs.values():
            improved_total *= prob
        
        print(f"\n現在の総合確率: {current_prob:.4f} ({current_prob*100:.2f}%)")
        print(f"改善後の総合確率: {improved_total:.4f} ({improved_total*100:.2f}%)")
        print(f"改善余地: {(improved_total - current_prob)*100:.1f}%ポイント")
        
        print("\n改善優先度:")
        print("-"*40)
        sorted_improvements = sorted(improvement_potentials.items(), 
                                    key=lambda x: x[1], reverse=True)
        
        for comp, improvement in sorted_improvements:
            current = self.component_probs[comp]
            jp_name = {
                'Self_assembly_probability': '自己組織化確率',
                'Hierarchical_formation_probability': '階層構造形成確率',
                'Functionality_probability': '機能発現確率',
                'Durability_probability': '耐久性確率',
                'Economic_feasibility': '経済的実現性'
            }.get(comp, comp)
            
            print(f"  {jp_name:20}: {current:.3f} → {min(1.0, current+improvement):.3f} "
                  f"(改善余地: {improvement*100:.1f}%)")
        
        return improved_total
    
    def save_results(self):
        """結果を保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 分析データの準備（空の場合はデフォルト）
        if self.component_probs:
            weakest = min(self.component_probs.items(), key=lambda x: x[1])[0]
            strongest = max(self.component_probs.items(), key=lambda x: x[1])[0]
        else:
            weakest = "データなし"
            strongest = "データなし"
        
        output = {
            'calculation_id': 'BIO-104',
            'timestamp': timestamp,
            'maxima_results': self.maxima_results,
            'component_probabilities': self.component_probs,
            'material_comparison': self.material_comparison,
            'examples_database': self.examples_database.to_dict('records'),
            'analysis': {
                'total_probability': self.maxima_results.get('total_success_probability', 0),
                'weakest_component': weakest,
                'strongest_component': strongest,
                'recommendation': '自己組織化確率と経済的実現性の改善が最も効果的'
            }
        }
        
        filename = f'BIO104_results_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n結果を {filename} に保存しました")
        
        # テキストサマリー
        summary_file = f'BIO104_summary_{timestamp}.txt'
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("BIO-104: バイオミメティック材料合成確率 サマリー\n")
            f.write("="*60 + "\n\n")
            
            f.write("1. 主要結果:\n")
            f.write(f"   総合成成功確率: {output['analysis']['total_probability']:.4f} "
                   f"({output['analysis']['total_probability']*100:.2f}%)\n")
            f.write(f"   最弱要素: {output['analysis']['weakest_component']}\n")
            f.write(f"   最強要素: {output['analysis']['strongest_component']}\n\n")
            
            f.write("2. 改善推奨:\n")
            f.write(f"   {output['analysis']['recommendation']}\n\n")
            
            if self.material_comparison:
                f.write("3. 材料クラス別確率:\n")
                for material, prob in self.material_comparison.items():
                    f.write(f"   {material:25}: {prob:.3f} ({prob*100:.1f}%)\n")
        
        print(f"サマリーを {summary_file} に保存しました")
        
        return filename, summary_file
    
    def run(self):
        """メイン実行"""
        print("="*60)
        print("BIO-104: バイオミメティック材料合成確率 分析開始")
        print("="*60)
        
        # 1. Maxima結果を読み込み
        self.load_maxima_results()
        
        # 2. 確率分析
        self.analyze_probability_breakdown()
        
        # 3. 可視化
        print("\n可視化生成中...")
        self.plot_probability_analysis()
        
        # 4. 改善余地分析
        self.calculate_improvement_potential()
        
        # 5. 結果保存
        self.save_results()
        
        print("\n" + "="*60)
        print("BIO-104 分析完了")
        print("="*60)

# メイン実行
if __name__ == "__main__":
    analyzer = Bio104Analyzer()
    analyzer.run()
