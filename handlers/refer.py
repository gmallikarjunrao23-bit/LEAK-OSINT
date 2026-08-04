"""
Referral handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import UserService
from utils.formatter import PremiumFormatter
from db.session import get_db

async def refer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async for session in get_db():
        user_service = UserService(session)
        user = await user_service.user_repo.get_by_telegram_id(user_id)
        if not user:
            await update.message.reply_text("❌ User not found.")
            return
        
        referral_link = f"https://t.me/{context.bot.username}?start=ref_{user.referral_code}"
        
        text = f"""
{PremiumFormatter.EMOJIS['gift']} *REFER & EARN* {PremiumFormatter.EMOJIS['gift']}

🔑 *Your Code:* `{user.referral_code}`
🔗 *Link:* `{referral_link}`

🎁 *Rewards:*
• You get `5 🪙` per referral
• Your friend gets `2.5 🪙`

📊 *Total Referrals:* {user.total_referrals}
"""
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        break

async def refer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await refer_command(update, context)
