from graphene.relay import Node, Connection
from graphene_django import DjangoObjectType
from django_filters import FilterSet
from user.models import User, Location, Family, Relationship

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        interfaces = (Node,)

class LocationConnection(Connection):
    class Meta:
        node = LocationType

class FamilyType(DjangoObjectType):
    class Meta:
        model = Family
        interfaces = (Node,)

class FamilyConnection(Connection):
    class Meta:
        node = FamilyType

class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)

class UserConnection(Connection):
    class Meta:
        node = UserType

class RelationshipType(DjangoObjectType):
    class Meta:
        model = Relationship
        interfaces = (Node,)

class RelationshipConnection(Connection):
    class Meta:
        node = RelationshipType

class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']

class FamilyFilter(FilterSet):
    class Meta:
        model = Family
        fields = ['name', 'description']

class LocationFilter(FilterSet):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'address']

class RelationshipFilter(FilterSet):
    class Meta:
        model = Relationship
        fields = ['relationship_type']
