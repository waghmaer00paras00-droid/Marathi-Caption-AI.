# Marathi Caption AI 🎬

Streamlit app starter for video transcript/caption generation using OpenAI API.

## Features
- Upload MP4/MOV/M4V/WEBM
- Extract audio with FFmpeg
- Transcribe with Whisper
- Translate transcript into Marathi or English
- Download TXT captions and original-language SRT

## Run locally
1. Install Python 3.10+
2. Install FFmpeg and ensure `ffmpeg` is on PATH
3. `pip install -r requirements.txt`
4. `streamlit run app.py`
5. Enter your OpenAI API key in the app

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository and upload all files in this folder.
2. Go to https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select the repository, branch, and `app.py`.
4. Deploy. FFmpeg is installed from `packages.txt`.
5. Keep your API key private. Do not commit it to GitHub.


## Notes / limitations
- This is a starter demo, not a finished commercial app.
- Translated captions are currently generated as a full transcript; SRT timing download is the original transcript language only.
- API usage can cost money depending on usage and model rates. Set usage limits in your API account.
