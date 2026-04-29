from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database
from config import ADMIN_IDS
from emojis import Emojis

router = Router()

class AdminForm(StatesGroup):
    waiting_for_broadcast = State()

@router.message(Command("admin"))
async def admin_panel(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.row(types.InlineKeyboardButton(text="Get Stats", callback_data="admin_stats", icon_custom_emoji_id=Emojis.get_id(Emojis.STATS)))
    kb.row(types.InlineKeyboardButton(text="Broadcast", callback_data="admin_broadcast", icon_custom_emoji_id=Emojis.get_id(Emojis.BROADCAST)))
    kb.row(types.InlineKeyboardButton(text="Give Credit", callback_data="admin_give_credit", icon_custom_emoji_id=Emojis.get_id(Emojis.TICKET)))
    
    admin_ui = (
        f"{Emojis.TOOLS} <b><u>Admin Control Panel</u></b>\n\n"
        f"Select an action below to manage the system:\n"
        f"____________________\n"
    )
    await message.answer(admin_ui, reply_markup=kb.as_markup(), parse_mode="HTML")

@router.callback_query(F.data == "admin_stats")
async def admin_stats_cb(call: types.CallbackQuery):
    if call.from_user.id not in ADMIN_IDS: return
    stats = await database.get_stats()
    await call.message.edit_text(f"{Emojis.STATS} <b>Bot Statistics</b>\n\nTotal Users: <code>{stats['total_users']}</code>", parse_mode="HTML")

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_cb(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS: return
    await call.message.edit_text(f"{Emojis.BROADCAST} <b>Enter the message to broadcast:</b>", parse_mode="HTML")
    await state.set_state(AdminForm.waiting_for_broadcast)

@router.callback_query(F.data == "admin_give_credit")
async def admin_give_credit_cb(call: types.CallbackQuery):
    if call.from_user.id not in ADMIN_IDS: return
    await call.message.edit_text(f"{Emojis.CROSS} Usage: <code>/give_credit [user_id] [amount]</code>", parse_mode="HTML")

@router.message(Command("stats"))
async def stats_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    stats = await database.get_stats()
    text = (
        f"{Emojis.STATS} <b>Bot Statistics</b>\n"
        "____________________\n\n"
        f"{Emojis.USERS} Total Users: <code>{stats['total_users']}</code>\n"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("broadcast"))
async def broadcast_cmd(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    await message.answer(f"{Emojis.BROADCAST} <b>Enter the message to broadcast to all users:</b>", parse_mode="HTML")
    await state.set_state(AdminForm.waiting_for_broadcast)

@router.message(AdminForm.waiting_for_broadcast)
async def broadcast_process(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()
    users = await database.get_all_users()
    count = 0
    
    await message.answer(f"{Emojis.ROCKET} Starting broadcast to {len(users)} users...", parse_mode="HTML")
    
    for user_id in users:
        try:
            await bot.send_message(user_id, message.html_text, parse_mode="HTML")
            count += 1
        except Exception:
            continue
            
    await message.answer(f"{Emojis.CHECK} Broadcast completed! Sent to {count} users.", parse_mode="HTML")

@router.message(Command("give_credit"))
async def give_credit_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer(f"{Emojis.CROSS} Usage: /give_credit [user_id] [amount]", parse_mode="HTML")
        return
    
    try:
        user_id = int(args[1])
        amount = int(args[2])
        await database.add_credits(user_id, amount)
        await message.answer(f"{Emojis.CHECK} Successfully added {amount} credits to user <code>{user_id}</code>", parse_mode="HTML")
    except ValueError:
        await message.answer(f"{Emojis.CROSS} Invalid User ID or Amount. Must be numbers.", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"{Emojis.CROSS} Error: <code>{str(e)}</code>", parse_mode="HTML")

@router.message(Command("set_tutorial"))
async def set_tutorial_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    # Check if a video is attached or replied to
    video_id = None
    if message.video:
        video_id = message.video.file_id
    elif message.reply_to_message and message.reply_to_message.video:
        video_id = message.reply_to_message.video.file_id
    
    if not video_id:
        await message.reply(f"{Emojis.CROSS} Please attach a video or reply to a video with /set_tutorial", parse_mode="HTML")
        return

    await database.set_setting("tutorial_video", video_id)
    await message.reply(f"{Emojis.CHECK} Tutorial video updated successfully!", parse_mode="HTML")

@router.message(Command("set_bots"))
async def set_bots_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    # Use html_text to preserve premium emojis/tags
    # Need to remove the command prefix "/set_bots" from the HTML
    raw_html = message.html_text
    
    # Precise stripping of command
    if raw_html.startswith("/set_bots"):
        text = raw_html[len("/set_bots"):].strip()
    else:
        text = raw_html.strip()

    # Also check reply
    if not text and message.reply_to_message:
        # Use html_text of the replied message
        text = message.reply_to_message.html_text

    if not text:
        await message.reply(f"{Emojis.CROSS} Usage: /set_bots <text> (or reply to a text message)", parse_mode="HTML")
        return

    await database.set_setting("bots_list", text)
    await message.reply(f"{Emojis.CHECK} Bots list updated successfully!", parse_mode="HTML")
