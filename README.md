# Whisper × FastAPI ミニアプリ — 現状まとめ

## 目的
- ローカルに置いた Whisper（`faster-whisper`）で **音声→テキスト** を最小工数で実行  
- **FastAPI** で外部から叩ける HTTP API を提供  
- フロントは **素の HTML/CSS/JS**（最低限のUI）

---

## 現在の状態（サマリ）
- [x] **ffmpeg** を Homebrew で導入済み  
- [x] **仮想環境** `.venv` 作成 & 依存インストール済み  
- [x] **サーバ起動成功**（`uvicorn`）  
- [x] `POST /api/transcribe` で **JSON** が返るのを確認  
- [x] `?srt=1` で **SRT** をダウンロードできるのを確認  
- [x] **compute_type エラー**（`int8_float16` 非対応）→ **`int8`** に切り替えて解消  
- [x] 静的配信を `/ui` に分離（`/` は `/ui` へリダイレクト、405回避）

---

## 実行環境
- macOS（Apple Silicon）
- Python: 仮想環境（`python3 -m venv .venv`）
- 主要ライブラリ：`fastapi`, `uvicorn[standard]`, `faster-whisper`, `ffmpeg-python`, `python-multipart`
- モデル（デフォルト）：`small`（初回DLが軽い）  
  - **CPU** では `compute_type=int8` を基本に動作

---

## ディレクトリ構成
wisper_app_test/
├── app/
│ ├── init.py
│ ├── asr.py # 変換(16kHz/mono) & Whisper推論（compute_typeの自動フォールバック）
│ └── main.py # FastAPI本体（/api/transcribe, /ui, /→/ui）
└── web/
└── index.html # 最小UI（アップロード & SRTダウンロード）