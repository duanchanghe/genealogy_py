import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .utils import generate_verification_code, send_verification_code
from django.core.cache import cache
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')

class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()

class RegisterMutation(graphene.Mutation):
    class Arguments:
        input = RegisterInput(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        try:
            # 验证密码
            validate_password(input.password)
            
            # 检查用户名是否已存在
            if User.objects.filter(username=input.username).exists():
                return RegisterMutation(success=False, errors=['用户名已存在'])
            
            # 检查邮箱是否已存在
            if User.objects.filter(email=input.email).exists():
                return RegisterMutation(success=False, errors=['邮箱已被注册'])
            
            # 创建用户
            user = User.objects.create_user(
                username=input.username,
                email=input.email,
                password=input.password,
                first_name=input.first_name or '',
                last_name=input.last_name or ''
            )
            
            # 发送验证邮件
            current_site = get_current_site(info.context)
            subject = '激活您的账号'
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            
            return RegisterMutation(success=True, errors=None)
        except ValidationError as e:
            return RegisterMutation(success=False, errors=list(e.messages))
        except Exception as e:
            return RegisterMutation(success=False, errors=[str(e)])

class SendVerificationCodeMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email):
        try:
            # 生成验证码
            code = generate_verification_code()
            
            # 存储验证码（15分钟有效）
            cache_key = f'verification_code_{email}'
            cache.set(cache_key, code, 900)  # 15分钟 = 900秒
            
            # 发送验证码
            send_verification_code(email, code)
            
            return SendVerificationCodeMutation(success=True, errors=None)
        except Exception as e:
            return SendVerificationCodeMutation(success=False, errors=[str(e)])

class VerifyEmailMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        code = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email, code):
        try:
            # 获取存储的验证码
            cache_key = f'verification_code_{email}'
            stored_code = cache.get(cache_key)
            
            if not stored_code:
                return VerifyEmailMutation(success=False, errors=['验证码已过期'])
            
            if code != stored_code:
                return VerifyEmailMutation(success=False, errors=['验证码错误'])
            
            # 验证成功后删除验证码
            cache.delete(cache_key)
            
            return VerifyEmailMutation(success=True, errors=None)
        except Exception as e:
            return VerifyEmailMutation(success=False, errors=[str(e)])

class ResetPasswordMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
            
            # 生成重置密码的token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # 发送重置密码邮件
            current_site = get_current_site(info.context)
            subject = '重置密码'
            message = render_to_string('user/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            
            return ResetPasswordMutation(success=True, errors=None)
        except User.DoesNotExist:
            return ResetPasswordMutation(success=False, errors=['用户不存在'])
        except Exception as e:
            return ResetPasswordMutation(success=False, errors=[str(e)])

class SetNewPasswordMutation(graphene.Mutation):
    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, uid, token, new_password):
        try:
            # 验证密码
            validate_password(new_password)
            
            # 解码用户ID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            
            # 验证token
            if not default_token_generator.check_token(user, token):
                return SetNewPasswordMutation(success=False, errors=['无效的token'])
            
            # 设置新密码
            user.set_password(new_password)
            user.save()
            
            return SetNewPasswordMutation(success=True, errors=None)
        except (TypeError, ValueError, User.DoesNotExist):
            return SetNewPasswordMutation(success=False, errors=['无效的链接'])
        except ValidationError as e:
            return SetNewPasswordMutation(success=False, errors=list(e.messages))
        except Exception as e:
            return SetNewPasswordMutation(success=False, errors=[str(e)])

class Mutation(graphene.ObjectType):
    register = RegisterMutation.Field()
    send_verification_code = SendVerificationCodeMutation.Field()
    verify_email = VerifyEmailMutation.Field()
    reset_password = ResetPasswordMutation.Field()
    set_new_password = SetNewPasswordMutation.Field()

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user

schema = graphene.Schema(query=Query, mutation=Mutation) 