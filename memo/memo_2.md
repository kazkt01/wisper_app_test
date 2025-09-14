2025/09/14


1,app/ ディレクトリ
・Pythonアプリの中核をここにまとめている
・main.py
　・FastAPIの「入口」。サーバーを立ち上げる対象。
　・エンドポイント定義（/api/transcribeや/ui）。

・asr.py
　・音声処理ロジックを分離
　・ffmpegで16kHz/mono変換→faster-wisperで推論。
　・main.pyに書かずに切り出すことで、責務を分けて読みやすく保守しやすくしている。

→「Webサーバー処理」と「音声認識ロジック」を分離することで、再利用性都見通しがよくなる。

2, web/ ディレクトリ
・性的ファイル置き場。
・index.htmlは、「簡易UI」　＝　ブラウザから試すための最低限装備。
・FastAPIは、StaticFilesを使ってここを/uiで配信する設定になってる。
→将来的にReactやNext.jsなどのフロントを差し替える時も、このディレクトリだけ変えれば済む。

３、ルート直下
・.venv/ （仮想環境）は、無視される想定（.gitignore対象）。
・requirements.txtを置いて依存管理している