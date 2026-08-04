"""
Admin handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.settings import settings
from repositories.query_repo import QueryRepository
from repositories.user_repo import UserRepository
from db.session import get_db

async def is_admin(user_id: int) -> bool:
    return user_id in settings.ADMIN_IDS

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ Unauthorized.")
        return
    
    async for session in get_db():
        query_repo = QueryRepository(session)
        user_repo = UserRepository(session)
        
        global_stats = await query_repo.get_global_stats()
        total_users = await user_repo.count()
        premium_users = await user_repo.count(is_premium=True)
        
        text = f"""
🔐 *ADMIN PANEL*
━━━━━━━━━━━━━━━━━━━━━
👤 Users: {total_users}
👑 Premium: {premium_users}
🔍 Searches: {global_stats['total_searches']}
📦 Found: {global_stats['total_found']}

🔗 *Web Admin:* http://yourdomain.com
"""
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        break

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await admin_command(update, context)
