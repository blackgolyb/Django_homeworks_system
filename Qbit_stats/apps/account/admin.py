from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User, Groups_of_users


class AdminUser(UserAdmin):
    list_display = ('username', 'email', 'full_name', 'dob', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'id')
    search_fields = ('username', 'email', 'full_name', 'dob')
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(User, AdminUser)
admin.site.register(Groups_of_users)
