"""
Start handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import UserService
from utils.formatter import PremiumFormatter
from db.session import get_db

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    async for session in get_db():
        user_service = UserService(session)
        db_user = await user_service.get_or_create_user(
            telegram_id=user.id,
            first_name=user.first_name,
            username=user.username,
            last_name=user.last_name
        )
        
        if context.args and context.args[0].startswith("ref_"):
            ref_code = context.args[0].replace("ref_", "")
            result = await user_service.process_referral(user.id, ref_code)
            if result and "success" in result:
                await update.message.reply_text(
                    f"🎉 *Referral Success!* You got {result['coins_awarded']} coins! 🪙",
                    parse_mode='Markdown'
                )
        
        keyboard = [
            [InlineKeyboardButton("🔍 Search", callback_data="search_menu"),
             InlineKeyboardButton("👤 Profile", callback_data="profile_menu")],
            [InlineKeyboardButton("💰 Plans", callback_data="plans_menu"),
             InlineKeyboardButton("🎁 Refer", callback_data="refer_menu")],
            [InlineKeyboardButton("📜 History", callback_data="history_menu"),
             InlineKeyboardButton("🆘 Support", callback_data="support_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        premium_status = "✅" if db_user.is_premium else "❌"
        welcome = f"""
{PremiumFormatter.EMOJIS['crown']} *LEAKOSINT PRO* {PremiumFormatter.EMOJIS['crown']}

🔥 Welcome, {user.first_name}!
🪙 *Coins:* `{db_user.coins}`
👑 *Premium:* {premium_status}
🔑 *Referral:* `{db_user.referral_code}`

━━━━━━━━━━━━━━━━━━━━━
💡 Use `/search <phone/email>` to begin.
"""
        await update.message.reply_text(welcome, reply_markup=reply_markup, parse_mode='Markdown')
        break

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Re-send main menu
    await start_command(update, context)

async def back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start_callback(update, context)
