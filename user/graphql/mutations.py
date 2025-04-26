import graphene
from graphql_jwt.decorators import login_required
from user.graphql.types import UserType, LocationType, FamilyType
from user.models import User, Location, Family
from graphql_auth import mutations
from graphene.relay import ClientIDMutation

class CreateLocation(ClientIDMutation):
    class Input:
        latitude = graphene.Decimal(required=True)
        longitude = graphene.Decimal(required=True)
        address = graphene.String()

    location = graphene.Field(LocationType)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        location = Location.objects.create(
            latitude=input.get('latitude'),
            longitude=input.get('longitude'),
            address=input.get('address')
        )
        return CreateLocation(location=location)

class CreateFamily(ClientIDMutation):
    class Input:
        family_code = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        location_id = graphene.ID()

    family = graphene.Field(FamilyType)

    def mutate_and_get_payload(root, info, **input):
        family = Family.objects.create(
            family_code=input.get('family_code'),
            name=input.get('name'),
            description=input.get('description')
        )
        
        if input.get('location_id'):
            family.location = Location.objects.get(pk=input.get('location_id'))
            family.save()
            
        return CreateFamily(family=family)

class CreateUser(ClientIDMutation):
    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()
        death_date = graphene.Date()
        milk_name = graphene.String()
        birth_place_id = graphene.ID()
        burial_place_id = graphene.ID()
        phone = graphene.String()
        gender = graphene.String()

    user = graphene.Field(UserType)

    def mutate_and_get_payload(root, info, **input):
        user = User.objects.create_user(
            username=input.get('username'),
            password=input.get('password'),
            first_name=input.get('first_name'),
            last_name=input.get('last_name'),
            email=input.get('email'),
            birth_date=input.get('birth_date'),
            death_date=input.get('death_date'),
            milk_name=input.get('milk_name'),
            phone=input.get('phone'),
            gender=input.get('gender')
        )
        
        if input.get('birth_place_id'):
            user.birth_place = Location.objects.get(pk=input.get('birth_place_id'))
        if input.get('burial_place_id'):
            user.burial_place = Location.objects.get(pk=input.get('burial_place_id'))
            
        user.save()
        return CreateUser(user=user)

class UpdateUser(ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()
        death_date = graphene.Date()
        milk_name = graphene.String()
        birth_place_id = graphene.ID()
        burial_place_id = graphene.ID()
        phone = graphene.String()
        gender = graphene.String()

    user = graphene.Field(UserType)

    @login_required
    def mutate_and_get_payload(root, info, **input):
        user = User.objects.get(pk=input.get('id'))
        
        if input.get('first_name') is not None:
            user.first_name = input.get('first_name')
        if input.get('last_name') is not None:
            user.last_name = input.get('last_name')
        if input.get('email') is not None:
            user.email = input.get('email')
        if input.get('birth_date') is not None:
            user.birth_date = input.get('birth_date')
        if input.get('death_date') is not None:
            user.death_date = input.get('death_date')
        if input.get('milk_name') is not None:
            user.milk_name = input.get('milk_name')
        if input.get('phone') is not None:
            user.phone = input.get('phone')
        if input.get('gender') is not None:
            user.gender = input.get('gender')
            
        if input.get('birth_place_id') is not None:
            if input.get('birth_place_id'):
                user.birth_place = Location.objects.get(pk=input.get('birth_place_id'))
            else:
                user.birth_place = None
                
        if input.get('burial_place_id') is not None:
            if input.get('burial_place_id'):
                user.burial_place = Location.objects.get(pk=input.get('burial_place_id'))
            else:
                user.burial_place = None
                
            
        user.save()
        return UpdateUser(user=user)

class UserMutation(graphene.AbstractType):
    create_location = CreateLocation.Field()
    create_family = CreateFamily.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()

    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
