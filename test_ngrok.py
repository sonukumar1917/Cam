import os
from pyngrok import ngrok
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("NGROK_AUTH_TOKEN")
port = int(os.getenv("PORT", 8000))

print(f"Testing ngrok with token: {token[:5]}...{token[-5:]} on port {port}")
try:
    ngrok.set_auth_token(token)
    tunnel = ngrok.connect(port)
    print(f"✅ Success! URL: {tunnel.public_url}")
    ngrok.disconnect(tunnel.public_url)
except Exception as e:
    print(f"❌ Failed: {e}")
