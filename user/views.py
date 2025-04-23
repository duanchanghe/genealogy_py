from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
from .models import User, VerificationCode
import json

def generate_verification_code():
    """生成6位数字验证码"""
    return ''.join(random.choices('0123456789', k=6))

@csrf_exempt
def send_verification_code(request):
    """
    发送验证码API
    
    请求示例:
    POST /send-verification-code/
    Content-Type: application/json
    
    {
        "phone": "13800138000"
    }
    
    成功响应:
    {
        "message": "验证码已发送",
        "code": "123456"  # 仅测试环境返回，生产环境应删除
    }
    
    错误响应:
    {
        "error": "手机号不能为空"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
            
            if not phone:
                return JsonResponse({'error': '手机号不能为空'}, status=400)
                
            # 生成验证码
            code = generate_verification_code()
            
            # 保存验证码
            VerificationCode.objects.create(
                phone=phone,
                code=code
            )
            
            # TODO: 这里应该调用短信服务发送验证码
            # 为了测试，直接返回验证码
            return JsonResponse({
                'message': '验证码已发送',
                'code': code  # 实际生产环境中应该删除这行
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '不支持的请求方法'}, status=405)

@csrf_exempt
def phone_password_login(request):
    """
    手机号密码登录API
    
    请求示例:
    POST /phone-password-login/
    Content-Type: application/json
    
    {
        "phone": "13800138000",
        "password": "your_password"
    }
    
    成功响应:
    {
        "message": "登录成功",
        "user": {
            "id": 1,
            "username": "username",
            "phone": "13800138000"
        }
    }
    
    错误响应:
    {
        "error": "手机号或密码错误"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
            password = data.get('password')
            
            if not phone or not password:
                return JsonResponse({'error': '手机号和密码不能为空'}, status=400)
            
            user = authenticate(request, phone=phone, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': '登录成功',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'phone': user.phone
                    }
                })
            else:
                return JsonResponse({'error': '手机号或密码错误'}, status=401)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '不支持的请求方法'}, status=405)

@csrf_exempt
def phone_code_login(request):
    """
    手机号验证码登录API
    
    请求示例:
    POST /phone-code-login/
    Content-Type: application/json
    
    {
        "phone": "13800138000",
        "code": "123456"
    }
    
    成功响应:
    {
        "message": "登录成功",
        "user": {
            "id": 1,
            "username": "username",
            "phone": "13800138000"
        }
    }
    
    错误响应:
    {
        "error": "手机号或验证码错误"
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
            code = data.get('code')
            
            if not phone or not code:
                return JsonResponse({'error': '手机号和验证码不能为空'}, status=400)
            
            user = authenticate(request, phone=phone, code=code)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'message': '登录成功',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'phone': user.phone
                    }
                })
            else:
                return JsonResponse({'error': '手机号或验证码错误'}, status=401)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '不支持的请求方法'}, status=405)
