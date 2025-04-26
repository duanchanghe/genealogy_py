import graphene
from user.graphql.queries import RelayQuery
from user.graphql.mutations import UserMutation

class Query(RelayQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation) 