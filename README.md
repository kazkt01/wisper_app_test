# wis
Whisper × FastAPI ミニアプリ — 現状まとめ
目的

ローカルに置いた Whisper（faster-whisper）で 音声→テキスト を最小工数で実行

FastAPI で外部から叩ける HTTP API を提供

フロントは 素の HTML/CSS/JS（最低限のUI）

現在の状態（サマリ）

 ffmpeg を Homebrew で導入済み

 仮想環境 .venv 作成 & 依存インストール済み

 サーバ起動成功（uvicorn）

 POST /api/transcribe で JSON が返るのを確認

 ?srt=1 で SRT をダウンロードできるのを確認

 compute_type エラー（int8_float16 非対応）→ int8 に切り替えて解消

 静的配信を /ui に分離（/ は /ui へリダイレクト、405回避）

実行環境

macOS（Apple Silicon）

Python: 仮想環境（python3 -m venv .venv）

主要ライブラリ：fastapi, uvicorn[standard], faster-whisper, ffmpeg-python, python-multipart

モデル（デフォルト）：small（初回DLが軽い）

CPU では compute_type=int8 を基本に動作


