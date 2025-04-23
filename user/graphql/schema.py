import graphene
from user.graphql.queries import UserQuery
from user.graphql.mutations import UserMutation

class Query(UserQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation) 