"""
Validators
"""

import re
from typing import Tuple

class Validator:
    PHONE_PATTERN = re.compile(r'^\+?[0-9\s\-()]{7,20}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @classmethod
    def is_phone(cls, value: str) -> bool:
        cleaned = re.sub(r'[\s\-()]', '', value)
        return bool(cls.PHONE_PATTERN.match(cleaned))
    
    @classmethod
    def is_email(cls, value: str) -> bool:
        return bool(cls.EMAIL_PATTERN.match(value.lower()))
    
    @classmethod
    def validate_and_normalize(cls, value: str) -> Tuple[bool, str, str]:
        value = value.strip()
        if not value:
            return False, "", "unknown"
        
        if cls.is_phone(value):
            return True, re.sub(r'[\s\-()]', '', value), "phone"
        elif cls.is_email(value):
            return True, value.lower().strip(), "email"
        else:
            return False, value, "unknown"
