"""
Logging middleware
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            user = update.effective_user
            logger.info(f"[{datetime.utcnow().isoformat()}] User {user.id} (@{user.username or 'N/A'}) sent: {update.message.text or '[non-text]'}")
        elif update.callback_query:
            user = update.effective_user
            logger.info(f"[{datetime.utcnow().isoformat()}] User {user.id} callback: {update.callback_query.data}")
        return True
