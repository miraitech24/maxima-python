#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POWERFUL LLM - デバッグ版
修正: API残高エラー対応、メニュー表示、ID管理
"""
from dotenv import load_dotenv
load_dotenv()
import os
import json
import glob
import readline
import atexit
import subprocess
import shutil
import urllib.request
import re
from datetime import datetime
from openai import OpenAI

# ============================================================================
# TAG: 001 - 入力履歴設定
# ============================================================================
histfile = os.path.expanduser("~/.powerful_llm_history")
try:
    readline.read_history_file(histfile)
except:
    pass
atexit.register(readline.write_history_file, histfile)


# ============================================================================
# TAG: 010 - PowerfulLLM クラス定義
# ============================================================================
class PowerfulLLM:
    # ========================================================================
    # TAG: 020 - 初期化
    # ========================================================================
    def __init__(self, api_type: str, api_key: str, session_name: str):
        self.api_type = api_type
        self.session_name = session_name
        self.session_file = f"chat_history_{session_name}.json"
        self.board_file = f"board_{session_name}.json"
        self.work_dir = f"work_{session_name}"
        self.messages = self.load_history()
        self.board = self.load_board()
        os.makedirs(self.work_dir, exist_ok=True)
        
        if api_type == "deepseek":
            self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        elif api_type == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        elif api_type == "grok":
            self.client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        else:
            raise ValueError(f"Unknown API type: {api_type}")
    
    # ========================================================================
    # TAG: 030 - 履歴管理
    # ========================================================================
    def load_history(self) -> list:
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
    
    # ========================================================================
    # TAG: 040 - 掲示板管理（修正: ID管理を改善）
    # ========================================================================
    def load_board(self) -> dict:
        default = {"posts": [], "attachments": [], "next_post_id": 1, "next_attach_id": 1}
        if os.path.exists(self.board_file):
            try:
                with open(self.board_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if "posts" not in data:
                        data["posts"] = []
                    if "attachments" not in data:
                        data["attachments"] = []
                    if "next_post_id" not in data:
                        data["next_post_id"] = max([p.get("id", 0) for p in data["posts"]] + [0]) + 1
                    if "next_attach_id" not in data:
                        data["next_attach_id"] = max([a.get("id", 0) for a in data["attachments"]] + [0]) + 1
                    return data
            except:
                return default
        return default
    
    def save_board(self):
        with open(self.board_file, 'w', encoding='utf-8') as f:
            json.dump(self.board, f, ensure_ascii=False, indent=2)
    
    def _reindex_ids(self):
        """IDを詰め直す（連番にする）"""
        # 投稿のIDを詰め直し
        posts = sorted(self.board.get("posts", []), key=lambda x: x.get("id", 0))
        for i, post in enumerate(posts, 1):
            post["id"] = i
        self.board["posts"] = posts
        self.board["next_post_id"] = len(posts) + 1
        
        # 添付のIDを詰め直し
        attachments = sorted(self.board.get("attachments", []), key=lambda x: x.get("id", 0))
        for i, att in enumerate(attachments, 1):
            att["id"] = i
        self.board["attachments"] = attachments
        self.board["next_attach_id"] = len(attachments) + 1
        
        self.save_board()
    
    def get_board_context(self) -> str:
        context = ""
        for att in self.board.get("attachments", []):
            if att.get("pinned", False):
                context += f"\n=== [ピン留め] {att['name']} ===\n{att['content']}\n"
        for att in self.board.get("attachments", []):
            if not att.get("pinned", False):
                context += f"\n=== {att['name']} ===\n{att['content']}\n"
        for post in self.board.get("posts", []):
            if post.get("pinned", False):
                context += f"\n【ピン留め投稿】{post['text']}\n"
        for post in self.board.get("posts", []):
            if not post.get("pinned", False):
                context += f"\n{post['text']}\n"
        return context
    
    def board_post(self, text: str):
        post_id = self.board.get("next_post_id", 1)
        post = {"id": post_id, "text": text, "time": str(datetime.now()), "pinned": False}
        self.board.setdefault("posts", []).append(post)
        self.board["next_post_id"] = post_id + 1
        self.save_board()
        return f"📝 投稿 #{post_id} を追加しました"
    
    def board_attach(self, path_or_url: str):
        if not path_or_url:
            return "❌ パスまたはURLを入力してください"
        
        is_url = path_or_url.startswith(('http://', 'https://'))
        
        if is_url:
            try:
                with urllib.request.urlopen(path_or_url, timeout=10) as response:
                    content = response.read().decode('utf-8', errors='ignore')
                name = path_or_url.split('/')[-1] or 'url_content'
            except Exception as e:
                return f"❌ URL読み込みエラー: {e}"
        else:
            if not os.path.exists(path_or_url):
                return f"❌ ファイルが見つかりません: {path_or_url}"
            with open(path_or_url, 'r', encoding='utf-8') as f:
                content = f.read()
            name = os.path.basename(path_or_url)
        
        attach_id = self.board.get("next_attach_id", 1)
        attach = {
            "id": attach_id,
            "path": path_or_url,
            "name": name,
            "content": content[:10000],
            "time": str(datetime.now()),
            "pinned": False,
            "is_url": is_url
        }
        self.board.setdefault("attachments", []).append(attach)
        self.board["next_attach_id"] = attach_id + 1
        self.save_board()
        return f"📎 添付しました: {name} (ID: {attach_id})"
    
    def board_attach_dir(self, dir_path: str, extensions: list = [".mac", ".py"]):
        if not os.path.exists(dir_path):
            return f"❌ ディレクトリが見つかりません: {dir_path}"
        
        files = []
        for ext in extensions:
            files.extend(glob.glob(os.path.join(dir_path, f"*{ext}")))
        
        if not files:
            return f"❌ {', '.join(extensions)}ファイルが見つかりません"
        
        count = 0
        for f in files:
            result = self.board_attach(f)
            if "添付しました" in result:
                count += 1
        return f"📎 {count}個のファイルを添付しました"
    
    def board_show(self):
        try:
            with open(self.board_file, 'r', encoding='utf-8') as f:
                self.board = json.load(f)
        except:
            self.board = {"posts": [], "attachments": [], "next_post_id": 1, "next_attach_id": 1}
        
        result = f"\n=== 掲示板 [{self.session_name}] ===\n"
        
        attachments = self.board.get("attachments", [])
        if attachments:
            result += "\n【添付ファイル】\n"
            for att in attachments:
                pin = "📌 " if att.get("pinned") else "   "
                url_mark = "🌐 " if att.get("is_url") else "📄 "
                result += f"{pin}{url_mark}[{att['id']}] {att['name']}\n"
        
        posts = self.board.get("posts", [])
        if posts:
            result += "\n【投稿】\n"
            for post in posts[-10:]:
                pin = "📌 " if post.get("pinned") else "   "
                result += f"{pin}#{post['id']}: {post['text'][:60]}\n"
        return result
    
    def board_show_attach(self, attach_id: int):
        try:
            with open(self.board_file, 'r', encoding='utf-8') as f:
                board_data = json.load(f)
        except:
            return "❌ 掲示板データを読み込めません"
        
        for att in board_data.get("attachments", []):
            if att["id"] == attach_id:
                return f"=== {att['name']} ===\n{att['content']}"
        return f"❌ 添付ファイル #{attach_id} が見つかりません"
    
    def board_pin(self, target_type: str, target_id: int):
        try:
            with open(self.board_file, 'r', encoding='utf-8') as f:
                board_data = json.load(f)
        except:
            return "❌ 掲示板データを読み込めません"
        
        if target_type == "post":
            for i, post in enumerate(board_data.get("posts", [])):
                if post["id"] == target_id:
                    board_data["posts"][i]["pinned"] = True
                    with open(self.board_file, 'w', encoding='utf-8') as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=2)
                    self.board = board_data
                    return f"📌 投稿 #{target_id} をピン留めしました"
            return f"❌ 投稿 #{target_id} が見つかりません"
        elif target_type == "attach":
            for i, att in enumerate(board_data.get("attachments", [])):
                if att["id"] == target_id:
                    board_data["attachments"][i]["pinned"] = True
                    with open(self.board_file, 'w', encoding='utf-8') as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=2)
                    self.board = board_data
                    return f"📌 ファイル #{target_id} ({att['name']}) をピン留めしました"
            return f"❌ ファイル #{target_id} が見つかりません"
        return "使用方法: /board pin post <番号> または /board pin attach <番号>"
    
    def board_unpin(self, target_type: str = None, target_id: int = None):
        if target_type is None or target_id is None:
            return "使用方法: /board unpin post <番号> または /board unpin attach <番号>"
        
        try:
            with open(self.board_file, 'r', encoding='utf-8') as f:
                board_data = json.load(f)
        except:
            return "❌ 掲示板データを読み込めません"
        
        if target_type == "post":
            for i, post in enumerate(board_data.get("posts", [])):
                if post["id"] == target_id:
                    board_data["posts"][i]["pinned"] = False
                    with open(self.board_file, 'w', encoding='utf-8') as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=2)
                    self.board = board_data
                    return f"📌 投稿 #{target_id} のピン留めを解除しました"
            return f"❌ 投稿 #{target_id} が見つかりません"
        elif target_type == "attach":
            for i, att in enumerate(board_data.get("attachments", [])):
                if att["id"] == target_id:
                    board_data["attachments"][i]["pinned"] = False
                    with open(self.board_file, 'w', encoding='utf-8') as f:
                        json.dump(board_data, f, ensure_ascii=False, indent=2)
                    self.board = board_data
                    return f"📌 ファイル #{target_id} ({att['name']}) のピン留めを解除しました"
            return f"❌ ファイル #{target_id} が見つかりません"
        return "使用方法: /board unpin post <番号> または /board unpin attach <番号>"
    
    def board_delete(self, target_type: str, target_id: int):
        try:
            with open(self.board_file, 'r', encoding='utf-8') as f:
                board_data = json.load(f)
        except:
            return "❌ 掲示板データを読み込めません"
        
        if target_type == "post":
            board_data["posts"] = [p for p in board_data.get("posts", []) if p["id"] != target_id]
            # IDを詰め直し
            for i, post in enumerate(board_data["posts"], 1):
                post["id"] = i
            board_data["next_post_id"] = len(board_data["posts"]) + 1
            with open(self.board_file, 'w', encoding='utf-8') as f:
                json.dump(board_data, f, ensure_ascii=False, indent=2)
            self.board = board_data
            return f"🗑️ 投稿 #{target_id} を削除しました（IDは再設定されました）"
        elif target_type == "attach":
            board_data["attachments"] = [a for a in board_data.get("attachments", []) if a["id"] != target_id]
            # IDを詰め直し
            for i, att in enumerate(board_data["attachments"], 1):
                att["id"] = i
            board_data["next_attach_id"] = len(board_data["attachments"]) + 1
            with open(self.board_file, 'w', encoding='utf-8') as f:
                json.dump(board_data, f, ensure_ascii=False, indent=2)
            self.board = board_data
            return f"🗑️ 添付ファイル #{target_id} を削除しました（IDは再設定されました）"
        return "使用方法: /board del post <番号> または /board del attach <番号>"
    
    # ========================================================================
    # TAG: 050 - Maxima/Python実行
    # ========================================================================
    def run_maxima(self, code: str) -> dict:
        mac_file = os.path.join(self.work_dir, "calc.mac")
        with open(mac_file, 'w', encoding='utf-8') as f:
            f.write(code)
        try:
            result = subprocess.run(
                ["maxima", "--very-quiet", "-b", mac_file],
                capture_output=True, text=True, timeout=30
            )
            return {"success": True, "stdout": result.stdout[:1000], "file": mac_file}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_python(self, code: str) -> dict:
        font_setup = """
