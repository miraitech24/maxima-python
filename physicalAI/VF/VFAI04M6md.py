#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:35:05 2026

@author: iwamura
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VF-AI-04-M6: 材料・建設計画

【想定仕様書】
目的: VF-AI-04-M5の熱管理システム設計に基づき、865拠点建設に必要な
      材料量、建設スケジュール、コストを計算する。

入力データ:
1. VF-AI-04-M5の出力:
   - VF_AI_04_M5_results.csv: 熱管理システム仕様
   - VF_AI_04_M5_summary.txt: 熱管理サマリー

2. VF-AI-04-M4の出力:
   - VF_AI_04_M4_schedule.csv: 建設スケジュール
   - VF_AI_04_M4_site_data.csv: 拠点配置

3. 材料パラメータ:
   - 鋼材密度・コスト
   - コンクリート量
   - 溶融塩量
   - 建設機械コスト

出力:
1. 材料必要量の時系列
2. 建設コスト見積もり
3. 物流計画
4. 建設フェーズ計画
5. 総合レポート
"""

print("=" * 80)
print("VF-AI-04-M6: 材料・建設計画（仕様書）")
print("=" * 80)
print("\n【想定される計算内容】")
print("1. 材料必要量計算")
print("   - 鋼材（パイプ、構造材）")
print("   - コンクリート（基礎）")
print("   - 断熱材")
print("   - 溶融塩")
print("   - 熱交換器材料")
print("")
print("2. 建設コスト見積もり")
print("   - 材料費")
print("   - 建設費")
print("   - 輸送費")
print("   - 人件費")
print("")
print("3. 物流計画")
print("   - 材料輸送スケジュール")
print("   - 建設機械配置")
print("   - 人員配置計画")
print("")
print("4. 建設フェーズ")
print("   - フェーズ1: 基盤整備")
print("   - フェーズ2: 主要構造建設")
print("   - フェーズ3: システム統合")
print("   - フェーズ4: 試験・調整")
print("")
print("【必要な入力ファイル】")
print("1. VF_AI_04_M5_results.csv")
print("2. VF_AI_04_M5_summary.txt")
print("3. VF_AI_04_M4_schedule.csv")
print("4. VF_AI_04_M4_site_data.csv")
print("")
print("【出力ファイル】")
print("1. VF_AI_04_M6_materials.csv - 材料必要量")
print("2. VF_AI_04_M6_costs.csv - コスト見積もり")
print("3. VF_AI_04_M6_logistics.csv - 物流計画")
print("4. VF_AI_04_M6_phases.csv - 建設フェーズ")
print("5. VF_AI_04_M6_final_report.txt - 総合レポート")
print("=" * 80)
