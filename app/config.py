import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
WPP_URL = os.getenv("WPP_URL", "http://localhost:21465")
WPP_SESSION = os.getenv("WPP_SESSION", "callmitra")
WPP_TOKEN = os.getenv("WPP_TOKEN", "")
BUSINESS = os.getenv("BUSINESS_NAME", "My Business")
AGENT = os.getenv("AGENT_NAME", "Aria")
SERVICES = [s.strip() for s in os.getenv("SERVICES", "Consultation").split(",")]
OPEN_HOUR = int(os.getenv("OPEN_HOUR", 9))
CLOSE_HOUR = int(os.getenv("CLOSE_HOUR", 17))
VOICE_LANG = os.getenv("VOICE_LANG", "en")  # "hi" for Hindi voice replies
