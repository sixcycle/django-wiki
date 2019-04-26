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


class AllowedUsers(models.Model):
    '''
        Table meant to represent the list of users who have access to the
        contents of the wiki during the content production phase
    '''
    user = models.ForeignKey(
        User
    )
