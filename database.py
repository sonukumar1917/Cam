import asyncio
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
# Ensure your config.py has correctly loaded SUPABASE_URL and SUPABASE_KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def run_sync(func, *args):
    """Run a synchronous function in a thread to avoid blocking the event loop."""
    return await asyncio.to_thread(func, *args)

async def init_db():
    # Database initialization is handled via Supabase Dashboard.
    pass

async def add_user(user_id, username, invited_by=None):
    # Check if user exists
    def _check():
        return supabase.table("bot_users").select("*").eq("user_id", user_id).execute()
    
    existing = await run_sync(_check)
    
    if not existing.data:
        if invited_by == user_id:
            invited_by = None
            
        data = {
            "user_id": user_id,
            "username": username or  "Unknown",
            "invited_by": invited_by,
            "credits": 1,
            "invites": 0
        }
        
        def _insert():
            supabase.table("bot_users").insert(data).execute()
        await run_sync(_insert)
        
        if invited_by:
            def _update_inviter():
                # Update inviter's stats
                inviter = supabase.table("bot_users").select("invites, credits").eq("user_id", invited_by).execute()
                if inviter.data:
                    new_invites = inviter.data[0]['invites'] + 1
                    new_credits = inviter.data[0]['credits'] + 1
                    supabase.table("bot_users").update({"invites": new_invites, "credits": new_credits}).eq("user_id", invited_by).execute()
            await run_sync(_update_inviter)
        return True
    return False

async def set_language(user_id, language):
    def _update():
        supabase.table("bot_users").update({"language": language}).eq("user_id", user_id).execute()
    await run_sync(_update)

async def get_user_data(user_id):
    def _select():
        return supabase.table("bot_users").select("credits, invites, language").eq("user_id", user_id).execute()
    res = await run_sync(_select)
    if res.data:
        return res.data[0]
    return None

async def get_all_users():
    def _select():
        return supabase.table("bot_users").select("user_id").execute()
    res = await run_sync(_select)
    return [row['user_id'] for row in res.data]

async def get_stats():
    def _select():
        return supabase.table("bot_users").select("*", count="exact").execute()
    res = await run_sync(_select)
    return {"total_users": res.count or 0}

async def add_credits(user_id, amount):
    def _process():
        user = supabase.table("bot_users").select("credits").eq("user_id", user_id).execute()
        if user.data:
            new_credits = user.data[0]['credits'] + amount
            supabase.table("bot_users").update({"credits": new_credits}).eq("user_id", user_id).execute()
    await run_sync(_process)

async def deduct_credits(user_id, amount):
    def _process():
        user = supabase.table("bot_users").select("credits").eq("user_id", user_id).execute()
        if user.data:
            current = user.data[0]['credits']
            if current >= amount:
                new_credits = current - amount
                supabase.table("bot_users").update({"credits": new_credits}).eq("user_id", user_id).execute()
                return True
            return False
        return False
    return await run_sync(_process)

# In-memory fallback for settings if table is missing
_settings_fallback = {}

async def set_setting(key, value):
    def _upsert():
        # Check if exists
        try:
            data = supabase.table("bot_settings").select("*").eq("key", key).execute()
            if data.data:
                supabase.table("bot_settings").update({"value": value}).eq("key", key).execute()
            else:
                supabase.table("bot_settings").insert({"key": key, "value": value}).execute()
        except Exception as e:
            # Fallback if table doesn't exist
            print(f"⚠️ Database Error (Settings): {e}. Using in-memory fallback.")
            _settings_fallback[key] = value

    await run_sync(_upsert)

async def get_setting(key):
    def _select():
        try:
            return supabase.table("bot_settings").select("value").eq("key", key).execute()
        except Exception:
            return None
            
    res = await run_sync(_select)
    if res and res.data:
        return res.data[0]['value']
    
    # Return from fallback if DB failed
    return _settings_fallback.get(key)
