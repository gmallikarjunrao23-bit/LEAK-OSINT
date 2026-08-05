"""
Search handler — Accept ANY input, show ALL API data
"""

import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import UserService
from services.leak_api import LeakAPI
from utils.formatter import PremiumFormatter
from db.session import get_db

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            f"🔍 *LEAK OSINT PRO*\n━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Search anything:*\n"
            f"  • Phone: `9876543210`\n"
            f"  • Email: `john@gmail.com`\n"
            f"  • Username: `@john_doe`\n"
            f"  • Domain: `example.com`\n"
            f"  • Any text: `anything`\n\n"
            f"📝 *Usage:* `/search <query>`",
            parse_mode='Markdown'
        )
        return
    
    target = " ".join(context.args)
    await perform_search(update, context, target)

async def text_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any text input — direct search"""
    target = update.message.text.strip()
    await perform_search(update, context, target)

async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE, target: str):
    user_id = update.effective_user.id
    
    # Detect type (just for display)
    from utils.validators import Validator
    input_type = Validator.detect_type(target)
    if input_type == "unknown":
        input_type = "text"
    
    msg = await update.message.reply_text(
        f"⏳ *Scanning 500+ databases...*\n"
        f"🎯 *Query:* `{target}`\n"
        f"📋 *Type:* `{input_type.upper()}`\n"
        f"✨ *This may take a few seconds*",
        parse_mode='Markdown'
    )
    
    async for session in get_db():
        user_service = UserService(session)
        
        # Check coins
        can_search, reason = await user_service.can_search(user_id)
        if not can_search:
            await msg.edit_text(
                f"❌ *Error*\n━━━━━━━━━━━━━━━━━━━━━\n{reason}",
                parse_mode='Markdown'
            )
            return
        
        # Call API
        api = LeakAPI()
        result = await api.lookup(target)
        await api.close()
        
        if "error" in result:
            await msg.edit_text(
                f"❌ *API Error*\n━━━━━━━━━━━━━━━━━━━━━\n{result['error']}",
                parse_mode='Markdown'
            )
            return
        
        # Log search
        await user_service.perform_search(user_id, target, result)
        
        # Get data — RAW API response
        data = result.get("data", {})
        response_time = result.get("response_time_ms", 0)
        
        # Format — SHOW EVERYTHING
        formatted = PremiumFormatter.result_card(
            target=target,
            target_type=input_type,
            data=data,
            response_time=response_time
        )
        
        await msg.edit_text(formatted, parse_mode='Markdown')
        break

async def search_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "search_menu":
        keyboard = [
            [InlineKeyboardButton("📱 Phone", callback_data="search_phone"),
             InlineKeyboardButton("✉️ Email", callback_data="search_email")],
            [InlineKeyboardButton("👤 Username", callback_data="search_username"),
             InlineKeyboardButton("🌐 Domain", callback_data="search_domain")],
            [InlineKeyboardButton("🔍 Any Query", callback_data="search_any")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        await query.edit_message_text(
            "🔍 *LEAK OSINT PRO*\n━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 *Search anything:*\n"
            "  • Phone: `9876543210`\n"
            "  • Email: `john@gmail.com`\n"
            "  • Username: `@john_doe`\n"
            "  • Domain: `example.com`\n"
            "  • Any text: `anything`\n\n"
            "📝 *Usage:* `/search <query>`",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "search_any":
        await query.edit_message_text(
            "🔍 *Enter anything to search*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Examples:*\n"
            f"  • `9876543210`\n"
            f"  • `john@gmail.com`\n"
            f"  • `@john_doe`\n"
            f"  • `example.com`\n"
            f"  • `anything`\n\n"
            f"📝 Just type and send!",
            parse_mode='Markdown'
        )
    else:
        # Phone, email, username, domain
        search_type = query.data.replace("search_", "")
        await query.edit_message_text(
            f"🔍 *Enter {search_type} to search*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Example:*\n"
            f"  • {search_type}: `{'9876543210' if search_type == 'phone' else 'john@gmail.com' if search_type == 'email' else '@john_doe' if search_type == 'username' else 'example.com'}`\n\n"
            f"📝 Just type and send!",
            parse_mode='Markdown'
        )
