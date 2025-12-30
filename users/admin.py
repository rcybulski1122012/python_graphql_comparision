from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('avatar_color',)
    fieldsets = UserAdmin.fieldsets + (
        ('Appearance', {'fields': ('avatar_color',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Appearance', {'fields': ('avatar_color',)}),
    )
