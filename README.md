# CallMitra: WhatsApp voice and text appointment agent

Clients message or send a voice note on WhatsApp. The agent (LangGraph + Groq) understands
English/Hindi/Hinglish, checks free slots, books, lists and cancels appointments, and answers
in text or a voice note. Based on the pattern of lucasboscatti/Whatsapp-Langgraph-Agent-Integration.

## Run
1. `cp .env.example .env` and fill in the keys. Set BUSINESS_NAME, SERVICES, hours for your niche.
2. Run WPPConnect Server (github.com/wppconnect-team/wppconnect-server), start a session, scan the QR code,
   and set its webhook to `http://<your-host>:8000/webhook`.
3. `pip install -r requirements.txt && uvicorn main:app --port 8000`
4. Message the connected WhatsApp number to test.

## Notes
- Bookings are stored in SQLite (`appointments.db`). Conversation memory is in-process; switch to
  the Postgres checkpointer for production and multiple workers.
- Verify the WPPConnect media-download endpoint in `app/wpp.py` against your server version.
- WPPConnect is unofficial. For a commercial SaaS use the official WhatsApp Cloud API.
- For real phone calls, add Twilio/Exotel and reuse `app/agent.py` unchanged.
# Ai-voice-assistant-callmitra-
