from django.contrib import admin
from .models import User, Location, Family, Relationship

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'first_name', 'last_name', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'phone', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'is_staff', 'gender')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude', 'address')
    search_fields = ('address',)

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('family_code', 'name', 'location')
    search_fields = ('family_code', 'name')
    list_filter = ('location',)

@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'relationship_type', 'status', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('relationship_type', 'status')
