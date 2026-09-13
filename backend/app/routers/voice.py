"""
Voice Router — Whisper Local Free — From free-claude-code 54.8k stars — Level 1 Polished $0
Whisper local free speech-to-text $0 — 100% margin — voice notes via free-claude-code integration
"""
from fastapi import APIRouter, UploadFile, File
from typing import Dict
import os

router = APIRouter(prefix="/api/voice", tags=["voice-whisper"])

@router.get("/")
async def voice_info():
    return {
        "voice": "Voice — Whisper Local Free — From free-claude-code 54.8k stars — $0 — 100% margin",
        "reality": "REAL_WITH_MOCK_FALLBACK - Real Whisper when installed, mock when not — $0 local free",
        "repo": "https://github.com/Alishahryar1/free-claude-code — 54.8k stars — voice Whisper local/NVIDIA NIM",
        "providers": {
            "whisper_local": {
                "name": "Whisper Local",
                "cost": "$0 local free",
                "margin": "100%",
                "models": ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
                "languages": "99 languages — auto-detect",
                "how_to_install": "pip install openai-whisper + whisper --model base --language auto audio.mp3 — or pip install faster-whisper — $0",
                "api": "POST /api/voice/transcribe — upload audio file — returns transcription",
                "use_case": "Voice notes for agents — content-creator agent — support-agent — client voice messages — $0 — 100% margin"
            },
            "whisper_nvidia_nim": {
                "name": "Whisper NVIDIA NIM",
                "cost": "$0 free tier",
                "how_to_get": "https://build.nvidia.com/ — NVIDIA NIM Whisper — nvapi-... — 40 req/min free",
                "api": "NVIDIA NIM API — audio transcription"
            },
            "faster_whisper": {
                "name": "Faster Whisper",
                "cost": "$0 local free",
                "how_to_install": "pip install faster-whisper — 4x faster than openai-whisper — CTranslate2 — $0",
                "recommended": True
            }
        },
        "integration": {
            "content_creator": "Voice notes for content-creator agent — transcribe client voice briefs — $0",
            "support_agent": "Transcribe support calls — Otter.ai $16/mo alternative $0 via Whisper local free",
            "researcher": "Transcribe research interviews — $0",
            "agency": "Client voice messages → text → tasks — $0"
        },
        "cost_comparison": {
            "otter_ai": "$16/mo — meeting transcription",
            "whisper_local": "$0 local free — 100% margin — needs local CPU/GPU — tiny 39M base 74M small 244M medium 769M large 1550M — RAM 1GB-10GB",
            "elevenlabs_stt": "$0.18/hour",
            "whisper_api_openai": "$0.006/min $0.36/hour"
        },
        "endpoints": {
            "info": "GET /api/voice/ — this",
            "transcribe": "POST /api/voice/transcribe — upload audio file (mp3/wav/m4a/ogg) — returns transcription — real Whisper when installed mock when not",
            "transcribe_mock": "POST /api/voice/transcribe — mock always works — $0 — for testing"
        },
        "docs": "docs/FREE_LLM_PROVIDERS.md — Whisper section — from free-claude-code voice Whisper local/NVIDIA NIM"
    }

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), model: str = "base", language: str = "auto"):
    """
    Transcribe audio file via Whisper local free — $0 — 100% margin
    Real Whisper when openai-whisper or faster-whisper installed, mock when not
    """
    try:
        # Try real Whisper local
        # First try faster-whisper (recommended, 4x faster)
        try:
            from faster_whisper import WhisperModel
            import tempfile
            
            # Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".mp3") as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name
            
            # Load model — base is good balance — 74M — needs ~1GB RAM
            whisper_model = WhisperModel(model, device="cpu", compute_type="int8")  # int8 for CPU efficiency
            
            # Transcribe
            segments, info = whisper_model.transcribe(tmp_path, language=None if language == "auto" else language)
            
            transcription = " ".join([segment.text for segment in segments])
            
            # Cleanup
            os.unlink(tmp_path)
            
            return {
                "transcription": transcription,
                "language": info.language,
                "language_probability": info.language_probability,
                "duration": info.duration,
                "model": model,
                "provider": "faster_whisper",
                "real": True,
                "cost": 0.0,
                "margin": "100%",
                "file": file.filename,
                "size": len(content)
            }
        except ImportError:
            # Try openai-whisper
            try:
                import whisper
                import tempfile
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1] or ".mp3") as tmp:
                    content = await file.read()
                    tmp.write(content)
                    tmp_path = tmp.name
                
                whisper_model = whisper.load_model(model)
                result = whisper_model.transcribe(tmp_path, language=None if language == "auto" else language)
                
                os.unlink(tmp_path)
                
                return {
                    "transcription": result["text"],
                    "language": result["language"],
                    "model": model,
                    "provider": "openai_whisper",
                    "real": True,
                    "cost": 0.0,
                    "margin": "100%",
                    "file": file.filename,
                    "size": len(content),
                    "segments": result.get("segments", [])[:3]  # First 3 segments
                }
            except ImportError:
                # Mock fallback — Whisper not installed
                content = await file.read()
                return {
                    "transcription": f"Mock transcription for {file.filename} — Whisper not installed — Install via pip install openai-whisper or pip install faster-whisper — $0 local free — 100% margin — File size {len(content)} bytes — Model {model} — Language {language} — Real transcription would be here when Whisper installed — For testing, this mock always works",
                    "language": language if language != "auto" else "en",
                    "language_probability": 0.99,
                    "duration": len(content) / 16000,  # Mock duration
                    "model": model,
                    "provider": "mock",
                    "real": False,
                    "mock": True,
                    "cost": 0.0,
                    "margin": "100%",
                    "file": file.filename,
                    "size": len(content),
                    "how_to_install_real": [
                        "pip install openai-whisper — openai-whisper — tiny 39M base 74M small 244M medium 769M large 1550M — $0 — needs 1GB-10GB RAM",
                        "pip install faster-whisper — faster-whisper — 4x faster — CTranslate2 — recommended — $0",
                        "NVIDIA NIM Whisper — https://build.nvidia.com/ — nvapi-... — 40 req/min free — $0"
                    ],
                    "note": "Real Whisper when installed — mock when not — $0 local free — 100% margin — from free-claude-code voice Whisper local/NVIDIA NIM"
                }
    except Exception as e:
        return {
            "transcription": f"Error transcribing {file.filename}: {e} — Mock fallback",
            "error": str(e),
            "provider": "mock",
            "real": False,
            "mock": True,
            "cost": 0.0,
            "file": file.filename
        }
