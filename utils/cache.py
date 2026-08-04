"""
Cache — Redis/in-memory
"""

import hashlib
import json
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
from config.settings import settings

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class Cache:
    def __init__(self):
        self.redis = None
        self.memory_cache: Dict[str, tuple] = {}
        if REDIS_AVAILABLE and settings.REDIS_URL:
            self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def get(self, key: str) -> Optional[Any]:
        if self.redis:
            try:
                value = await self.redis.get(key)
                if value:
                    return json.loads(value)
            except:
                pass
        if key in self.memory_cache:
            value, expires_at = self.memory_cache[key]
            if expires_at > datetime.utcnow():
                return value
            else:
                del self.memory_cache[key]
        return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        serialized = json.dumps(value)
        if self.redis:
            try:
                await self.redis.setex(key, ttl, serialized)
                return True
            except:
                pass
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        self.memory_cache[key] = (value, expires_at)
        return True

cache = Cache()
