import socket
import requests

url = "uiabjgahaotfswfzeyxf.supabase.co"
print(f"Testing DNS for {url}...")
try:
    ip = socket.gethostbyname(url)
    print(f"✅ Resolved to {ip}")
except Exception as e:
    print(f"❌ DNS Resolution Failed: {e}")

print("\nTesting HTTPS connection...")
try:
    res = requests.get(f"https://{url}", timeout=10)
    print(f"✅ Response Code: {res.status_code}")
except Exception as e:
    print(f"❌ HTTPS Connection Failed: {e}")
