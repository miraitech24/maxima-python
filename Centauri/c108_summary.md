# C108: 真空シール設計（再計算・真の連成版）

## 連成内容

【Maxima連成】sympyで記号計算 → Maximaで数値評価

### 拡散方程式の解析解

$ C(x,t) = C_0 \cdot \text{erf}\left(\frac{x}{2\sqrt{Dt}}\right) $

$ M(t) = 2C_0\sqrt{\frac{Dt}{\pi}} $

### 漏れ率（ポアズイユ流れ）

$ Q = \frac{\pi r^4 \Delta p}{8\eta L} $

### Oリング応力緩和

$ \sigma(t) = \sigma_0 \cdot \exp\left(-\frac{t}{\tau}\right) $

## 計算結果

<img width="1800" height="1500" alt="c108_vacuum_seal" src="https://github.com/user-attachments/assets/cd5263ef-1e81-45f3-8dc0-acef2cd302cb" />

- 10年後のアウトガス量: 44.81 nmol/m²
- 25℃での漏れ率: 69063223916.81 pL/s
- -100℃での漏れ率: 108305312831.63 pL/s
- 10年後のOリング応力: 0.41 MPa
- 応力保持率: 8.2 %

## 推奨シール材質

| 使用環境               | 推奨材質                  | 理由          |
| ------------------ | --------------------- | ----------- |
| プロキシマb（-100℃〜+50℃） | FKM（フッ素）またはVMQ（シリコーン） | 広い温度範囲に対応   |
| プロキシマc（-234℃一定）    | PTFE（テフロン）またはメタルシール   | 極低温でもシール性維持 |
| 0.8光年先BH近傍（高温）     | メタルシール（Cu）            | 高温に耐える      |
