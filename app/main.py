from pathlib import Path
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app.asr import transcribe_path, to_srt

app = FastAPI(title="Whisper Minimal API")

# フロント配信用（/ で index.html を返す）
app.mount("/", StaticFiles(directory="web", html=True), name="web")

@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = "ja", srt: bool = False):
    # 最小バリデーション
    if not file.filename:
        raise HTTPException(400, "no filename")

    # 一時保存
    try:
        suffix = Path(file.filename).suffix or ".bin"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = Path(tmp.name)
            tmp.write(await file.read())
    except Exception as e:
        raise HTTPException(500, f"failed to store upload: {e}")

    try:
        result = transcribe_path(tmp_path, language=language)
    except Exception as e:
        raise HTTPException(500, f"transcription failed: {e}")
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

    # srt=1 ならSRT返す（ダウンロードしやすい）
    if str(srt).lower() in {"1", "true", "yes"}:
        srt_text = to_srt(result["segments"])
        return PlainTextResponse(srt_text, media_type="text/plain; charset=utf-8")

    return JSONResponse(result)
