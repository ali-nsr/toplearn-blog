from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import *


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'created_date', 'role']
    list_filter = ['email']
    fieldsets = (
        ('user', {'fields': ('email', 'password')}),
        ('user information', {'fields': ('first_name', 'last_name','image')}),
        ('user access', {'fields': ('is_active', 'role')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'is_active')}),
    )
    search_fields = ['email']
    ordering = ['-created_date']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
