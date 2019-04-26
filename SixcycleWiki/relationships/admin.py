from django.contrib import admin
from relationships.models import *
# Register your models here.

admin.site.register(OrganizationReadArticle)
admin.site.register(OrganizationEditArticle)
admin.site.register(GroupReadArticle)
admin.site.register(GroupEditArticle)
admin.site.register(UserReadArticle)
admin.site.register(UserEditArticle)
