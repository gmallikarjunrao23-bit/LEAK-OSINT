"""
Plans handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.premium_service import PremiumService
from utils.formatter import PremiumFormatter
from config.settings import settings
from db.session import get_db

async def plans_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async for session in get_db():
        premium_service = PremiumService(session)
        pricing = premium_service.get_pricing()
        
        keyboard = [
            [InlineKeyboardButton("👑 Premium — ₹100/mo", callback_data="pay_premium"),
             InlineKeyboardButton("🏢 Enterprise — ₹500/yr", callback_data="pay_enterprise")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        await update.message.reply_text(
            PremiumFormatter.plans_card(pricing),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        break

async def plans_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await plans_command(update, context)
