import streamlit as st
import tempfile, subprocess, os, json
from openai import OpenAI

st.set_page_config(page_title="Marathi Caption AI", page_icon="🎬", layout="centered")
st.markdown("<style> .stApp {background: linear-gradient(135deg,#10121b,#251533);} h1,h2,h3,p {color:#f4f4f7;} </style>", unsafe_allow_html=True)
st.title("🎬 Marathi Caption AI")
st.caption("Video मधून subtitles तयार करा • मराठी / English")

api_key = st.text_input("OpenAI API Key", type="password", help="तुमचा API key या session मध्येच वापरला जातो.")
video = st.file_uploader("व्हिडिओ अपलोड करा", type=["mp4", "mov", "m4v", "webm"])
lang = st.radio("कॅप्शनची भाषा", ["मराठी", "English", "Original transcript"], horizontal=True)
style = st.selectbox("Caption style", ["Simple", "Cinematic", "Reels / punchy", "Clean professional"])

if st.button("✨ Generate captions", type="primary", disabled=not (api_key and video)):
    client = OpenAI(api_key=api_key)
    with st.spinner("Audio काढतो आणि captions तयार करतो..."):
        try:
            with tempfile.TemporaryDirectory() as tmp:
                in_path = os.path.join(tmp, video.name)
                audio_path = os.path.join(tmp, "audio.mp3")
                with open(in_path, "wb") as f: f.write(video.getbuffer())
                # Extract audio using FFmpeg installed on the cloud host
                proc = subprocess.run(["ffmpeg", "-y", "-i", in_path, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", audio_path], capture_output=True)
                if proc.returncode != 0:
                    st.error("Audio extract करता आला नाही. Video format तपासा.")
                    st.stop()
                with open(audio_path, "rb") as audio:
                    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio, response_format="verbose_json", timestamp_granularities=["segment"])
                segments = getattr(transcript, "segments", []) or []
                original_text = transcript.text
                if lang == "Original transcript":
                    result_text = original_text
                    translated_segments = []
                else:
                    target = "Marathi" if lang == "मराठी" else "English"
                    style_hint = {"Simple":"natural, easy to read", "Cinematic":"cinematic, expressive but faithful", "Reels / punchy":"short, punchy social-video style without changing meaning", "Clean professional":"clean professional subtitles"}[style]
                    prompt = f"Translate this video transcript into {target}. Style: {style_hint}. Preserve meaning, do not add information. Return only the translated text.\n\nTranscript:\n{original_text}"
                    translated = client.responses.create(model="gpt-4o-mini", input=prompt)
                    result_text = translated.output_text.strip()
                    translated_segments = []
                st.subheader("Transcript")
                st.text_area("Edit caption text", value=result_text, height=240, key="caption_edit")
                st.download_button("⬇️ Download TXT", data=result_text, file_name="captions.txt", mime="text/plain")
                # Build timed SRT using original segments; translation is paragraph-level so timing may be approximate.
                if segments:
                    srt_parts = []
                    for i, seg in enumerate(segments, 1):
                        start = float(seg.get("start", 0)); end = float(seg.get("end", start+2))
                        txt = seg.get("text", "").strip()
                        srt_parts.append(f"{i}\n{fmt_time(start)} --> {fmt_time(end)}\n{txt}\n")
                    srt = "\n".join(srt_parts)
                    st.download_button("⬇️ Download SRT (original language)", data=srt, file_name="captions_original.srt", mime="text/plain")
                st.info("टीप: translated text सध्या पूर्ण transcript म्हणून तयार होते. SRT टाइमिंग original भाषेत दिले आहे.")
        except Exception as e:
            st.error(f"Error: {e}")


def fmt_time(sec):
    ms = int(round(sec * 1000)); hours = ms // 3600000; ms %= 3600000
    mins = ms // 60000; ms %= 60000; secs = ms // 1000; ms %= 1000
    return f"{hours:02}:{mins:02}:{secs:02},{ms:03}"
