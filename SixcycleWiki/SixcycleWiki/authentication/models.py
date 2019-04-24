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

    def __str__(self):
        # This is required since the 'Team and Training' Organization is saved
        # in our table as 'TNT' I have no idea what changing the name will do
        # to the core product, so its probably safer just to have an edge case
        # here based on the ID of the organization.
        if self.id == 10:
            return "Team and Training"
        else:
            return "{}".format(
                self.name
            )


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


class Group(models.Model):
    name = models.CharField('name', max_length=255, blank=True)

    class Meta:
        db_table = 'profiles_group'
        app_label = 'authentication'


class GroupMemberRelation(models.Model):
    user = models.ForeignKey(User, related_name='GroupMemberRelation')
    group = models.ForeignKey(Group, related_name='GroupMemberRelation')

    class Meta:
        db_table = 'profiles_groupmemberrelation'
        app_label = 'authentication'
