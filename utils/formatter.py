"""
Premium Formatter — Parse API response correctly, show ALL data
"""

from typing import Dict, Any
from datetime import datetime

class PremiumFormatter:
    EMOJIS = {
        # Premium / Header
        "crown": "👑",
        "sparkle": "✨",
        "fire": "🔥",
        "rocket": "🚀",
        "star": "⭐",
        "diamond": "💎",
        "trophy": "🏆",
        "shield": "🛡️",
        "bolt": "⚡",
        "target": "🎯",
        
        # Actions / Status
        "search": "🔍",
        "found": "✅",
        "error": "❌",
        "warning": "⚠️",
        "loading": "⏳",
        "check": "✔️",
        "lock": "🔒",
        "key": "🔑",
        
        # Data / Info
        "coin": "🪙",
        "wallet": "💰",
        "gift": "🎁",
        "database": "🗄️",
        "graph": "📊",
        "chart": "📈",
        "clock": "⏰",
        "calendar": "📅",
        "pdf": "📄",
        "history": "📜",
        
        # Contact / People
        "phone": "📱",
        "mobile": "📱",
        "email": "✉️",
        "email_icon": "✉️",
        "user": "👤",
        "username": "👤",
        "admin": "🔐",
        "support": "🆘",
        "info": "ℹ️",
        "link": "🔗",
        "id": "🆔",
        "name": "📛",
        "fullname": "📛",
        "firstname": "📛",
        "lastname": "📛",
        "father": "👨",
        "fathername": "👨",
        "mother": "👩",
        "address": "📍",
        "adres": "📍",
        "location": "📍",
        "city": "🏙️",
        "state": "🗺️",
        "region": "🗺️",
        "country": "🌍",
        "globe": "🌍",
        "passport": "🛂",
        "aadhar": "🆔",
        "pan": "🆔",
        "url": "🔗",
        "website": "🌐",
        "title": "📌",
        "description": "📝",
        "records": "📊",
        "source": "📂"
    }
    
    @staticmethod
    def result_card(target: str, target_type: str, data: Dict[str, Any], response_time: int = 0) -> str:
        """Parse and show ALL data from API — premium format"""
        
        lines = [
            f"{PremiumFormatter.EMOJIS.get('sparkle', '✨')} *LEAK OSINT PRO* {PremiumFormatter.EMOJIS.get('sparkle', '✨')}",
            "━━━━━━━━━━━━━━━━━━━━━",
            "📋 *SEARCH RESULTS*",
            "",
            f"🎯 *Query:* `{target}`",
            f"📂 *Type:* `{target_type.upper()}`",
            f"⏱️ *Response:* {response_time}ms",
            "━━━━━━━━━━━━━━━━━━━━━",
            ""
        ]
        
        # Check if data exists
        if not data:
            lines.append("❌ *No data received*")
            lines.append("")
            lines.append(f"{PremiumFormatter.EMOJIS.get('coin', '🪙')} *Coins used:* 1")
            return "\n".join(lines)
        
        # Parse the actual data
        total_records = 0
        platform_count = 0
        
        # Iterate through sources (source1, source2, etc.)
        for source_key, source_data in data.items():
            if not source_data:
                continue
                
            platform_count += 1
            title = source_data.get("title", source_key.replace("_", " ").title())
            description = source_data.get("description", "")
            records = source_data.get("records", [])
            
            # Clean title (remove emoji prefixes like 💾)
            if title and title[0] in ["💾", "📁", "🗂️"]:
                title = title[1:]
            
            lines.append(f"[{platform_count}] *{title}*")
            lines.append("━" * min(len(title) + 2, 30))
            
            # Show description if present
            if description:
                if len(description) > 250:
                    description = description[:250] + "..."
                lines.append(f"  📝 *Info:* {description}")
                lines.append("")
            
            # Show records
            if records:
                for idx, record in enumerate(records, 1):
                    if isinstance(record, dict):
                        for field_key, field_value in record.items():
                            if field_value and str(field_value).strip():
                                clean_key = field_key.lower().replace(" ", "").replace("_", "")
                                emoji = PremiumFormatter.EMOJIS.get(clean_key, "📌")
                                field_name = field_key.replace("_", " ").title()
                                
                                # Handle nested values
                                if isinstance(field_value, dict):
                                    value_str = ", ".join([f"{k}: {v}" for k, v in field_value.items() if v])
                                elif isinstance(field_value, list):
                                    value_str = ", ".join([str(v) for v in field_value if v])
                                else:
                                    value_str = str(field_value)
                                
                                lines.append(f"  {emoji} *{field_name}:* `{value_str}`")
                                total_records += 1
                    else:
                        lines.append(f"  📌 `{record}`")
                        total_records += 1
                
                lines.append("")  # Space after records
            else:
                lines.append("  ❌ *No records in this source*")
                lines.append("")
        
        if total_records == 0:
            lines.append("❌ *No records found*")
            lines.append("🛡️ *Clean record — No leaks detected*")
        
        # Footer
        lines.append("━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"📊 *Total Sources: {platform_count} | Total Records: {total_records}*")
        lines.append(f"{PremiumFormatter.EMOJIS.get('coin', '🪙')} *Coins used:* 1")
        
        return "\n".join(lines)
    
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
{PremiumFormatter.EMOJIS.get('crown', '👑')} *USER PROFILE* {PremiumFormatter.EMOJIS.get('crown', '👑')}
━━━━━━━━━━━━━━━━━━━━━
📛 *Name:* {user.first_name or 'N/A'}
🆔 *User ID:* `{user.telegram_id}`
👤 *Username:* @{user.username or 'N/A'}
📅 *Joined:* {user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'}

━━━━━━━━━━━━━━━━━━━━━
{PremiumFormatter.EMOJIS.get('coin', '🪙')} *Coins:* `{user.coins}` [ {tier} ]
🔍 *Searches:* {user.total_searches}
💰 *Cost:* {1} coin/search
👥 *Referrals:* {user.total_referrals}

━━━━━━━━━━━━━━━━━━━━━
🛡️ *Premium:* {premium_status}
"""
    
    @staticmethod
    def loading_animation(target: str) -> str:
        return f"""
{PremiumFormatter.EMOJIS.get('loading', '⏳')} *Scanning 500+ databases...*

🎯 *Query:* `{target}`
✨ *This may take a few seconds*

📊 *Checking:*
  • Social Media Platforms
  • Breach Databases
  • Public Records
  • Dark Web Sources
"""