import matplotlib.pyplot as plt
try:
    import matplotlib.font_manager as fm
    for name in ["IPAexGothic", "Noto Sans CJK JP", "IPAGothic", "Yu Gothic"]:
        if name in {t.name for t in fm.fontManager.ttflist}:
            plt.rcParams["font.family"] = name
            break
    else:
        plt.rcParams["font.family"] = "sans-serif"
except:
    plt.rcParams["font.family"] = "sans-serif"
"""
        py_file = os.path.join(self.work_dir, "script.py")
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write(font_setup + "\n" + code)
        try:
            result = subprocess.run(
                ["python", py_file],
                capture_output=True, text=True, timeout=30
            )
            return {"success": True, "stdout": result.stdout[:1000], "file": py_file}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ========================================================================
    # TAG: 060 - Auto生成
    # ========================================================================
    def auto_calc(self, request: str) -> str:
        prompt = f"""以下の要求を満たすPythonコードを書いてください。

要求: {request}

条件:
- グラフが必要なら matplotlib を使う
- 結果は print() で表示する
- コードだけを返す（説明は不要）
- コードブロックは ```python と ``` で囲む
"""
        self.messages.append({"role": "user", "content": prompt})
        
        try:
            if self.api_type == "deepseek":
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=self.messages,
                    temperature=0.3
                )
                ai_response = response.choices[0].message.content
            elif self.api_type == "gemini":
                response = self.model.generate_content(prompt)
                ai_response = response.text
            elif self.api_type == "grok":
                response = self.client.chat.completions.create(
                    model="grok-beta",
                    messages=self.messages,
                    temperature=0.3
                )
                ai_response = response.choices[0].message.content
            else:
                return "Unknown API type"
        except Exception as e:
            error_msg = str(e)
            if "402" in error_msg or "Insufficient Balance" in error_msg:
                return f"❌ API残高が不足しています。\n\n詳細: {error_msg}\n\n💡 対応策:\n1. APIキーの残高を確認してください\n2. 別のAPIキーに切り替える (/api)\n3. 無料枠があるAPIを使用する"
            return f"❌ APIエラー: {error_msg}"
        
        self.messages.append({"role": "assistant", "content": ai_response})
        
        code_match = re.search(r'```python\n(.*?)\n```', ai_response, re.DOTALL)
        if not code_match:
            code_match = re.search(r'```\n(.*?)\n```', ai_response, re.DOTALL)
        if not code_match:
            return f"❌ コードを抽出できませんでした\n\n{ai_response[:500]}"
        
        code = code_match.group(1)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        code_file = os.path.join(self.work_dir, f"auto_{timestamp}.py")
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        result = self.run_python(code)
        
        output = f"🤖 要求: {request}\n\n"
        output += f"📁 コード保存: {code_file}\n\n"
        if result["success"]:
            output += f"✅ 実行結果:\n{result['stdout']}"
        else:
            output += f"❌ エラー:\n{result.get('error', result.get('stderr', '不明'))}"
        
        return output
    
    # ========================================================================
    # TAG: 070 - 会話（修正: エラーハンドリング強化）
    # ========================================================================
    def chat(self, user_input: str) -> str:
        board_context = self.get_board_context()
        if board_context:
            full_input = f"[掲示板の内容]\n{board_context}\n\n[質問]\n{user_input}"
        else:
            full_input = user_input
        
        self.messages.append({"role": "user", "content": full_input})
        
        try:
            if self.api_type == "deepseek":
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=self.messages,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
            elif self.api_type == "gemini":
                gemini_messages = []
                for msg in self.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    gemini_messages.append({"role": role, "parts": [msg["content"]]})
                response = self.model.generate_content(gemini_messages[-1]["parts"][0])
                answer = response.text
            elif self.api_type == "grok":
                response = self.client.chat.completions.create(
                    model="grok-beta",
                    messages=self.messages,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
            else:
                answer = "Unknown API type"
        except Exception as e:
            error_msg = str(e)
            if "402" in error_msg or "Insufficient Balance" in error_msg:
                return f"❌ API残高が不足しています。\n\n💡 対応策:\n1. APIキーの残高を確認してください\n2. 別のAPIキーに切り替える (/api)\n3. 無料枠があるAPIを使用する"
            return f"❌ APIエラー: {error_msg}"
        
        self.messages.append({"role": "assistant", "content": answer})
        self.save_history()
        return answer
    
    def clear_history(self):
        self.messages = []
        self.save_history()
        return "✅ 会話履歴をクリアしました"
    
    # ========================================================================
    # TAG: 080 - セッション入出力
    # ========================================================================
    def export_session(self, export_path: str):
        data = {
            "session_name": self.session_name,
            "messages": self.messages,
            "board": self.board,
            "exported_at": str(datetime.now())
        }
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return f"📤 セッションをエクスポートしました: {export_path}"
    
    def import_session(self, import_path: str):
        with open(import_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.messages = data.get("messages", [])
        self.board = data.get("board", {"posts": [], "attachments": [], "next_post_id": 1, "next_attach_id": 1})
        self.save_history()
        self.save_board()
        return f"📥 セッションをインポートしました: {import_path}"


# ============================================================================
# TAG: 090 - ユーティリティ関数
# ============================================================================
def get_multiline_input():
    """複数行入力（/end で終了）"""
    print("複数行入力モード（/end で終了）:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == '/end':
            break
        lines.append(line)
    return "\n".join(lines)


def get_auto_multiline_input():
    """/auto の複数行入力モード"""
    print("複数行入力モード（終了は /end）:")
    print("-" * 40)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == '/end':
            break
        lines.append(line)
    return "\n".join(lines)


def get_existing_sessions():
    files = glob.glob("chat_history_*.json")
    sessions = []
    for f in files:
        name = f.replace("chat_history_", "").replace(".json", "")
        sessions.append(name)
    return sorted(sessions)  # ソートして安定した順序に


def format_session_name(name, max_len=14):
    """セッション名を固定長に整形（全角対応）"""
    def display_width(s):
        width = 0
        for c in s:
            if ord(c) > 127:
                width += 2
            else:
                width += 1
        return width
    
    if display_width(name) > max_len:
        result = ""
        width = 0
        for c in name:
            cw = 2 if ord(c) > 127 else 1
            if width + cw > max_len - 3:
                result += "..."
                break
            result += c
            width += cw
        return result
    padding = max_len - display_width(name)
    return name + " " * padding


def delete_session_by_name(name):
    files = [f"chat_history_{name}.json", f"board_{name}.json"]
    for f in files:
        if os.path.exists(f):
            os.remove(f)
    if os.path.exists(f"work_{name}"):
        shutil.rmtree(f"work_{name}")
    return f"🗑️ セッション '{name}' を削除しました"


def rename_session_by_name(old, new):
    if os.path.exists(f"chat_history_{new}.json"):
        return f"❌ セッション '{new}' は既に存在します"
    pairs = [
        (f"chat_history_{old}.json", f"chat_history_{new}.json"),
        (f"board_{old}.json", f"board_{new}.json"),
        (f"work_{old}", f"work_{new}"),
    ]
    for old_f, new_f in pairs:
        if os.path.exists(old_f):
            os.rename(old_f, new_f)
    return f"✏️ セッション '{old}' → '{new}' に変更しました"


def delete_session_by_number(num: int):
    sessions = get_existing_sessions()
    if 1 <= num <= len(sessions):
        name = sessions[num - 1]
        result = delete_session_by_name(name)
        return f"{result}\n💡 注意: セッション番号が再設定されました"
    return "❌ セッションが見つかりません"


def rename_session_by_number(num: int, new_name: str):
    sessions = get_existing_sessions()
    if 1 <= num <= len(sessions):
        return rename_session_by_name(sessions[num - 1], new_name)
    return "❌ セッションが見つかりません"


def search_all_sessions(keyword: str):
    sessions = get_existing_sessions()
    result = f"=== '{keyword}' を含む履歴 ===\n"
    found = False
    for session in sessions:
        file = f"chat_history_{session}.json"
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            for msg in history:
                if keyword in msg.get("content", ""):
                    result += f"\n【{session}】\n{msg['content'][:200]}...\n"
                    found = True
    return result if found else "📭 見つかりませんでした"


def set_api_key(api_type: str) -> str:
    if api_type == "deepseek":
        key = input("DeepSeek APIキー: ").strip()
        os.environ["DEEPSEEK_API_KEY"] = key
        return key
    elif api_type == "gemini":
        key = input("Gemini APIキー: ").strip()
        os.environ["GEMINI_API_KEY"] = key
        return key
    elif api_type == "grok":
        key = input("Grok APIキー: ").strip()
        os.environ["GROK_API_KEY"] = key
        return key
    return ""


# ============================================================================
# TAG: 100 - メインループ（修正: メニュー表示と番号管理）
# ============================================================================
def main():
    api_type = "deepseek"
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    
    print("\n" + "=" * 60)
    print("POWERFUL LLM")
    print("=" * 60)
    
    if api_key:
        print(f"API: {api_type} (環境変数)")
    else:
        print(f"API: {api_type} (未設定 → /api)")
    print("=" * 60)
    
    while True:
        try:
            sessions = get_existing_sessions()
            print("\n" + "=" * 50)
            print("メインメニュー")
            print("=" * 50)
            
            # 2列表示（完全に揃える）
            mid = (len(sessions) + 1) // 2
            left_col = sessions[:mid]
            right_col = sessions[mid:]
            
            print("セッション:")
            max_len = max(len(left_col), len(right_col))
            
            # ヘッダー
            print(f"  {'番号':<6} {'セッション名':<20}  {'番号':<6} {'セッション名'}")
            
            for i in range(max_len):
                left_num = i + 1
                right_num = i + mid + 1
                
                if i < len(left_col):
                    left_name = format_session_name(left_col[i], 16)
                    left_str = f"  [{left_num:2d}]  {left_name}"
                else:
                    left_str = " " * 28
                
                if i < len(right_col):
                    right_name = format_session_name(right_col[i], 16)
                    right_str = f"  [{right_num:2d}]  {right_name}"
                else:
                    right_str = ""
                
                print(f"{left_str:<28}{right_str}")
            
            print(f"\n  [{len(sessions)+1:2d}]  新規作成")
            print(f"\n  x [番号]     : セッション削除")
            print(f"  y [番号] [名前]: セッション名変更")
            print(f"  z           : 終了")
            
            choice = input("\n選択: ").strip().lower()
            
            if choice == 'z':
                print("終了します")
                break
            elif choice.startswith('x'):
                parts = choice.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    num = int(parts[1])
                    print(delete_session_by_number(num))
                else:
                    print("使用方法: x <番号>")
                continue
            elif choice.startswith('y'):
                parts = choice.split()
                if len(parts) >= 3 and parts[1].isdigit():
                    num = int(parts[1])
                    new_name = ' '.join(parts[2:])
                    print(rename_session_by_number(num, new_name))
                else:
                    print("使用方法: y <番号> <新しい名前>")
                continue
            elif choice.isdigit():
                choice_num = int(choice)
                total = len(sessions)
                if 1 <= choice_num <= total:
                    session_name = sessions[choice_num - 1]
                elif choice_num == total + 1:
                    session_name = input("新しいセッション名: ").strip()
                    if not session_name:
                        session_name = f"s_{datetime.now().strftime('%m%d_%H%M%S')}"
                    new_session_file = f"chat_history_{session_name}.json"
                    if not os.path.exists(new_session_file):
                        with open(new_session_file, 'w', encoding='utf-8') as f:
                            json.dump([], f)
                    print(f"✅ 新規セッション '{session_name}' を作成しました")
                    continue
                else:
                    session_name = f"s_{datetime.now().strftime('%m%d_%H%M%S')}"
            else:
                session_name = f"s_{datetime.now().strftime('%m%d_%H%M%S')}"
            
            # APIキーが未設定なら設定
            if not api_key:
                print(f"\n⚠️ APIキー未設定 ({api_type})")
                api_key = set_api_key(api_type)
                if not api_key:
                    print("APIキーが設定されていません。終了します")
                    break
            
            llm = PowerfulLLM(api_type, api_key, session_name)
            
            print(f"\nセッション: {session_name} [API: {api_type}]")
            print("-" * 40)
            print("/help でコマンド一覧")
            print("/ml で複数行入力（/end で終了）")
            print("/auto で複数行コード生成（/end で終了）")
            print("-" * 40)
            
            while True:
                try:
                    user = input("\n> ").strip()
                    if not user:
                        continue
                    
                    if user == '/quit':
                        break
                    elif user == '/main':
                        print("メインメニューに戻ります...")
                        break
                    elif user == '/clear':
                        print(llm.clear_history())
                    elif user == '/ml':
                        multiline = get_multiline_input()
                        if multiline:
                            answer = llm.chat(multiline)
                            print(f"\n🤖 {answer}")
                        else:
                            print("入力が空です")
                    elif user == '/auto':
                        print("🤖 複数行コード生成モード（/end で終了）")
                        request = get_auto_multiline_input()
                        if request.strip():
                            result = llm.auto_calc(request)
                            print(result)
                        else:
                            print("要求が空です")
                    elif user == '/help':
                        print("""
