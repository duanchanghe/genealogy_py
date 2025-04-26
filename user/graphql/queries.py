import graphene
from user.graphql.types import UserType, FamilyType, LocationType
from user.models import User, Family, Location

class UserQuery(graphene.ObjectType):
    """
    GraphQL查询
    
    示例1 - 获取所有用户:
    query {
        allUsers {
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
    
    示例2 - 获取单个用户:
    query {
        user(id: "1") {
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
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())
    all_families = graphene.List(FamilyType)
    family = graphene.Field(FamilyType, family_id=graphene.ID())
    all_locations = graphene.List(LocationType)
    location = graphene.Field(LocationType, id=graphene.ID())

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)
        
    def resolve_all_families(self, info):
        return Family.objects.all()
        
    def resolve_family(self, info, family_id):
        return Family.objects.get(family_id=family_id)
        
    def resolve_all_locations(self, info):
        return Location.objects.all()
        
    def resolve_location(self, info, id):
        return Location.objects.get(pk=id) 