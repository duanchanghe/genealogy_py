import graphene
from graphql_jwt.decorators import login_required
from user.graphql.types import UserType, LocationType, FamilyType, AuthResponse
from user.models import User, Location, Family
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.hashers import make_password
from graphql_jwt.shortcuts import get_token
from user.graphql.utils import (
    generate_verification_code,
    validate_phone,
    save_verification_code,
    verify_code,
    validate_password
)

User = get_user_model()

class CreateLocation(graphene.Mutation):
    """
    创建位置
    
    示例:
    mutation {
        createLocation(
            latitude: "39.9042"
            longitude: "116.4074"
            address: "北京市东城区"
        ) {
            location {
                id
                latitude
                longitude
                address
            }
        }
    }
    """
    class Arguments:
        latitude = graphene.Decimal(required=True)
        longitude = graphene.Decimal(required=True)
        address = graphene.String()

    location = graphene.Field(LocationType)

    def mutate(self, info, latitude, longitude, address=None):
        location = Location.objects.create(
            latitude=latitude,
            longitude=longitude,
            address=address
        )
        return CreateLocation(location=location)

class CreateFamily(graphene.Mutation):
    """
    创建家族
    
    示例:
    mutation {
        createFamily(
            familyCode: "FAM001"
            name: "张氏家族"
            description: "张氏家族描述"
            locationId: "1"
        ) {
            family {
                family_id
                family_code
                name
                description
                location {
                    id
                    latitude
                    longitude
                    address
                }
            }
        }
    }
    """
    class Arguments:
        family_code = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        location_id = graphene.ID()

    family = graphene.Field(FamilyType)

    def mutate(self, info, family_code, name, description=None, location_id=None):
        family = Family.objects.create(
            family_code=family_code,
            name=name,
            description=description
        )
        
        if location_id:
            family.location = Location.objects.get(pk=location_id)
            family.save()
            
        return CreateFamily(family=family)

class CreateUser(graphene.Mutation):
    """
    创建用户
    
    示例:
    mutation {
        createUser(
            username: "张三"
            password: "password123"
            firstName: "三"
            lastName: "张"
            email: "zhangsan@example.com"
            birthDate: "1990-01-01"
            deathDate: null
            milkName: "小张"
            phone: "13800138000"
            gender: "male"
            birthPlaceId: "1"
            burialPlaceId: null
            familyId: "1"
        ) {
            user {
                id
                username
                first_name
                last_name
                email
                phone
                birth_date
                death_date
                milk_name
                gender
                birth_place {
                    id
                    latitude
                    longitude
                    address
                }
                burial_place {
                    id
                    latitude
                    longitude
                    address
                }
                family {
                    family_id
                    family_code
                    name
                }
            }
        }
    }
    """
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()
        death_date = graphene.Date()
        milk_name = graphene.String()
        birth_place_id = graphene.ID()
        burial_place_id = graphene.ID()
        phone = graphene.String()
        gender = graphene.String()
        family_id = graphene.ID()

    user = graphene.Field(UserType)

    def mutate(self, info, username, password, first_name=None, last_name=None, 
               email=None, birth_date=None, death_date=None, milk_name=None, 
               birth_place_id=None, burial_place_id=None, phone=None, 
               gender=None, family_id=None):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            birth_date=birth_date,
            death_date=death_date,
            milk_name=milk_name,
            phone=phone,
            gender=gender
        )
        
        if birth_place_id:
            user.birth_place = Location.objects.get(pk=birth_place_id)
        if burial_place_id:
            user.burial_place = Location.objects.get(pk=burial_place_id)
        if family_id:
            user.family = Family.objects.get(family_id=family_id)
            
        user.save()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    """
    更新用户信息
    
    示例:
    mutation {
        updateUser(
            id: "1"
            firstName: "三"
            lastName: "张"
            email: "new.email@example.com"
            birthDate: "1990-01-01"
            deathDate: null
            milkName: "新乳名"
            phone: "13900139000"
            gender: "male"
            birthPlaceId: "2"
            burialPlaceId: null
            familyId: "1"
        ) {
            user {
                id
                username
                first_name
                last_name
                email
                phone
                birth_date
                death_date
                milk_name
                gender
                birth_place {
                    id
                    latitude
                    longitude
                    address
                }
                burial_place {
                    id
                    latitude
                    longitude
                    address
                }
                family {
                    family_id
                    family_code
                    name
                }
            }
        }
    }
    
    注意: 此操作需要登录认证
    """
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()
        death_date = graphene.Date()
        milk_name = graphene.String()
        birth_place_id = graphene.ID()
        burial_place_id = graphene.ID()
        phone = graphene.String()
        gender = graphene.String()
        family_id = graphene.ID()

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, id, first_name=None, last_name=None, email=None, 
               birth_date=None, death_date=None, milk_name=None, 
               birth_place_id=None, burial_place_id=None, phone=None, 
               gender=None, family_id=None):
        user = User.objects.get(pk=id)
        
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        if birth_date is not None:
            user.birth_date = birth_date
        if death_date is not None:
            user.death_date = death_date
        if milk_name is not None:
            user.milk_name = milk_name
        if phone is not None:
            user.phone = phone
        if gender is not None:
            user.gender = gender
            
        if birth_place_id is not None:
            if birth_place_id:
                user.birth_place = Location.objects.get(pk=birth_place_id)
            else:
                user.birth_place = None
                
        if burial_place_id is not None:
            if burial_place_id:
                user.burial_place = Location.objects.get(pk=burial_place_id)
            else:
                user.burial_place = None
                
        if family_id is not None:
            if family_id:
                user.family = Family.objects.get(family_id=family_id)
            else:
                user.family = None
                
        user.save()
        return UpdateUser(user=user)

