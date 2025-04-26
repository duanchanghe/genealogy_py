import graphene
from graphql_jwt.decorators import login_required
from user.graphql.types import UserType, LocationType, FamilyType
from user.models import User, Location, Family

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

class UserMutation(graphene.ObjectType):
    create_location = CreateLocation.Field()
    create_family = CreateFamily.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
