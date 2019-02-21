from authtools.models import AbstractEmailUser


class ProxyUser(AbstractEmailUser):
    class Meta:
        db_table = 'profiles_user'
        app_label = 'authentication'
