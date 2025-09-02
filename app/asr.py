import os, subprocess
from pathlib import Path
from typing import List, Dict

from faster_whisper import WhisperModel

MODEL_NAME = os.getenv("WHISPER_MODEL", "medium")
_model = None

def _detect_device() -> str:
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"

def _load_model() -> WhisperModel:
    global _model
    if _model is None:
        device = _detect_device()
        compute_type = "float16" if device == "cuda" else "int8_float16"
        _model = WhisperModel(MODEL_NAME, device=device, compute_type=compute_type)
    return _model

def _ffmpeg_to_wav16k(src: Path, dst: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "16000", "-f", "wav", str(dst)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def transcribe_path(src_path: Path, language: str = "ja") -> Dict:
    tmp_wav = src_path.with_suffix(".16k.wav")
    _ffmpeg_to_wav16k(src_path, tmp_wav)

    model = _load_model()
    # 最小構成なのでVADはオフ（追加依存を避ける）。十分実用。
    segments, info = model.transcribe(str(tmp_wav), beam_size=5, vad_filter=False, language=language)

    segs = []
    for seg in segments:
        segs.append({
            "start": float(seg.start or 0),
            "end": float(seg.end or 0),
            "text": seg.text.strip()
        })
    full_text = "".join(s["text"] for s in segs).strip()
    try:
        tmp_wav.unlink()
    except Exception:
        pass
    return {"language": info.language, "text": full_text, "segments": segs}

def _ts(s: float) -> str:
    h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{int(sec):02d},{int((sec % 1) * 1000):03d}"

def to_srt(segments: List[Dict]) -> str:
    lines = []
    for i, seg in enumerate(segments, start=1):
        lines.append(str(i))
        lines.append(f"{_ts(seg['start'])} --> {_ts(seg['end'])}")
        lines.append(seg['text'])
        lines.append("")
    return "\n".join(lines)