class SendVerificationCode(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, phone):
        if not validate_phone(phone):
            return SendVerificationCode(success=False, errors=["无效的手机号格式"])

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = User(phone=phone)
        
        code = generate_verification_code()
        user.save_verification_code(code)
        
        # TODO: 在实际生产环境中，这里应该调用短信服务发送验证码
        print(f"验证码: {code}")  # 仅用于测试
        
        return SendVerificationCode(success=True, errors=None)

class RegisterWithPhone(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        code = graphene.String(required=True)
        password = graphene.String(required=True)
        username = graphene.String()

    Output = AuthResponse

    def mutate(self, info, phone, code, password, username=None):
        if not validate_phone(phone):
            return AuthResponse(success=False, errors=["无效的手机号格式"])

        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            return AuthResponse(success=False, errors=[password_error])

        try:
            user = User.objects.get(phone=phone)
            if user.is_active:
                return AuthResponse(success=False, errors=["该手机号已注册"])
        except User.DoesNotExist:
            user = User(phone=phone)

        if not user.verify_code(code):
            return AuthResponse(success=False, errors=["验证码无效或已过期"])

        if not username:
            username = phone

        user.username = username
        user.set_password(password)
        user.is_active = True
        user.verification_code = None
        user.verification_code_expires = None
        user.save()

        # 生成token并登录
        token = get_token(user)
        login(info.context, user)

        return AuthResponse(success=True, errors=None, user=user, token=token)

class LoginWithPhone(graphene.Mutation):
    class Arguments:
        phone = graphene.String(required=True)
        code = graphene.String(required=True)

    Output = AuthResponse

    def mutate(self, info, phone, code):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return AuthResponse(success=False, errors=["用户不存在"])

        if not user.is_active:
            return AuthResponse(success=False, errors=["账号已被禁用"])

        if not user.verify_code(code):
            return AuthResponse(success=False, errors=["验证码无效或已过期"])

        user.verification_code = None
        user.verification_code_expires = None
        user.save()

        # 生成token并登录
        token = get_token(user)
        login(info.context, user)

        return AuthResponse(success=True, errors=None, user=user, token=token)

class Logout(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        if info.context.user.is_authenticated:
            logout(info.context)
            return Logout(success=True)
        return Logout(success=False)

class UserMutation(graphene.ObjectType):
    create_location = CreateLocation.Field()
    create_family = CreateFamily.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    send_verification_code = SendVerificationCode.Field()
    register_with_phone = RegisterWithPhone.Field()
    login_with_phone = LoginWithPhone.Field()
    logout = Logout.Field()
