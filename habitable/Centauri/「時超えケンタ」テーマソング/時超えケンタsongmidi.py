#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 15:45:30 2026

@author: iwamura
"""

import struct
import subprocess
import os

def note_num(name, octave=4):
    notes = {'C':0, 'C#':1, 'D':2, 'D#':3, 'E':4, 'F':5, 'F#':6, 'G':7, 'G#':8, 'A':9, 'A#':10, 'B':11}
    return notes[name] + (octave+1)*12

def create_simple_midi(filename, tempo=120):
    """シンプルなMIDIファイルを生成（MuseScore互換）"""
    
    ppqn = 480  # 分解能
    
    # ---- トラック0: テンポ設定のみ ----
    track0 = bytearray()
    # テンポ
    tempo_us = 60000000 // tempo
    track0.extend([0x00, 0xFF, 0x51, 0x03])
    track0.extend(struct.pack('>I', tempo_us)[1:])
    # トラック終了
    track0.extend([0x00, 0xFF, 0x2F, 0x00])
    
    # ---- トラック1: 音符のみ ----
    track1 = bytearray()
    
    # プログラムチェンジ（ピアノ）
    track1.extend([0x00, 0xC0, 0x00])
    
    # メロディ（音価はティック単位）
    notes_data = [
        # (ノートナンバー, 開始位置, 長さ)
        # Aメロ
        (note_num('E',4), 0, 480),
        (note_num('E',4), 480, 480),
        (note_num('F',4), 960, 480),
        (note_num('G',4), 1440, 480),
        (note_num('A',4), 1920, 960),
        (note_num('G',4), 2880, 480),
        (note_num('E',4), 3360, 480),
        (note_num('C',4), 3840, 960),
        (note_num('D',4), 4800, 480),
        (note_num('E',4), 5280, 480),
        (note_num('F',4), 5760, 960),
        (note_num('E',4), 6720, 480),
        (note_num('D',4), 7200, 480),
        (note_num('C',4), 7680, 1920),
        # Aメロ2
        (note_num('E',4), 9600, 480),
        (note_num('E',4), 10080, 480),
        (note_num('F',4), 10560, 480),
        (note_num('G',4), 11040, 480),
        (note_num('A',4), 11520, 960),
        (note_num('G',4), 12480, 480),
        (note_num('E',4), 12960, 480),
        (note_num('C',4), 13440, 960),
        (note_num('D',4), 14400, 480),
        (note_num('E',4), 14880, 480),
        (note_num('F',4), 15360, 960),
        (note_num('E',4), 16320, 480),
        (note_num('D',4), 16800, 480),
        (note_num('C',4), 17280, 1920),
        # Bメロ
        (note_num('F',4), 19200, 480),
        (note_num('G',4), 19680, 480),
        (note_num('A',4), 20160, 960),
        (note_num('A',4), 21120, 480),
        (note_num('G',4), 21600, 480),
        (note_num('F',4), 22080, 960),
        (note_num('E',4), 23040, 480),
        (note_num('F',4), 23520, 480),
        (note_num('G',4), 24000, 960),
        (note_num('C',4), 24960, 480),
        (note_num('E',4), 25440, 480),
        (note_num('C',4), 25920, 960),
        # サビ
        (note_num('C',5), 26880, 480),
        (note_num('C',5), 27360, 480),
        (note_num('B',4), 27840, 480),
        (note_num('A',4), 28320, 480),
        (note_num('G',4), 28800, 960),
        (note_num('A',4), 29760, 480),
        (note_num('B',4), 30240, 480),
        (note_num('C',5), 30720, 960),
        (note_num('C',5), 31680, 480),
        (note_num('B',4), 32160, 480),
        (note_num('A',4), 32640, 960),
        (note_num('G',4), 33600, 480),
        (note_num('F',4), 34080, 480),
        (note_num('E',4), 34560, 960),
        (note_num('F',4), 35520, 480),
        (note_num('G',4), 36000, 480),
        (note_num('A',4), 36480, 1920),
    ]
    
    # デルタタイム方式でイベントを生成
    current_time = 0
    for pitch, start, duration in sorted(notes_data, key=lambda x: x[1]):
        # 開始位置までのデルタ
        delta = start - current_time
        if delta > 0:
            track1.extend(encode_delta(delta))
        else:
            track1.extend([0x00])
        # ノートオン
        track1.extend([0x90, pitch, 100])
        current_time = start
        
        # ノートオフまでのデルタ
        track1.extend(encode_delta(duration))
        # ノートオフ
        track1.extend([0x80, pitch, 0])
        current_time = start + duration
    
    # トラック終了
    track1.extend([0x00, 0xFF, 0x2F, 0x00])
    
    # ---- MIDIファイル構築 ----
    with open(filename, 'wb') as f:
        # ヘッダ
        f.write(b'MThd')
        f.write(struct.pack('>I', 6))
        f.write(struct.pack('>H', 1))  # フォーマット1
        f.write(struct.pack('>H', 2))  # 2トラック
        f.write(struct.pack('>H', ppqn))
        
        # トラック0
        f.write(b'MTrk')
        f.write(struct.pack('>I', len(track0)))
        f.write(track0)
        
        # トラック1
        f.write(b'MTrk')
        f.write(struct.pack('>I', len(track1)))
        f.write(track1)
    
    return filename

def encode_delta(value):
    """可変長長さをエンコード"""
    if value == 0:
        return bytes([0])
    result = []
    while value > 0:
        result.insert(0, value & 0x7F)
        value >>= 7
    for i in range(len(result) - 1):
        result[i] |= 0x80
    return bytes(result)

# 生成
output_path = "tokikoe_kenta_simple.mid"
create_simple_midi(output_path, tempo=120)
print(f"MIDIファイル生成: {output_path}")
print(f"ファイルサイズ: {os.path.getsize(output_path)} バイト")

# 演奏
try:
    if os.name == 'nt':
        os.startfile(output_path)
    elif os.name == 'posix':
        for player in ['timidity', 'fluidsynth', 'aplaymidi', 'playmidi']:
            try:
                subprocess.Popen([player, output_path],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"演奏中: {player}")
                break
            except FileNotFoundError:
                continue
except Exception as e:
    print(f"演奏エラー: {e}")

print(f"\nMuseScoreで開く: {output_path}")
