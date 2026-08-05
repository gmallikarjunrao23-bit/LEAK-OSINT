"""
Premium Formatter — Show ALL API data, 2x better than reference
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
        "admin": "🔐", "chart": "📈", "clock": "⏰", "check": "✔️",
        "globe": "🌍", "info": "ℹ️", "link": "🔗", "id": "🆔",
        "name": "📛", "address": "📍", "passport": "🛂", "region": "🗺️",
        "father": "👨", "mobile": "📱", "email_icon": "✉️"
    }
    
    @staticmethod
    def result_card(target: str, target_type: str, data: Dict[str, Any], response_time: int = 0) -> str:
        """Show ALL platforms, ALL fields — exactly what API returns"""
        
        # Extract results - could be in different formats
        results = data.get("results", {}) or data.get("data", {}) or {}
        
        # Count total records
        total_sources = 0
        total_records = 0
        
        for platform, info in results.items():
            if info:
                total_sources += 1
                if isinstance(info, dict):
                    # Count non-empty fields
                    for key, value in info.items():
                        if value and str(value).strip() and str(value) != "None" and str(value) != "null":
                            total_records += 1
                elif isinstance(info, list):
                    total_records += len([i for i in info if i])
                else:
                    if info:
                        total_records += 1
        
        # Header
        lines = [
            f"✨ *LEAK OSINT PRO* ✨",
            "━━━━━━━━━━━━━━━━━━━━━",
            f"📋 *SEARCH RESULTS*",
            "",
            f"🎯 *Query:* `{target}`",
            f"📂 *Type:* `{target_type.upper()}`",
            f"📊 *Total Sources:* `{total_sources}`",
            f"📦 *Total Records:* `{total_records}`",
            f"⏱️ *Response:* {response_time}ms",
            "━━━━━━━━━━━━━━━━━━━━━",
            ""
        ]
        
        if total_sources == 0:
            lines.append("❌ *No records found*")
            lines.append("🛡️ *Clean record — No leaks detected*")
            lines.append("")
            lines.append("🪙 *Coins used:* 1")
            return "\n".join(lines)
        
        # Each platform — SHOW EVERYTHING
        platform_count = 0
        for platform, info in results.items():
            if not info:
                continue
            
            platform_count += 1
            platform_name = platform.replace("_", " ").title()
            
            lines.append(f"[{platform_count}] *{platform_name}*")
            lines.append("━" * len(platform_name) + "━" * 2)
            
            # Format data
            if isinstance(info, dict):
                for key, value in info.items():
                    if value and str(value).strip() and str(value) != "None" and str(value) != "null":
                        field_name = key.replace("_", " ").title()
                        emoji = PremiumFormatter._get_field_emoji(key)
                        
                        # Handle nested data
                        if isinstance(value, dict):
                            value_str = ", ".join([f"{k}: {v}" for k, v in value.items() if v])
                            if value_str:
                                lines.append(f"  {emoji} *{field_name}:* `{value_str}`")
                        elif isinstance(value, list):
                            value_str = ", ".join([str(v) for v in value if v])
                            if value_str:
                                lines.append(f"  {emoji} *{field_name}:* `{value_str}`")
                        else:
                            lines.append(f"  {emoji} *{field_name}:* `{value}`")
            elif isinstance(info, list):
                for item in info:
                    if item:
                        lines.append(f"  📌 `{item}`")
            else:
                lines.append(f"  📌 `{info}`")
            
            lines.append("")  # Space between platforms
        
        # Footer
        lines.append("━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"📊 *Page 1 | Records 1-{total_records} of {total_records}*")
        lines.append(f"🪙 *Coins used:* 1")
        
        return "\n".join(lines)
    
    @staticmethod
    def _get_field_emoji(field_key: str) -> str:
        field_lower = field_key.lower()
        
        if "phone" in field_lower or "mobile" in field_lower or "number" in field_lower:
            return "📱"
        elif "email" in field_lower:
            return "✉️"
        elif "name" in field_lower or "fullname" in field_lower or "firstname" in field_lower:
            return "📛"
        elif "address" in field_lower or "adres" in field_lower or "location" in field_lower:
            return "📍"
        elif "passport" in field_lower or "id" in field_lower or "aadhar" in field_lower:
            return "🛂"
        elif "region" in field_lower or "state" in field_lower or "city" in field_lower:
            return "🗺️"
        elif "father" in field_lower or "mother" in field_lower or "parent" in field_lower:
            return "👨"
        elif "username" in field_lower or "user" in field_lower:
            return "👤"
        elif "url" in field_lower or "link" in field_lower:
            return "🔗"
        elif "date" in field_lower or "time" in field_lower:
            return "📅"
        elif "passport" in field_lower:
            return "🛂"
        else:
            return "📌"
    
    @staticmethod
    def profile_card(user) -> str:
        """User profile — premium card"""
        premium_status = "✅ Active" if user.is_premium else "❌ Inactive"
        
        tier = "Bronze"
        if user.coins >= 500:
            tier = "Gold 🥇"
        elif user.coins >= 200:
            tier = "Silver 🥈"
        
        return f"""
👑 *USER PROFILE* 👑
━━━━━━━━━━━━━━━━━━━━━
📛 *Name:* {user.first_name or 'N/A'}
🆔 *User ID:* `{user.telegram_id}`
👤 *Username:* @{user.username or 'N/A'}
📅 *Joined:* {user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'}

━━━━━━━━━━━━━━━━━━━━━
🪙 *Coins:* `{user.coins}` [ {tier} ]
🔍 *Searches:* {user.total_searches}
💰 *Cost:* {1} coin/search
👥 *Referrals:* {user.total_referrals}

━━━━━━━━━━━━━━━━━━━━━
🛡️ *Premium:* {premium_status}
"""
    
    @staticmethod
    def loading_animation(target: str) -> str:
        return f"""
⏳ *Scanning 500+ databases...*

🎯 *Query:* `{target}`
✨ *This may take a few seconds*

📊 *Checking:*
  • Social Media Platforms
  • Breach Databases
  • Public Records
  • Dark Web Sources
"""
