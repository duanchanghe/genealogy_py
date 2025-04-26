import graphene
from graphql_jwt.decorators import login_required
from user.graphql.types import UserType, LocationType
from user.models import User, Location

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

class CreateUser(graphene.Mutation):
    """
    创建用户
    
    示例:
    mutation {
        createUser(
            username: "张三"
            password: "password123"
            email: "zhangsan@example.com"
            birthday: "1990-01-01"
            milkName: "小张"
            phone: "13800138000"
            birthPlaceId: "1"
            fatherId: "2"
            motherId: "3"
            spouseIds: ["4", "5"]
        ) {
            user {
                id
                username
                email
                phone
                birthday
                milkName
                birthPlace {
                    id
                    latitude
                    longitude
                    address
                }
                father {
                    id
                    username
                }
                mother {
                    id
                    username
                }
                spouses {
                    id
                    username
                }
            }
        }
    }
    """
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String()
        birthday = graphene.Date()
        death_date = graphene.Date()
        milk_name = graphene.String()
        birth_place_id = graphene.ID()
        burial_place_id = graphene.ID()
        phone = graphene.String()
        father_id = graphene.ID()
        mother_id = graphene.ID()
        spouse_ids = graphene.List(graphene.ID)

    user = graphene.Field(UserType)

    def mutate(self, info, username, password, email=None, birthday=None, death_date=None,
               milk_name=None, birth_place_id=None, burial_place_id=None, phone=None,
               father_id=None, mother_id=None, spouse_ids=None):
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            birthday=birthday,
            death_date=death_date,
            milk_name=milk_name,
            phone=phone
        )
        
        if birth_place_id:
            user.birth_place = Location.objects.get(pk=birth_place_id)
        if burial_place_id:
            user.burial_place = Location.objects.get(pk=burial_place_id)
        if father_id:
            user.father = User.objects.get(pk=father_id)
        if mother_id:
            user.mother = User.objects.get(pk=mother_id)
        if spouse_ids:
            spouses = User.objects.filter(pk__in=spouse_ids)
            user.spouses.set(spouses)
            
        user.save()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    """
    更新用户信息
    
    示例:
    mutation {
        updateUser(
            id: "1"
            email: "new.email@example.com"
            phone: "13900139000"
            milkName: "新乳名"
            birthPlaceId: "2"
            fatherId: "3"
            motherId: "4"
            spouseIds: ["5", "6"]
        ) {
            user {
                id
                username
                email
                phone
                milkName
                birthPlace {
                    id
                    latitude
                    longitude
                    address
                }
                father {
                    id
                    username
                }
                mother {
                    id
                    username
                }
                spouses {
                    id
                    username
                }
            }
        }
    }
    
    注意: 此操作需要登录认证
    """
    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String()
        birthday = graphene.Date()
        death_date = graphene.Date()
        milk_name = graphene.String()
        birth_place_id = graphene.ID()
        burial_place_id = graphene.ID()
        phone = graphene.String()
        father_id = graphene.ID()
        mother_id = graphene.ID()
        spouse_ids = graphene.List(graphene.ID)

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, id, email=None, birthday=None, death_date=None,
               milk_name=None, birth_place_id=None, burial_place_id=None, phone=None,
               father_id=None, mother_id=None, spouse_ids=None):
        user = User.objects.get(pk=id)
        if email:
            user.email = email
        if birthday:
            user.birthday = birthday
        if death_date:
            user.death_date = death_date
        if milk_name:
            user.milk_name = milk_name
        if phone:
            user.phone = phone
        if birth_place_id:
            user.birth_place = Location.objects.get(pk=birth_place_id)
        if burial_place_id:
            user.burial_place = Location.objects.get(pk=burial_place_id)
        if father_id:
            user.father = User.objects.get(pk=father_id)
        if mother_id:
            user.mother = User.objects.get(pk=mother_id)
        if spouse_ids is not None:
            spouses = User.objects.filter(pk__in=spouse_ids)
            user.spouses.set(spouses)
            
        user.save()
        return UpdateUser(user=user)

class UserMutation(graphene.ObjectType):
    create_location = CreateLocation.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field() 