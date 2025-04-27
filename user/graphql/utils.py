import random
import re
from django.utils import timezone

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