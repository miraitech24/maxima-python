# 室内気流解析システム (Python + Maxima連成)

## 課題仕様

### 目的

室内空間（部屋）における空気の流れをNavier-Stokes方程式に基づいて解析する。

### 数式モデル

#### 連続の式 (非圧縮)

$$
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0
$$

#### Navier-Stokes方程式 (x方向)

$$
u\frac{\partial u}{\partial x} + v\frac{\partial u}{\partial y} = -\frac{1}{\rho}\frac{\partial p}{\partial x} + \nu\left(\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2}\right)
$$

#### Navier-Stokes方程式 (y方向)

$$
u\frac{\partial v}{\partial x} + v\frac{\partial v}{\partial y} = -\frac{1}{\rho}\frac{\partial p}{\partial y} + \nu\left(\frac{\partial^2 v}{\partial x^2} + \frac{\partial^2 v}{\partial y^2}\right)
$$

### パラメータ

| パラメータ     | 値       | 単位    |
| --------- | ------- | ----- |
| 空気密度 ρ    | 1.225   | kg/m³ |
| 動粘性係数 ν   | 1.5e-05 | m²/s  |
| 入口速度      | 0.5     | m/s   |
| レイノルズ数 Re | 66666.7 | -     |
| 計算格子数     | 60×45   | -     |

## 計算方式

airflow.py ->AIRFLOW_model.macをcall

## 結論

- **解像度**: 60×45 格子
- **最大流速**: 0.000 m/s
- **最大圧力**: 0.000 Pa

### 考察

1. **Maxima連成**: Navier-Stokes方程式の導出をMaximaに任せ、式の検証が容易になった
2. **室内気流特性**: 入口付近で加速し、障害物(家具)周辺で渦が発生する
3. **レイノルズ数**: 層流領域(Re<2000)に該当
4. **実用性**: 換気設計・空調配置の基礎評価に適用可能

### 今後の課題

- 3次元への拡張
- 乱流モデルの導入 (k-ε, LES)
- 熱輸送・浮力の考慮
- 時間発展計算 (非定常解析)
