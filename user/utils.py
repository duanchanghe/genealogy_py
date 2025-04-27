import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_verification_code(length=6):
    """生成验证码"""
    return ''.join(random.choices(string.digits, k=length))

def send_verification_code(phone, code):
    """发送验证码"""
    # 这里应该调用短信服务发送验证码
    # 为了测试，我们先用邮件发送
    subject = '验证码'
    message = f'您的验证码是：{code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [phone]
    send_mail(subject, message, from_email, recipient_list) 