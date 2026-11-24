from fastapi import FastAPI, Request, BackgroundTasks
from app.agent import reply
from app.wpp import send_text, send_voice, transcribe

app = FastAPI(title="CallMitra")

async def handle(phone: str, msg_id: str, kind: str, body: str):
    try:
        voice_in = kind in ("ptt", "audio")
        text = await transcribe(msg_id) if voice_in else body
        answer = await reply(phone, text)
        await (send_voice(phone, answer) if voice_in else send_text(phone, answer))
    except Exception:
        await send_text(phone, "Sorry, something went wrong. Please try again in a moment.")

@app.post("/webhook")
async def webhook(req: Request, bg: BackgroundTasks):
    d = await req.json()
    if d.get("event") != "onmessage" or d.get("fromMe") or d.get("isGroupMsg"):
        return {"ok": True}
    phone = d["from"].split("@")[0]
    bg.add_task(handle, phone, d.get("id", ""), d.get("type", "chat"), d.get("body", ""))
    return {"ok": True}

@app.get("/health")
def health(): return {"status": "ok"}
