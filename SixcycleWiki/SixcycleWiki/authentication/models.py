from authtools.models import AbstractEmailUser


class User(AbstractEmailUser):
    class Meta:
        db_table = 'profiles_user'
        app_label = 'authentication'
