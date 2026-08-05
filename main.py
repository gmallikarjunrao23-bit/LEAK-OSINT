"""
LeakOSINT Pro — Main Entry Point
"""

import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config.settings import settings
from handlers import start, search, profile, plans, payment, refer, redeem, history, admin, support
from middlewares import ThrottleMiddleware, LoggingMiddleware
from db.session import init_db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class LeakBot:
    def __init__(self):
        self.token = settings.BOT_TOKEN
        self.app = None
    
    def build(self) -> Application:
        logger.info("🔥 Building LeakOSINT Pro...")
        
        self.app = Application.builder().token(self.token).build()
        
        self._register_handlers()
        
        logger.info("✅ Bot built successfully")
        return self.app
    
    def _register_handlers(self):
        # Commands
        self.app.add_handler(CommandHandler("start", start.start_command))
        self.app.add_handler(CommandHandler("search", search.search_command))
        self.app.add_handler(CommandHandler("profile", profile.profile_command))
        self.app.add_handler(CommandHandler("plans", plans.plans_command))
        self.app.add_handler(CommandHandler("pay", payment.pay_command))
        self.app.add_handler(CommandHandler("submit", payment.submit_payment))
        self.app.add_handler(CommandHandler("checkpayment", payment.check_payment_command))
        self.app.add_handler(CommandHandler("refer", refer.refer_command))
        self.app.add_handler(CommandHandler("redeem", redeem.redeem_command))
        self.app.add_handler(CommandHandler("history", history.history_command))
        self.app.add_handler(CommandHandler("admin", admin.admin_command))
        self.app.add_handler(CommandHandler("support", support.support_command))
        
        # Callbacks
        self.app.add_handler(CallbackQueryHandler(start.start_callback, pattern="^start$"))
        self.app.add_handler(CallbackQueryHandler(search.search_callback, pattern="^search_"))
        self.app.add_handler(CallbackQueryHandler(plans.plans_callback, pattern="^plan_"))
        self.app.add_handler(CallbackQueryHandler(payment.payment_callback, pattern="^pay_"))
        self.app.add_handler(CallbackQueryHandler(payment.payment_submit_callback, pattern="^payment_submit$"))
        self.app.add_handler(CallbackQueryHandler(refer.refer_callback, pattern="^refer_"))
        self.app.add_handler(CallbackQueryHandler(profile.profile_callback, pattern="^profile_"))
        self.app.add_handler(CallbackQueryHandler(history.history_callback, pattern="^history_"))
        self.app.add_handler(CallbackQueryHandler(admin.admin_callback, pattern="^admin_"))
        self.app.add_handler(CallbackQueryHandler(support.support_callback, pattern="^support_"))
        self.app.add_handler(CallbackQueryHandler(start.back_callback, pattern="^back_"))
        
        # Text handler for direct search
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Regex(r'^\+?[0-9]{10,15}$|^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            search.text_search
        ))
    
    def run(self):
        logger.info("🚀 Starting bot polling...")
        self.app.run_polling()

if __name__ == "__main__":
    await init_db()
    bot = LeakBot()
    bot.build()
    bot.run()
