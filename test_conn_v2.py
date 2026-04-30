import socket
import requests

def test(url):
    print(f"Testing {url}...")
    try:
        ip = socket.gethostbyname(url)
        print(f"✅ Resolved to {ip}")
    except Exception as e:
        print(f"❌ DNS Failed: {e}")

test("google.com")
test("uiahjgahaoffswfzeyxt.supabase.co")
test("api.supabase.com")
