"""
Payment handler — UPI flow
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.payment_service import PaymentService
from services.premium_service import PremiumService
from utils.formatter import PremiumFormatter
from config.settings import settings
from db.session import get_db

UPI_ID = settings.UPI_ID

async def pay_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async for session in get_db():
        premium_service = PremiumService(session)
        tier = await premium_service.get_user_tier(user_id)
        
        if tier.value in ["premium", "enterprise"]:
            await update.message.reply_text(
                f"👑 *You already have {tier.value.upper()} plan!*",
                parse_mode='Markdown'
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("👑 Premium (₹100/mo)", callback_data="pay_premium"),
             InlineKeyboardButton("🏢 Enterprise (₹500/yr)", callback_data="pay_enterprise")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
        ]
        
        await update.message.reply_text(
            f"""
{ PremiumFormatter.EMOJIS['wallet']} *UPI PAYMENT* {PremiumFormatter.EMOJIS['wallet']}

💳 *UPI ID:* `{UPI_ID}`

📋 *Steps:*

1️⃣ Send payment to `{UPI_ID}`
2️⃣ Note your Transaction ID
3️⃣ Click a plan below
4️⃣ Submit your transaction ID

━━━━━━━━━━━━━━━━━━━━━
👑 *Premium* — ₹100/month
🏢 *Enterprise* — ₹500/year
""",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        break

async def payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    plan = query.data.replace("pay_", "")
    context.user_data['payment_plan'] = plan
    
    prices = {"premium": 100, "enterprise": 500}
    price = prices.get(plan, 100)
    
    keyboard = [[InlineKeyboardButton("✅ Submit Proof", callback_data="payment_submit")]]
    await query.edit_message_text(
        f"""
{PremiumFormatter.EMOJIS['wallet']} *PAYMENT — {plan.upper()}*

💳 *UPI ID:* `{UPI_ID}`
💵 *Amount:* ₹{price}

📋 *Step 1:* Send ₹{price} to `{UPI_ID}`
📋 *Step 2:* Click Submit Proof below
📋 *Step 3:* Enter your Transaction ID

⚠️ Keep your transaction ID ready.
""",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def payment_submit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        f"""
{ PremiumFormatter.EMOJIS['key']} *SUBMIT PAYMENT PROOF*

📋 *Step 3:* Enter your transaction ID

*Format:* `/submit <transaction_id>`
*Example:* `/submit 1234567890`
""",
        parse_mode='Markdown'
    )

async def submit_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            f"{PremiumFormatter.EMOJIS['error']} *Usage:* `/submit <transaction_id>`",
            parse_mode='Markdown'
        )
        return
    
    user_id = update.effective_user.id
    username = update.effective_user.username or "N/A"
    txn_id = context.args[0]
    plan = context.user_data.get('payment_plan', 'premium')
    prices = {"premium": 100, "enterprise": 500}
    amount = prices.get(plan, 100)
    
    async for session in get_db():
        payment_service = PaymentService(session)
        
        payment = await payment_service.create_upi_payment(
            user_id=user_id,
            username=username,
            transaction_id=txn_id,
            amount=amount,
            plan=plan
        )
        
        await update.message.reply_text(
            f"""
{ PremiumFormatter.EMOJIS['check']} *PAYMENT SUBMITTED!*

✅ Your payment proof has been submitted.

📋 *Details:*
• Plan: `{plan.upper()}`
• Amount: ₹{amount}
• Txn ID: `{txn_id}`

⏳ *Status:* Pending admin verification

🔔 You'll be notified when approved.
Use `/checkpayment` to check status.
""",
            parse_mode='Markdown'
        )
        break

async def check_payment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    async for session in get_db():
        payment_service = PaymentService(session)
        payments = await payment_service.get_user_payments(user_id, limit=5)
        
        if not payments:
            await update.message.reply_text(
                f"{PremiumFormatter.EMOJIS['history']} *No payment history*",
                parse_mode='Markdown'
            )
            return
        
        lines = [f"{PremiumFormatter.EMOJIS['history']} *PAYMENT HISTORY*", "━━━━━━━━━━━━━━━━━━━━━"]
        status_emojis = {"pending": "⏳", "approved": "✅", "rejected": "❌", "completed": "🎉"}
        
        for p in payments:
            emoji = status_emojis.get(p.status, "❓")
            date = p.created_at.strftime('%Y-%m-%d') if p.created_at else 'N/A'
            lines.append(f"{emoji} *{p.plan.upper()}* — ₹{p.amount} | {p.status.upper()}")
        
        await update.message.reply_text("\n".join(lines), parse_mode='Markdown')
        break
