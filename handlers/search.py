"""
Search handler
"""

import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import UserService
from services.leak_api import LeakAPI
from utils.formatter import PremiumFormatter
from utils.validators import Validator
from db.session import get_db

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            f"{PremiumFormatter.EMOJIS['error']} *Usage:* `/search <phone/email>`",
            parse_mode='Markdown'
        )
        return
    target = " ".join(context.args)
    await perform_search(update, context, target)

async def text_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text.strip()
    is_valid, normalized, _ = Validator.validate_and_normalize(target)
    if not is_valid:
        await update.message.reply_text("❌ Invalid input. Send phone or email.", parse_mode='Markdown')
        return
    await perform_search(update, context, normalized)

async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE, target: str):
    user_id = update.effective_user.id
    msg = await update.message.reply_text(
        PremiumFormatter.loading_animation(target),
        parse_mode='Markdown'
    )
    
    async for session in get_db():
        user_service = UserService(session)
        
        can_search, reason = await user_service.can_search(user_id)
        if not can_search:
            await msg.edit_text(PremiumFormatter.error_message(reason), parse_mode='Markdown')
            return
        
        api = LeakAPI()
        result = await api.lookup(target)
        await api.close()
        
        if "error" in result:
            await msg.edit_text(PremiumFormatter.error_message(result["error"]), parse_mode='Markdown')
            return
        
        search_result = await user_service.perform_search(user_id, target, result)
        if "error" in search_result:
            await msg.edit_text(PremiumFormatter.error_message(search_result["error"]), parse_mode='Markdown')
            return
        
        data = result.get("data", {})
        found_count = len(data.get("results", {})) if isinstance(data, dict) else 0
        
        formatted = PremiumFormatter.result_card(target, data, found_count)
        await msg.edit_text(formatted, parse_mode='Markdown')
        break

async def search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "search_menu":
        keyboard = [
            [InlineKeyboardButton("📱 Phone", callback_data="search_phone"),
             InlineKeyboardButton("✉️ Email", callback_data="search_email")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            f"{PremiumFormatter.EMOJIS['search']} *Select search type*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
