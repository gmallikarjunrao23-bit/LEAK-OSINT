"""
Start handler — Welcome + Registration
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
            [
                InlineKeyboardButton(f"{PremiumFormatter.EMOJIS.get('search', '🔍')} Search", callback_data="search_menu"),
                InlineKeyboardButton(f"{PremiumFormatter.EMOJIS.get('user', '👤')} Profile", callback_data="profile_menu")
            ],
            [
                InlineKeyboardButton(f"{PremiumFormatter.EMOJIS.get('wallet', '💰')} Plans", callback_data="plans_menu"),
                InlineKeyboardButton(f"{PremiumFormatter.EMOJIS.get('gift', '🎁')} Refer", callback_data="refer_menu")
            ],
            [
                InlineKeyboardButton(f"{PremiumFormatter.EMOJIS.get('history', '📜')} History", callback_data="history_menu"),
                InlineKeyboardButton(f"{PremiumFormatter.EMOJIS.get('support', '🆘')} Support", callback_data="support_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        premium_status = "✅" if db_user.is_premium else "❌"
        crown = PremiumFormatter.EMOJIS.get('crown', '👑')
        coin = PremiumFormatter.EMOJIS.get('coin', '🪙')
        
        welcome = f"""
{crown} *LEAK OSINT PRO* {crown}
━━━━━━━━━━━━━━━━━━━━━

🔥 Welcome, {user.first_name}!
🔐 *Your private leak intelligence bot*

📊 *500+ databases indexed*
{coin} *Coins:* `{db_user.coins}`
👑 *Premium:* {premium_status}
🔑 *Referral Code:* `{db_user.referral_code}`

━━━━━━━━━━━━━━━━━━━━━
💡 Use `/search <phone/email>` to begin.
⚡ Premium users get animated results & PDF export.
"""
        
        await update.message.reply_text(
            welcome,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        break

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start_command(update, context)

async def back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start_callback(update, context)
