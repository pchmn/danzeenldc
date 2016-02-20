from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserAdminCustom(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Infos personnelles', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ('username', 'email')

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
