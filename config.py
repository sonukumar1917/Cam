import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = ("7662960174:AAFq2lgr_P9LP2x6IYOCK9ECwXGymPvRJ74")
ADMIN_IDS = [int(i.strip()) for i in os.getenv("ADMIN_IDS", "7655738256,").split(",")]
force_join_str = os.getenv("FORCE_JOIN_CHANNELS", "")
FORCE_JOIN_CHANNELS = [ch.strip() for ch in force_join_str.split(",") if ch.strip()]
IP_API_URL = "https://abbas-apis.vercel.app/api/ip?ip="

# Supabase Credentials
SUPABASE_URL = "https://eyymkvqberjybsygvjkv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV5eW1rdnFiZXJqeWJzeWd2amt2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDAxNzAzMywiZXhwIjoyMDg1NTkzMDMzfQ.GpPjAhwG_oNNIFLG_cRA0UU8G5Z7ypfTH_t-AXPyW7c"

# Server Settings
PORT = int(os.getenv("PORT", 8888))
BASE_URL = os.getenv("https://cam-3-ut2r.onrender.com") # Example: https://your-app.onrender.com
NGROK_AUTH_TOKEN = os.getenv("ngrok config add-authtoken 39LalZppmN2SwlonfsCxP1FAN0C_shLK6SiJyd7MBHMmb1ao")
