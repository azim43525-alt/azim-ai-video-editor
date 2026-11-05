import os, uuid, shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from editor import make_video

BASE = Path(__file__).parent
WORK = BASE / "work"
WORK.mkdir(exist_ok=True)

app = FastAPI(title="AI Video Editor")
templates = Jinja2Templates(directory=str(BASE / "templates"))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create")
async def create(
    script: str = Form(...),
    voice: UploadFile = File(...),
    footage: UploadFile = File(...)
):
    if not script.strip():
        raise HTTPException(400, "Please add a script.")
    job = uuid.uuid4().hex[:10]
    folder = WORK / job
    folder.mkdir()
    voice_path = folder / (Path(voice.filename or "voice.mp3").name)
    video_path = folder / (Path(footage.filename or "footage.mp4").name)
    with voice_path.open("wb") as f:
        shutil.copyfileobj(voice.file, f)
    with video_path.open("wb") as f:
        shutil.copyfileobj(footage.file, f)
    output = folder / "final_video.mp4"
    try:
        result = make_video(script, voice_path, video_path, output, folder)
    except Exception as e:
        shutil.rmtree(folder, ignore_errors=True)
        raise HTTPException(500, f"Render failed: {str(e)[:500]}")
    return {"job": job, "download": f"/download/{job}", "editor_notes": result}

@app.get("/download/{job}")
async def download(job: str):
    path = WORK / job / "final_video.mp4"
    if not path.exists():
        raise HTTPException(404, "Video not found.")
    return FileResponse(path, media_type="video/mp4", filename="edited_video.mp4")
