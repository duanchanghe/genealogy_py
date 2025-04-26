import graphene
from user.graphql.types import RelationshipType, UserType, FamilyType, LocationType
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from user.graphql.types import UserFilter, FamilyFilter, LocationFilter, RelationshipFilter

class RelayQuery(graphene.ObjectType):

    all_users = DjangoFilterConnectionField(UserType, filterset_class=UserFilter)
    user = relay.Node.Field(UserType)

    all_families = DjangoFilterConnectionField(FamilyType, filterset_class=FamilyFilter)
    family = relay.Node.Field(FamilyType)

    all_locations = DjangoFilterConnectionField(LocationType, filterset_class=LocationFilter)
    location = relay.Node.Field(LocationType)

    all_relationships = DjangoFilterConnectionField(RelationshipType, filterset_class=RelationshipFilter)
    relationship = relay.Node.Field(RelationshipType)
