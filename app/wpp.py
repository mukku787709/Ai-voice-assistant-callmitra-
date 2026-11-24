import base64, io, httpx
from groq import Groq
from gtts import gTTS
from .config import *

H = {"Authorization": f"Bearer {WPP_TOKEN}"}
API = f"{WPP_URL}/api/{WPP_SESSION}"
groq = Groq(api_key=GROQ_API_KEY)

async def send_text(phone, text):
    async with httpx.AsyncClient() as c:
        await c.post(f"{API}/send-message", headers=H, json={"phone": phone, "message": text, "isGroup": False})

async def send_voice(phone, text):
    buf = io.BytesIO(); gTTS(text, lang=VOICE_LANG).write_to_fp(buf)
    b64 = "data:audio/mpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    async with httpx.AsyncClient() as c:
        await c.post(f"{API}/send-voice-base64", headers=H, json={"phone": phone, "base64Ptt": b64, "isGroup": False})

async def transcribe(message_id: str) -> str:
    # Verify this endpoint against your wppconnect-server version.
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{API}/get-media-by-message/{message_id}", headers=H)
    audio = base64.b64decode(r.json()["base64"])
    t = groq.audio.transcriptions.create(file=("voice.ogg", audio), model="whisper-large-v3")
    return t.text
