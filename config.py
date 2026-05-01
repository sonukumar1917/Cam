import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = ("7662960174:AAHQgyZvi-qNRmWhPeaXRM9xhSIv7NoLgng")
ADMIN_IDS = [int(i.strip()) for i in os.getenv("ADMIN_IDS", "7655738256,").split(",")]
force_join_str = os.getenv("FORCE_JOIN_CHANNELS", "")
FORCE_JOIN_CHANNELS = [ch.strip() for ch in force_join_str.split(",") if ch.strip()]
IP_API_URL = "https://abbas-apis.vercel.app/api/ip?ip="

# Supabase Credentials
SUPABASE_URL = "https://eyymkvqberjybsygvjkv.supabase.co"
SUPABASE_KEY = "sb_publishable_DmMS3dTp3T9jY6t8KzZEig_avZjn0QZ"

# Server Settings
PORT = int(os.getenv("PORT", 8080))
BASE_URL = os.getenv("https://cam-3-ut2r.onrender.com") # Example: https://your-app.onrender.com
NGROK_AUTH_TOKEN = os.getenv("ngrok config add-authtoken 39LalZppmN2SwlonfsCxP1FAN0C_shLK6SiJyd7MBHMmb1ao")
