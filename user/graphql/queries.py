import graphene
from user.graphql.types import UserType
from user.models import User

class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID())

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id) 