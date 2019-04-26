from django.contrib import admin
from dashboard.models import OrganizationAdmins, AllowedUsers
# Register your models here.

admin.site.register(OrganizationAdmins)


class AllowedUsersAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)

admin.site.register(AllowedUsers, AllowedUsersAdmin)
