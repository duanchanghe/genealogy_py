import graphene
from user.graphql.types import UserType
from user.models import User

class UserQuery(graphene.ObjectType):
    """
    GraphQL查询
    
    示例1 - 获取所有用户:
    query {
        allUsers {
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
    
    示例2 - 获取单个用户:
    query {
        user(id: "1") {
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
    """
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id) 