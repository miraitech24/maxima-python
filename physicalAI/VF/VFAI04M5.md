## VF-AI-04-M5: 熱管理システム設計

## 【仕様書】

目的: VF-AI-04-M4のネットワーク配置に基づき、865拠点の熱管理システムを設計する。 入力データ:

1. VF-AI-04-M4の出力:
   - VF_AI_04_M4_site_data.csv: 拠点配置データ
   - VF_AI_04_M4_schedule.csv: 建設スケジュール
   - VF_AI_04_M4_summary.txt: ネットワークサマリー
2. 物理制約:
   - 各拠点発熱量: 10TW地下炉
   - 熱伝導媒体: 溶融塩 (NaK, 700-900K)
   - 熱輸送距離: 拠点間平均距離
   - 熱損失許容: 総発熱の5%以下
3. 設計目標:
   - 熱輸送ネットワークの最適化
   - 熱交換器のサイジング
   - 冷却システム設計
   - 熱エネルギー貯蔵設計
     出力:
4. 熱輸送ネットワーク設計図
5. 熱交換器仕様
6. 冷却システム設計
7. 熱エネルギー貯蔵計画
8. 次のモジュールへの引き渡しデータ



================================================================================
VF-AI-04-M5: Thermal Management System Design
================================================================================

1. Setting up font configuration...
   Using default sans-serif font (no Japanese)

2. Checking required files...
   ✓ VF_AI_04_M4_site_data.csv
   ✓ VF_AI_04_M4_schedule.csv
   ✓ VF_AI_04_M4_summary.txt

3. Loading data...
   Sites: 865
   Schedule points: 31

4. Thermal calculations...
   Heat per site: 6.50 TW
   Mass flow: 20967741.9 kg/s
   Volume flow: 11648.746 m³/s
   Pipe diameter: 86.115 m (86115.2 mm)

5. Creating visualizations...
   Saved: VF_AI_04_M5_main.png

6. Detailed calculations...
   Heat loss per pipe: 0.73 GW
   Heat loss percentage: 0.01%
   Heat exchanger area: 70358179.8 m²
   Saved: VF_AI_04_M5_detailed.png

7. Saving results...
   Saved: VF_AI_04_M5_results.csv
   Saved: VF_AI_04_M5_summary.txt

================================================================================
COMPLETE: VF-AI-04-M5
================================================================================

Output files created:

1. VF_AI_04_M5_main.png
2. VF_AI_04_M5_detailed.png
3. VF_AI_04_M5_results.csv
4. VF_AI_04_M5_summary.txt

Next module: VF-AI-04-M6
