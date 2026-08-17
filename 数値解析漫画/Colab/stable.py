#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# ============================================================================
# 【重要】Hugging Face ミラーサイト設定（中国国内向け）
# ============================================================================
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# プロキシ設定（VPNを使用している場合はコメント解除）
# os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

# ============================================================================
# メインコード
# ============================================================================

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
from datetime import datetime

def generate_image_local(prompt, output_dir="generated_images"):
    """ローカルでStable Diffusionを実行"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # デバイス設定
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    
    print(f"🖥️ 使用デバイス: {device}")
    print(f"🔗 Hugging Face Endpoint: {os.environ.get('HF_ENDPOINT', 'default')}")
    print("⏳ モデルをロード中...（初回はダウンロードに時間がかかります）")
    
    try:
        # モデルのロード
#        pipe = StableDiffusionPipeline.from_pretrained(
#            "runwayml/stable-diffusion-v1-5",
#            torch_dtype=dtype,
#            use_auth_token=None
#        )
#        pipe = StableDiffusionPipeline.from_pretrained(
#            "hakurei/waifu-diffusion",  # アニメ風
#            torch_dtype=dtype
#        ) 
        pipe = StableDiffusionPipeline.from_pretrained(
            "dreamshaper/dreamshaper-8",  # 高品質な汎用モデル
            torch_dtype=dtype
         )
        pipe = pipe.to(device)
        
        # CPUモードの場合のメモリ節約
        if device == "cpu":
            pipe.enable_attention_slicing()
            print("💡 CPUモード: メモリ節約オプションを有効化")
        
        print("⏳ 画像生成中...")
        
        # 画像生成
        image = pipe(
            prompt,
            guidance_scale=7.5,
            num_inference_steps=30
        ).images[0]
        
        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/sd_image_{timestamp}.png"
        image.save(filename)
        
        print(f"✅ 画像を保存しました: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        print("")
        print("💡 対策:")
        print("  1. HF_ENDPOINT=https://hf-mirror.com が正しく設定されているか確認")
        print("  2. インターネット接続を確認")
        print("  3. プロキシ設定を確認（VPN使用時）")
        print("  4. 日本に帰国してから実行する（最も確実）")
        return None

# ============================================================================
# メイン実行
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Stable Diffusion 画像生成")
    print("=" * 60)
    print(f"📡 HF_ENDPOINT: {os.environ.get('HF_ENDPOINT', '未設定')}")
    print("=" * 60)
    
    # プロンプト入力
    prompt = input("\nプロンプトを入力してください: ").strip()
    if not prompt:
        prompt = "a beautiful landscape with mountains and lake, digital art, 4k"
        print(f"デフォルトプロンプトを使用: {prompt}")
    
    generate_image_local(prompt)