"""
History handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from repositories.query_repo import QueryRepository
from utils.formatter import PremiumFormatter
from db.session import get_db

async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async for session in get_db():
        query_repo = QueryRepository(session)
        history = await query_repo.get_user_history(user_id, limit=10)
        
        if not history:
            await update.message.reply_text(f"{PremiumFormatter.EMOJIS['history']} *No search history*", parse_mode='Markdown')
            return
        
        lines = [f"{PremiumFormatter.EMOJIS['history']} *SEARCH HISTORY*", "━━━━━━━━━━━━━━━━━━━━━"]
        for idx, q in enumerate(history, 1):
            date = q.created_at.strftime('%Y-%m-%d %H:%M') if q.created_at else 'N/A'
            lines.append(f"{idx}. `{q.target}` — {q.found_count} found\n   📅 {date}")
        
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        await update.message.reply_text("\n".join(lines), parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        break

async def history_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await history_command(update, context)
