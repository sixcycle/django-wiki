from authtools.models import AbstractEmailUser
from django.db import models


class User(AbstractEmailUser):
    profile_picture_url = models.URLField()
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'profiles_user'
        app_label = 'authentication'
