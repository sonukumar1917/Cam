import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = ("7662960174:AAHQgyZvi-qNRmWhPeaXRM9xhSIv7NoLgng")
ADMIN_IDS = [int(i.strip()) for i in os.getenv("ADMIN_IDS", "7655738256,").split(",")]
FORCE_JOIN_CHANNELS = os.getenv("FORCE_JOIN_CHANNELS").split(",")
IP_API_URL = ""

# Supabase Credentials
SUPABASE_URL = os.getenv("https://eyymkvqberjybsygvjkv.supabase.co")
SUPABASE_KEY = os.getenv("sb_publishable_DmMS3dTp3T9jY6t8KzZEig_avZjn0QZ")

# Server Settings
PORT = int(os.getenv("PORT", 8080))
BASE_URL = os.getenv("https://cam-3-ut2r.onrender.com") # Example: https://your-app.onrender.com
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
