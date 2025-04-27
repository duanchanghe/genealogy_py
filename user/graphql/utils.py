import random
import re
from django.utils import timezone
from django.core.cache import cache
from datetime import timedelta

def generate_verification_code():
    """生成6位数字验证码"""
    return ''.join(random.choices('0123456789', k=6))

def validate_phone(phone):
    """验证手机号格式"""
    if not re.match(r'^1[3-9]\d{9}$', phone):
        return False
    return True

def validate_password(password):
    """验证密码强度"""
    if len(password) < 8:
        return False, "密码长度必须至少为8位"
    if not any(c.isdigit() for c in password):
        return False, "密码必须包含至少一个数字"
    if not any(c.isalpha() for c in password):
        return False, "密码必须包含至少一个字母"
    return True, None

def save_verification_code(email, code):
    """保存验证码到缓存
    
    Args:
        email: 用户邮箱
        code: 验证码
    
    Returns:
        bool: 是否保存成功
    """
    try:
        # 使用邮箱作为key，验证码作为value
        # 设置15分钟过期时间
        cache.set(f'verification_code_{email}', code, timeout=15*60)
        return True
    except Exception:
        return False

def verify_code(email, code):
    """验证验证码是否正确
    
    Args:
        email: 用户邮箱
        code: 用户输入的验证码
    
    Returns:
        bool: 验证是否通过
    """
    try:
        saved_code = cache.get(f'verification_code_{email}')
        if not saved_code:
            return False
        return saved_code == code
    except Exception:
        return False 