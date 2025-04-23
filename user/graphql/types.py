from graphene_django import DjangoObjectType
from user.models import User, Location

class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude', 'address')

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'birthday', 'death_date', 'milk_name', 
                 'birth_place', 'burial_place', 'phone', 'date_joined', 
                 'father', 'mother', 'spouses') 