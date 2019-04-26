from django.contrib import admin
from dashboard.models import OrganizationAdmins, AllowedUsers
# Register your models here.

admin.site.register(OrganizationAdmins)


class AllowedUsersAdmin(admin.ModelAdmin):
    search_fields = ['user_email']

admin.site.register(AllowedUsers, AllowedUsersAdmin)
