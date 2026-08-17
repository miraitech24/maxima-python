# POWERFUL_LLM

ターミナルで動く「思考の補助ツール」。計算・メモ・コード生成を一体化。

## これは何か？

LLM（大規模言語モデル）をターミナルから操作するCLIツールです。

「コーディングエージェント」ではありません。  
「プロジェクトを自動修正するツール」でもありません。

「数式処理」と「意図的なメモ管理」に特化した、思考の補助ツールです。

## 特徴（強み）

### 1. 掲示板（Board）機能

- 会話とは独立した「共有メモ」を管理できる

- 投稿・添付ファイル・ピン留めで意図的なコンテキスト管理が可能

- AnythingLLMのような「自動RAG」より精度が高い（人間が明示的に管理するため）

### 2. Maxima連携

- 数式処理・数値計算がターミナルから実行可能

- 他のLLM CLIツールにはない独自機能

### 3. Python実行統合

- コード生成→実行→結果確認が1フローで完結

- グラフ描画にも対応（matplotlib）

### 4. 複数API対応

- DeepSeek / Gemini / Grok を切り替え可能

- API残高エラーにも対応済み

### 5. セッション管理

- 会話履歴・掲示板をファイルで永続化

- セッション一覧表示・削除・名前変更が可能

## このツールの向き不向き（弱み）

### 向いている人

- 数式処理・計算をLLMと一緒に行いたい

- 「メモ」や「コンテキスト」を明示的に管理したい

- コード生成して手動でコピペするのに慣れている

- シンプルなターミナルツールが好き

### 向いていない人

- Git統合が必要な人（Aiderを使ってください）

- プロジェクト全体を自動修正したい人（OpenCodeを使ってください）

- エンタープライズ品質を求める人（Codex CLIを使ってください）

- エージェント的な自律ループを求める人

- リッチなUI・TUIを求める人

## インストール

リポジトリをクローン:  
git clone https://github.com/yourname/powerful_llm.git  
cd powerful_llm

依存関係をインストール:  
pip install -r requirements.txt

環境変数ファイルを作成:  
cp .env.example .env  
.env にAPIキーを記入

## 使い方

起動:  
python POWERFUL_LLM.py

メインメニュー:

- セッション一覧から選択 or 新規作成

- x [番号] でセッション削除

- y [番号] [名前] でセッション名変更

### 会話中コマンド

/help : 全コマンド一覧  
/clear : 会話履歴クリア  
/main : メインメニューに戻る  
/quit : 終了  
/ml : 複数行入力（/endで終了）  
/api : API切り替え

### 掲示板コマンド

/board list : 掲示板表示  
/board post 文章 : 投稿  
/board attach パス/URL : ファイル/URL添付  
/board attach_dir パス : .mac/.pyを一括添付  
/board show ID : 添付内容表示  
/board pin post/attach 番号 : ピン留め  
/board unpin post/attach 番号 : ピン留解除  
/board del post/attach 番号 : 削除（ID再設定）

### 実行コマンド

/maxima コード : Maxima実行  
/py コード : Python実行  
/auto : 複数行コード生成（/endで終了）

### 履歴コマンド

/history : 履歴一覧  
/history show N : 詳細表示  
/history del N : 削除（番号指定）  
/history del N-M : 削除（範囲指定）  
/history search_all 単語 : 全セッション検索

## ファイル構成

chat_history_{セッション名}.json : 会話履歴  
board_{セッション名}.json : 掲示板データ  
work_{セッション名}/ : 実行ファイル保存ディレクトリ

## 要件

- Python 3.8+

- OpenAIライブラリ（DeepSeek/Grok用）

- google-generativeai（Gemini用）

- Maxima（/maximaを使う場合）

## 投げ銭について

- 投げ銭は感謝の気持ちであり、製品の購入ではありません

- 投げ銭によってサポート義務や機能追加の約束は一切発生しません

- 開発は作者の趣味であり、投げ銭に依存していません

## メンテナンスポリシー

- このツールは作者が自分で使うために作られています

- バグ報告は歓迎しますが、対応は気が向いたときにします

- 機能追加リクエストは基本的に受け付けません（フォーク歓迎）

- PRは歓迎しますが、マージは作者の裁量です

## ライセンス

MIT License

## 謝辞

- DeepSeek / Gemini / Grok 各API提供元

- Maxima 開発チーム

- Python エコシステム
