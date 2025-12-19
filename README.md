```markdown
wxMaxima と Spyder の連成サンプル（質量-ばね-ダンパ系）
=====================================================

概要
----
- params.txt にパラメータを記述（Maxima の代入式形式: `m: 1.0;` のように）
- wxMaxima (problem.wxm) を実行すると params.txt を読み込み、解析パラメータ（wn, zeta）を analytic.txt に出力
- Spyder（または普通の Python 実行）で spyder_solve_and_plot.py を実行すると:
  - params.txt, analytic.txt を読み込む
  - 数値解を求め、解析解と比較して results.csv と response.png を生成

ファイル一覧
------------
- params.txt : 入力パラメータ（テキスト）
- problem.wxm : wxMaxima 用スクリプト（Maxima による解析）
- analytic.txt : Maxima が出力する解析パラメータ（自動生成）
- spyder_solve_and_plot.py : Python（Spyder で開いて実行）
- results.csv : Python 実行で生成される数値データ
- response.png : プロット画像

実行手順
--------
1. 同じディレクトリに params.txt を置く（中身は上記参照）
2. wxMaxima を開き problem.wxm をロードしてセルを評価（または Maxima に対して `batch("problem.wxm");`）
   - 実行後に analytic.txt が作成される
3. Spyder で spyder_solve_and_plot.py を開き実行
   - results.csv と response.png が作成され、プロットが表示される

メモ
----
- params.txt は Maxima が直接読み込める形（`name: value;`）になっていますが、必要なら別フォーマット（JSON 等）にして両方のパーサを調整できます。
- Maxima からより詳細な解析式（完全な解析解テキスト）を直接出力して Python で評価することも可能です（このサンプルでは安定して動くように wn, zeta のみを書き出しています）。
- Spyder 上でプロットが表示されない場合は、Matplotlib のバックエンド設定を確認してください（%matplotlib inline / qt5 など）。

```