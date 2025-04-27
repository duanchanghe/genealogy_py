from graphene_django import DjangoObjectType
from user.models import User, Location, Family, Relationship
import graphene

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude', 'address')

class FamilyType(DjangoObjectType):
    class Meta:
        model = Family
        fields = ('id', 'family_id', 'family_code', 'name', 'description', 'location')

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'location', 'family', 'is_active', 'is_staff') 

class RelationshipType(DjangoObjectType):
    class Meta:
        model = Relationship
        fields = ('id', 'user', 'related_user', 'relationship_type', 'start_date', 'end_date')

class AuthResponse(graphene.ObjectType):
    """认证响应类型"""
    token = graphene.String()
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)





