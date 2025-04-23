from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User, VerificationCode
from django.utils import timezone
from datetime import timedelta

class PhonePasswordBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
            if user.phone_password == password:  # 注意：实际应用中应该使用加密密码
                return user
        except User.DoesNotExist:
            return None
        return None

class PhoneVerificationCodeBackend(ModelBackend):
    def authenticate(self, request, phone=None, code=None, **kwargs):
        try:
            # 验证码有效期为5分钟
            valid_time = timezone.now() - timedelta(minutes=5)
            verification = VerificationCode.objects.filter(
                phone=phone,
                code=code,
                is_used=False,
                created_at__gte=valid_time
            ).first()
            
            if verification:
                user = User.objects.get(phone=phone)
                verification.is_used = True
                verification.save()
                return user
        except User.DoesNotExist:
            return None
        return None 