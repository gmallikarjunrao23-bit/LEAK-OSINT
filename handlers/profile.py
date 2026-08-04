"""
Profile handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import UserService
from db.session import get_db

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async for session in get_db():
        user_service = UserService(session)
        details = await user_service.get_user_with_details(user_id)
        if not details:
            await update.message.reply_text("❌ User not found.")
            return
        
        user = details["user"]
        stats = details["stats"]
        
        text = f"""
👑 *USER PROFILE* 👑
━━━━━━━━━━━━━━━━━━━━━
📌 *ID:* `{user.telegram_id}`
👤 *Name:* {user.first_name or 'N/A'}
🏷️ *Plan:* `{user.plan.upper()}`
🛡️ *Premium:* {"✅ Active" if user.is_premium else "❌ Inactive"}
🪙 *Coins:* `{user.coins}`
🔑 *Referral:* `{user.referral_code}`
👥 *Referrals:* {user.total_referrals}
🔍 *Searches:* {stats['total_searches']}
📦 *Found:* {stats['total_found']}
"""
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        break

async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await profile_command(update, context)
