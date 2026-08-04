"""
LeakPro API wrapper
"""

import aiohttp
import asyncio
import hashlib
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from config.settings import settings

class LeakAPI:
    def __init__(self):
        self.base_url = settings.LEAK_API_URL
        self.api_key = settings.LEAK_API_KEY
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache = {}
        self.max_retries = 3
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={"User-Agent": "Mozilla/5.0"}
            )
        return self.session
    
    def _cache_key(self, target: str) -> str:
        return hashlib.md5(f"{target}_{self.api_key}".encode()).hexdigest()
    
    async def lookup(self, target: str, force_refresh: bool = False) -> Dict[str, Any]:
        cache_key = self._cache_key(target)
        
        if not force_refresh and cache_key in self.cache:
            entry = self.cache[cache_key]
            if datetime.utcnow() < entry["expires_at"]:
                return entry["data"]
            else:
                del self.cache[cache_key]
        
        session = await self._get_session()
        params = {"key": self.api_key, "number": target}
        start_time = time.time()
        
        for attempt in range(self.max_retries):
            try:
                async with session.get(self.base_url, params=params) as resp:
                    response_time_ms = int((time.time() - start_time) * 1000)
                    
                    if resp.status == 200:
                        data = await resp.json()
                        result = {"data": data, "status": resp.status, "response_time_ms": response_time_ms}
                        self.cache[cache_key] = {"data": result, "expires_at": datetime.utcnow() + timedelta(hours=1)}
                        return result
                    elif resp.status == 429:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    else:
                        return {"error": f"HTTP {resp.status}", "status": resp.status}
            except asyncio.TimeoutError:
                if attempt == self.max_retries - 1:
                    return {"error": "Timeout"}
                await asyncio.sleep(1)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return {"error": str(e)}
                await asyncio.sleep(1)
        
        return {"error": "Max retries exceeded"}
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
