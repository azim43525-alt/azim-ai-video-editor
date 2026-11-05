# AZIM AI VIDEO EDITOR — Android Starter Kit

## What is included
- `CLAUDE_PROJECT_INSTRUCTIONS.md`: upload this into a Claude Project as project knowledge.
- `app.py`: web app and upload/download routes.
- `editor.py`: voice transcription, timed captions, FFmpeg rendering.
- `claude_editor.py`: optional Claude API edit-plan integration.
- `templates/index.html`: mobile-friendly editor page.
- `requirements.txt`, `Dockerfile`, `render.yaml`: deployment files.

## Current capabilities and limitations
This is a starter MVP, not a complete CapCut replacement. It accepts a script, voice recording, and one video clip; uses Whisper to create segment-timed subtitles; loops/crops the supplied clip to vertical 9:16; and exports an MP4. If configured, Claude returns an editing plan. It does NOT yet generate AI footage, automatically select multiple scene clips, create TTS audio, or provide advanced animated captions/transitions.

## Android deployment outline
1. Extract this ZIP.
2. Create a GitHub repository named `azim-ai-video-editor`.
3. Upload all files and preserve the `templates/index.html` folder structure.
4. Sign in to Render, connect GitHub, choose New > Blueprint, and select the repository.
5. Wait for deployment. Open the URL supplied by Render in Android Chrome.
6. Chrome menu > Add to Home screen can add a shortcut.

## Connect Claude
1. Create a Claude Project named `AZIM AI VIDEO EDITOR`.
2. Upload `CLAUDE_PROJECT_INSTRUCTIONS.md` to Project Knowledge, or paste its contents into Project Instructions.
3. For API integration, create an API key in Anthropic Console and add it in Render Environment Variables as `ANTHROPIC_API_KEY`.
4. Never put the API key in HTML, JavaScript, Project Knowledge, or a public GitHub repository.

## Important
- Hosting and API usage may cost money. Payment setup should be handled with a parent/guardian.
- This demo stores uploads in `work/`; it does not automatically delete them. Do not use it as a public service until authentication, upload limits, rate limits, and automatic file deletion are added.
- Use only media you own or have permission to use.
- Render needs enough memory/CPU for Whisper and FFmpeg. The default Whisper model is `base`; set `WHISPER_MODEL=tiny` in Render Environment to reduce memory use.
- Local run requires Python 3.11 and FFmpeg: `pip install -r requirements.txt`, then `uvicorn app:app --reload`.
