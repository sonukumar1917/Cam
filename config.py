import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7662960174:AAHQgyZvi-qNRmWhPeaXRM9xhSIv7NoLgng")
ADMIN_IDS = [int(i) for i in os.getenv("7655738256").split(",")]
FORCE_JOIN_CHANNELS = os.getenv("FORCE_JOIN_CHANNELS").split(",")
IP_API_URL = "https://abbas-apis.vercel.app/api/ip?ip="

# Supabase Credentials
SUPABASE_URL = os.getenv("https://cam-2-vo2q.onrender.com")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Server Settings
PORT = int(os.getenv("PORT", 8080))
BASE_URL = os.getenv("https://cam-2-vo2q.onrender.com") # Example: https://your-app.onrender.com
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
