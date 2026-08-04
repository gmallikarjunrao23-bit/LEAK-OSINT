"""
Premium Formatter — Emojis, Colors, Cards
"""

from typing import Dict, Any
from datetime import datetime

class PremiumFormatter:
    EMOJIS = {
        "search": "🔍", "found": "✅", "error": "❌", "warning": "⚠️",
        "loading": "⏳", "coin": "🪙", "crown": "👑", "fire": "🔥",
        "sparkle": "✨", "star": "⭐", "rocket": "🚀", "lock": "🔒",
        "key": "🔑", "database": "🗄️", "graph": "📊", "pdf": "📄",
        "wallet": "💰", "gift": "🎁", "trophy": "🏆", "shield": "🛡️",
        "bolt": "⚡", "target": "🎯", "diamond": "💎", "phone": "📱",
        "email": "✉️", "user": "👤", "history": "📜", "support": "🆘",
        "admin": "🔐", "chart": "📈", "clock": "⏰", "check": "✔️"
    }
    
    @staticmethod
    def result_card(target: str, data: Dict[str, Any], found_count: int) -> str:
        if found_count == 0:
            return f"""
🔍 *Search Results for:* `{target}`

❌ *No leaks found*
🛡️ *Clean record*

🪙 *Coins used:* 1
"""
        lines = [
            f"{PremiumFormatter.EMOJIS['sparkle']} *LEAK REPORT* {PremiumFormatter.EMOJIS['sparkle']}",
            "",
            f"{PremiumFormatter.EMOJIS['phone']} *Target:* `{target}`",
            f"{PremiumFormatter.EMOJIS['database']} *Databases:* {found_count}",
            "",
            "━━━━━━━━━━━━━━━━━━━━━",
            ""
        ]
        
        results = data.get("results", {}) or data.get("data", {}) or {}
        for idx, (db_name, info) in enumerate(results.items(), 1):
            if info:
                if isinstance(info, dict):
                    info_str = ", ".join([f"{k}: {v}" for k, v in info.items() if v])
                else:
                    info_str = str(info)
                lines.append(f"{idx}. *{db_name}*")
                lines.append(f"   └─ {info_str[:200]}")
                lines.append("")
        
        lines.append(f"{PremiumFormatter.EMOJIS['lock']} *Report generated securely*")
        lines.append(f"🪙 *Coins used:* 1")
        return "\n".join(lines)
    
    @staticmethod
    def loading_animation(target: str) -> str:
        return f"""
{PremiumFormatter.EMOJIS['loading']} *Scanning 500+ databases...*

🎯 *Target:* `{target}`
✨ *This may take a few seconds*
"""
    
    @staticmethod
    def error_message(error: str, suggestion: str = None) -> str:
        lines = [f"{PremiumFormatter.EMOJIS['error']} *Error*\n━━━━━━━━━━━━━━━━━━━━━\n💬 {error}"]
        if suggestion:
            lines.append(f"\n💡 *Suggestion:* {suggestion}")
        return "\n".join(lines)
    
    @staticmethod
    def plans_card(pricing: dict) -> str:
        return f"""
{PremiumFormatter.EMOJIS['crown']} *SUBSCRIPTION PLANS* {PremiumFormatter.EMOJIS['crown']}

📋 *Free*
  • 5 searches/day
  • Basic search only
  • Price: `FREE`

{PremiumFormatter.EMOJIS['diamond']} *Premium* — ₹{pricing['premium']['price']}/mo
  • 100 searches/day
  • PDF export
  • Animated emojis
  • Colored buttons

{PremiumFormatter.EMOJIS['trophy']} *Enterprise* — ₹{pricing['enterprise']['price']}/yr
  • Unlimited searches
  • All premium features
  • Priority support

💳 *UPI:* `{UPI_ID}`
💡 Use `/pay` to subscribe
"""
