from django.db import models
from SixcycleWiki.authentication.models import User, Organization

# Create your models here.


class OrganizationAdmins(models.Model):
    user = models.ForeignKey(
        User
    )
    organization = models.ForeignKey(
        Organization
    )
