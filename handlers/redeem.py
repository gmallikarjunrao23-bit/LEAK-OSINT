"""
Redeem handler
"""

from telegram import Update
from telegram.ext import ContextTypes
from utils.formatter import PremiumFormatter

async def redeem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            f"{PremiumFormatter.EMOJIS['error']} *Usage:* `/redeem <code>`",
            parse_mode='Markdown'
        )
        return
    await update.message.reply_text(
        f"{PremiumFormatter.EMOJIS['coin']} *Promo code system coming soon.*",
        parse_mode='Markdown'
    )
