import graphene
from user.graphql.types import RelationshipType, UserType, FamilyType, LocationType
from user.models import Relationship, User, Family, Location


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
    
    示例3 - 分页获取用户列表:
    query {
        allUsers(page: 1, pageSize: 10) {
            data {
                id
                username
                first_name
                last_name
            }
            pageInfo {
                currentPage
                pageSize
                total
                totalPages
                hasNextPage
                hasPreviousPage
            }
        }
    }
    """    
    all_users = graphene.Field(
        graphene.List(UserType),
        offset=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=10)
    )
    all_families = graphene.Field(
        graphene.List(FamilyType),
        offset=graphene.Int(default_value=0), 
        limit=graphene.Int(default_value=10)
    )
    all_locations = graphene.Field(
        graphene.List(LocationType),
        offset=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=10)
    )
    all_relationships = graphene.Field(
        graphene.List(RelationshipType),
        user_id=graphene.ID(required=True),
        offset=graphene.Int(default_value=0),
        limit=graphene.Int(default_value=10)
    )
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    family = graphene.Field(FamilyType, id=graphene.ID(required=True))
    location = graphene.Field(LocationType, id=graphene.ID(required=True))
    relationship = graphene.Field(RelationshipType, id=graphene.ID(required=True))

    def resolve_all_users(self, info, offset=0, limit=10):
        return User.objects.all()[offset:offset+limit]

    def resolve_all_families(self, info, offset=0, limit=10):
        return Family.objects.all()[offset:offset+limit]

    def resolve_all_locations(self, info, offset=0, limit=10):
        return Location.objects.all()[offset:offset+limit]

    def resolve_all_relationships(self, info, user_id, offset=0, limit=10):
        return Relationship.objects.filter(user_id=user_id)[offset:offset+limit]

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    def resolve_family(self, info, id):
        return Family.objects.get(family_id=id)

    def resolve_location(self, info, id):
        return Location.objects.get(pk=id)

    def resolve_relationship(self, info, id):
        return Relationship.objects.get(pk=id)