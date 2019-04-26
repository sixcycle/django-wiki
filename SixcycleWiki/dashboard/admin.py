from django.contrib import admin
from dashboard.models import OrganizationAdmins, AllowedUsers
# Register your models here.

admin.site.register(OrganizationAdmins)


class AuthorAdmin(admin.ModelAdmin):
    search_files = ['user_email']

admin.site.register(AllowedUsers, AllowedUsersAdmin)
