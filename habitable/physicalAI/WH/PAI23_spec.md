# PAI-23: Exotic Matter Stability Verification

## 課題仕様

- ID: PAI-23
- 対象: Exotic Matter
- 物理的核心: Stability Verification
- 計算式: $\frac{\rho + 3p}{\rho - p} < \frac{1}{2\lambda}$
- Maxima導出式: $${{\rho+3\,p}\over{\rho-p}}<{{1}\over{2\,{\it lam}}}$$

## 実行方法

1. PAI23_maxima.mac (安定性条件の解析導出)
2. `PAI23.py` (数値計算+可視化)

## ファイル構成

| ファイル                  | 説明                 |
| --------------------- | ------------------ |
| `PAI23.py`            | メインPythonスクリプト     |
| `PAI23_maxima.mac`    | Maximaスクリプト（解析式導出） |
| `PAI23_spec.md`       | 課題仕様書（本ファイル）       |
| `PAI23_results.csv`   | 数値計算結果             |
| `PAI23_summary.txt`   | 計算サマリー             |
| `PAI23_stability.png` | 2x2グラフ             |

## グラフ説明

### (a) 安定性マップ

- エネルギー密度ρと圧力pのパラメータ空間における安定性を示す
- 黒線が安定性閾値。閾値より小さい領域が安定
- 赤色領域は不安定、青色領域は安定

### (b) 真空崩壊確率

- 時間経過に伴う真空崩壊（トンネル効果）の確率
- 50%崩壊時間が重要な設計パラメータ

### (c) エネルギー条件違反

- NEC/WEC/SECの各エネルギー条件に対する違反の有無
- エキゾチック物質は通常、NECとWECに違反する

### (d) 状態方程式パラメータ空間

- ρ-p平面での安定性分布
- 負のエネルギー密度領域がエキゾチック物質の特徴

## 結論

- NEC違反: True
- WEC違反: True
- SEC違反: True
- エキゾチック物質はNECとWECに違反するが、特定の条件下で安定に存在可能
- 真空崩壊確率は時間とともに増加し、長期的な安定性には対策が必要
