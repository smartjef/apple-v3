from django.contrib import admin
from .models import UserProfile, ResidentialInfo, Team

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'description', 'phone')
    search_fields = ('user', 'description', 'phone')
    raw_id_fields = ('user',)


@admin.register(ResidentialInfo)
class ResidentialInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'zip_code', 'apartment_or_floor', 'country', 'postal_code')
    list_filter = ('user', 'country')
    search_fields = ('user', 'address', 'city', 'zip_code', 'apartment_or_floor', 'country', 'postal_code')
    raw_id_fields = ('user',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'image', 'order')
    list_filter = ('is_active',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)

