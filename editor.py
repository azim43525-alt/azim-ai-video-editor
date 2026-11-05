import os, json, subprocess
from pathlib import Path
from faster_whisper import WhisperModel
from claude_editor import create_edit_notes

def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-2500:])
    return p.stdout

def make_video(script, voice, footage, output, folder):
    # Transcribe the supplied voice and get word/segment timing.
    model_name = os.getenv("WHISPER_MODEL", "base")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(voice), word_timestamps=True, vad_filter=True)
    segments = list(segments)
    if not segments:
        raise RuntimeError("No speech was detected in the voice file.")

    # Build an SRT subtitle file with timestamps aligned to the uploaded voice.
    srt = folder / "captions.srt"
    def stamp(seconds):
        ms = int(seconds * 1000)
        h, ms = divmod(ms, 3600000)
        m, ms = divmod(ms, 60000)
        s, ms = divmod(ms, 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"
    with srt.open("w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            text = seg.text.strip()
            f.write(f"{i}\n{stamp(seg.start)} --> {stamp(seg.end)}\n{text}\n\n")

    # Claude is optional: it returns an editorial plan, not the rendered pixels.
    notes = create_edit_notes(script)
    voice_duration = float(run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                                str(voice)]).strip())
    # Scale supplied footage to vertical 9:16, loop if needed, lay voice over it,
    # and burn synchronized captions. Captions are phrase/segment timed.
    escaped = str(srt).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,"
          "crop=1080:1920,setsar=1,"
          f"subtitles='{escaped}':force_style='FontName=DejaVu Sans,FontSize=18,"
          "Bold=1,Outline=2,Shadow=1,Alignment=2,MarginV=150'")
    run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(footage), "-i", str(voice),
         "-t", str(voice_duration), "-vf", vf, "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
         str(output)])
    return notes
