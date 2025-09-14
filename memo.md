2025/09/14
起動方法

<!-- アプリのディレクトリに移動 -->
cd wisper_app_test   
<!--　pythonの仮想環境を構築-->
python3 -m venv .venv
source .venv/bin/activate

<!-- その中で起動し -->
uvicorn app.main:app --reload --port 8000

<!-- 以下でブラウザにUI表示されているのを覗きに行きそこでファイルをUPすると一応使える。 -->
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

<!-- APIを直接叩くなら-Fのとこにファイルを入れて飛ばすとできる -->
curl -X POST \
  -F "file=@test.wav" \
  -F "language=ja" \
  http://127.0.0.1:8000/api/transcribe


<!-- 文字起こし受け取りたいならこれ -->
curl -o out.srt -X POST \
  -F "file=@test.wav" \
  -F "language=ja" \
  "http://127.0.0.1:8000/api/transcribe?srt=1"








2025/09/02
・wisperをローカルに落とす。
・Fast APIで外部から叩ける仕様にする。

<!-- まず、ffmpegをダウンロード -->


# macOS（Homebrew）
brew install ffmpeg


<!-- 仮想環境を作る？ -->
python3 -m venv .venv