=== コマンド一覧 ===
/help           - ヘルプ
/clear          - 会話履歴クリア
/main           - メインメニュー
/quit           - 終了
/ml             - 複数行入力（/endで終了）
/api            - API切り替え

/history        - 会話履歴表示（番号付き）
/history show N - 会話履歴詳細表示
/history del N  - 会話履歴削除（番号指定）
/history del N-M - 会話履歴削除（範囲指定）
/history search_all 単語 - 全セッション検索

/board list     - 掲示板表示
/board post 文章 - 投稿
/board attach パス/URL - ファイル/URL添付
/board attach_dir パス - ディレクトリ内の.mac/.pyを一括添付
/board show ID  - 添付ファイル内容表示
/board pin post 番号 - 投稿ピン留め
/board pin attach 番号 - ファイルピン留め
/board unpin post 番号 - ピン留解除
/board unpin attach 番号
/board del post 番号 - 投稿削除
/board del attach 番号 - 添付削除

/maxima コード   - Maxima実行
/py コード       - Python実行
/auto            - 複数行コード生成（/endで終了）

/export パス     - セッションエクスポート
/import パス     - セッションインポート
""")
                    elif user == '/api':
                        print("APIを選択:")
                        print("  1: DeepSeek")
                        print("  2: Gemini")
                        print("  3: Grok")
                        new_choice = input("選択 (1-3): ").strip()
                        new_api_type = None
                        new_api_key = None
                        if new_choice == "1":
                            new_api_type = "deepseek"
                            new_api_key = os.environ.get("DEEPSEEK_API_KEY")
                            if not new_api_key:
                                new_api_key = set_api_key("deepseek")
                        elif new_choice == "2":
                            new_api_type = "gemini"
                            new_api_key = os.environ.get("GEMINI_API_KEY")
                            if not new_api_key:
                                new_api_key = set_api_key("gemini")
                        elif new_choice == "3":
                            new_api_type = "grok"
                            new_api_key = os.environ.get("GROK_API_KEY")
                            if not new_api_key:
                                new_api_key = set_api_key("grok")
                        else:
                            print("無効な選択")
                            continue
                        if new_api_key:
                            api_type = new_api_type
                            api_key = new_api_key
                            print(f"✅ APIを {api_type} に切り替えました")
                    elif user == '/history':
                        if not llm.messages:
                            print("📭 会話履歴がありません")
                        else:
                            print("\n=== 会話履歴 ===\n")
                            for i, msg in enumerate(llm.messages, 1):
                                role = "👤" if msg["role"] == "user" else "🤖"
                                preview = msg["content"][:80] + ("..." if len(msg["content"]) > 80 else "")
                                print(f"{i:3d} {role}: {preview}")
                    elif user.startswith('/history show '):
                        try:
                            num = int(user.split()[2])
                            if 1 <= num <= len(llm.messages):
                                msg = llm.messages[num - 1]
                                print(f"\n=== 履歴 #{num} ===")
                                print(f"役割: {'👤 ユーザー' if msg['role'] == 'user' else '🤖 AI'}")
                                print(f"内容:\n{msg['content']}")
                            else:
                                print(f"❌ 履歴 #{num} は存在しません（1〜{len(llm.messages)}）")
                        except:
                            print("使用方法: /history show <番号>")
                    elif user.startswith('/history del '):
                        arg = user[13:].strip()
                        try:
                            if '-' in arg:
                                start, end = map(int, arg.split('-'))
                                if 1 <= start <= len(llm.messages) and 1 <= end <= len(llm.messages):
                                    del llm.messages[start-1:end]
                                    llm.save_history()
                                    print(f"✅ 履歴 {start}〜{end} を削除しました")
                                else:
                                    print(f"❌ 範囲が無効です（1〜{len(llm.messages)}）")
                            else:
                                num = int(arg)
                                if 1 <= num <= len(llm.messages):
                                    del llm.messages[num-1]
                                    llm.save_history()
                                    print(f"✅ 履歴 #{num} を削除しました")
                                else:
                                    print(f"❌ 履歴 #{num} は存在しません（1〜{len(llm.messages)}）")
                        except:
                            print("使用方法: /history del <番号> または /history del <開始>-<終了>")
                    elif user.startswith('/history search_all '):
                        keyword = user[21:].strip()
                        if keyword:
                            print(search_all_sessions(keyword))
                        else:
                            print("使用方法: /history search_all <単語>")
                    elif user == '/board list':
                        print(llm.board_show())
                    elif user.startswith('/board post '):
                        text = user[12:].strip()
                        if text:
                            print(llm.board_post(text))
                        else:
                            print("文章を入力してください")
                    elif user.startswith('/board attach '):
                        path = user[14:].strip()
                        if path:
                            print(llm.board_attach(path))
                        else:
                            print("パスまたはURLを入力してください")
                    elif user.startswith('/board attach_dir '):
                        path = user[18:].strip()
                        if path:
                            print(llm.board_attach_dir(path))
                        else:
                            print("ディレクトリパスを入力してください")
                    elif user.startswith('/board show '):
                        try:
                            aid = int(user.split()[2])
                            print(llm.board_show_attach(aid))
                        except:
                            print("使用方法: /board show <添付ID>")
                    elif user.startswith('/board pin '):
                        parts = user.split()
                        if len(parts) == 4 and parts[2] in ['post', 'attach']:
                            try:
                                pid = int(parts[3])
                                print(llm.board_pin(parts[2], pid))
                            except:
                                print("番号を入力してください")
                        else:
                            print("使用方法: /board pin post <番号> または /board pin attach <番号>")
                    elif user.startswith('/board unpin '):
                        parts = user.split()
                        if len(parts) == 4 and parts[2] in ['post', 'attach']:
                            try:
                                pid = int(parts[3])
                                print(llm.board_unpin(parts[2], pid))
                            except:
                                print("番号を入力してください")
                        else:
                            print("使用方法: /board unpin post <番号> または /board unpin attach <番号>")
                    elif user.startswith('/board del '):
                        parts = user.split()
                        if len(parts) == 4 and parts[2] in ['post', 'attach']:
                            try:
                                pid = int(parts[3])
                                print(llm.board_delete(parts[2], pid))
                            except:
                                print("番号を入力してください")
                        else:
                            print("使用方法: /board del post <番号> または /board del attach <番号>")
                    elif user.startswith('/maxima '):
                        code = user[8:].strip()
                        if code:
                            print("🔢 Maxima実行中...")
                            result = llm.run_maxima(code)
                            if result["success"]:
                                print(f"✅ 完了\n{result['stdout']}\n📁 {result['file']}")
                            else:
                                print(f"❌ {result.get('error')}")
                        else:
                            print("コードを入力してください")
                    elif user.startswith('/py '):
                        code = user[4:].strip()
                        if code:
                            print("🐍 Python実行中...")
                            result = llm.run_python(code)
                            if result["success"]:
                                print(f"✅ 完了\n{result['stdout']}\n📁 {result['file']}")
                            else:
                                print(f"❌ {result.get('error')}")
                        else:
                            print("コードを入力してください")
                    elif user.startswith('/export '):
                        path = user[8:].strip()
                        if path:
                            print(llm.export_session(path))
                        else:
                            print("使用方法: /export <パス>")
                    elif user.startswith('/import '):
                        path = user[8:].strip()
                        if path and os.path.exists(path):
                            print(llm.import_session(path))
                        else:
                            print(f"❌ ファイルが見つかりません: {path}")
                    else:
                        answer = llm.chat(user)
                        print(f"\n🤖 {answer}")
                except KeyboardInterrupt:
                    print("\n\n中断されました。セッションを続行します...")
                    continue
                    
        except KeyboardInterrupt:
            print("\n\n中断されました。メインメニューに戻ります...")
            continue
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")
            print("メインメニューに戻ります...")
            continue


if __name__ == "__main__":
    main()