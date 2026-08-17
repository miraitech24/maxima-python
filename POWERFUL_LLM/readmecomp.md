# POWERFUL_LLM

ターミナルLLMクライアント。計算・思考補助に特化。

## 強み

- 掲示板（共有メモ/添付/ピン留め）
- Maxima連携（数式処理）
- Python実行（コード生成→即検証）
- 複数API（DeepSeek/Gemini/Grok）
- セッション管理（保存/復元/エクスポート）

## 弱み（できないこと）

- Git連携なし（Aiderとは違う）
- プロジェクト全体理解なし（OpenCodeとは違う）
- エージェントループなし
- エディタ統合なし
- ローカルLLM非対応
- UIは質素（TUIではない）

## インストール

```bash
git clone ...
pip install -r requirements.txt
echo "DEEPSEEK_API_KEY=xxx" > .env
```
