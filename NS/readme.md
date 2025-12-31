# 課題：Maxima-Python連成によるS字配管内の流体解析システム

## 1. 概要

本プロジェクトは、数式処理ソフト **Maxima** と **Python** を連成させ、産業用プラント等で見られるS字型湾曲配管内の流体挙動（ナビエ・ストークス方程式）を解析するものである。

## 2. 数理モデル

[cite_start]解析対象は定常・非圧縮性粘性流体とし、以下のナビエ・ストークス方程式を基礎とする 。

$\mathbf{u} \cdot \nabla \mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u}$

## 3. システム構成と連成方法

- **Maxima (`spipe.mac`)**:
  - 基礎方程式の定義と、中央差分法に基づく代数的離散化の実施。
  - 美しい数式表記による数理的妥当性の検証。
  - `flow_equations.py` への計算式の自動エクスポート。
- **Python (`spipe.py,spipev.py`)**:
  - [cite_start]`%run` または `import` による導出式の取り込み 。
  - 3次元S字境界適合格子（Curvilinear Grid）の生成。
  - Maximaより継承したアルゴリズムを用いた収束計算の実行。

## 4. 可視化仕様

- **速度分布コンター図**: 配管内部を縦断する面での流速変化を色彩で表現。
- **ベクトル図**: 速度の方向と強さをカラーベクトル（Quiver）で重畳表示。

## 5. 特記事項

- [cite_start]宇宙物理分野以外の応用（空調設備、化学プラント配管等）を想定している 。

<img width="248" height="261" alt="spipe2025-12-31" src="https://github.com/user-attachments/assets/776d8342-ea7a-4ee0-8005-1a7b6df60331" />

<img width="788" height="664" alt="spipev2025-12-31" src="https://github.com/user-attachments/assets/2126cd74-4d93-4e1d-8046-bc8d198c2a3d" />


