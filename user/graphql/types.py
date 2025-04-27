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
        fields = ('family_id', 'family_code', 'name', 'description', 'location')

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 
                 'is_active', 'date_joined', 'birth_date', 'death_date', 'milk_name', 
                 'birth_place', 'burial_place', 'phone', 'family', 'gender') 

class RelationshipType(DjangoObjectType):
    class Meta:
        model = Relationship
        fields = ('id', 'user', 'relative', 'relationship_type')

class AuthResponse(graphene.ObjectType):
    """认证响应类型"""
    token = graphene.String()
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)





