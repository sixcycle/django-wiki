from authtools.models import AbstractEmailUser
from django.db import models


class User(AbstractEmailUser):
    profile_picture_url = models.URLField()
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'profiles_user'
        app_label = 'authentication'


class Organization(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField(blank=True)
    paymentPlan = models.CharField(max_length=255, blank=True)
    isOrgPaying = models.BooleanField(default=True)
    profilepicture = models.URLField(
        blank=True,
        default='https://s3.amazonaws.com/sixcycle/customAssets/placeholder-avatar-group.png'
    )
    template_prefix = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'profiles_organization'
        app_label = 'authentication'


class OrgUserRelationship(models.Model):
    user = models.ForeignKey(User, related_name='OrgUserRelationship')
    organization = models.ForeignKey(
        Organization,
        related_name='OrgUserRelationship'
        )
    uniqueId = models.CharField(max_length=255, blank=False)

    class Meta:
        db_table = 'profiles_orguserrelationship'
        app_label = 'authentication'
