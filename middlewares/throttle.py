"""
Throttle middleware
"""

from typing import Dict, List
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ContextTypes

class ThrottleMiddleware:
    def __init__(self, rate_limit: int = 3, per_seconds: int = 5):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.requests: Dict[int, List[datetime]] = {}
    
    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id if update.effective_user else None
        if not user_id:
            return
        
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.per_seconds)
        
        if user_id in self.requests:
            self.requests[user_id] = [t for t in self.requests[user_id] if t > cutoff]
        else:
            self.requests[user_id] = []
        
        if len(self.requests[user_id]) >= self.rate_limit:
            await update.message.reply_text(
                f"⏳ *Slow down!* Please wait {self.per_seconds} seconds.",
                parse_mode='Markdown'
            )
            return False
        
        self.requests[user_id].append(now)
        return True
