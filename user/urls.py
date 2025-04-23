from django.urls import path
from . import views

urlpatterns = [
    # 这里可以添加user应用的URL patterns
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('phone-password-login/', views.phone_password_login, name='phone_password_login'),
    path('phone-code-login/', views.phone_code_login, name='phone_code_login'),
] 