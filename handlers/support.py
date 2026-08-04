"""
Support handler
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.formatter import PremiumFormatter

async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
{PremiumFormatter.EMOJIS['support']} *SUPPORT* {PremiumFormatter.EMOJIS['support']}

📚 *Common Issues:*
• Insufficient coins → /refer or /plans
• Search not working → Check input format
• Payment issues → /checkpayment

👑 *Premium Support:* Priority for premium users

━━━━━━━━━━━━━━━━━━━━━
📧 *Contact:* @YouKnowAbhi
"""
    keyboard = [
        [InlineKeyboardButton("👤 @YouKnowAbhi", url="https://t.me/YouKnowAbhi")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ]
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await support_command(update, context)
