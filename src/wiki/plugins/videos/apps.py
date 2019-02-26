from django.apps import AppConfig
from django.core.checks import register
from django.utils.translation import gettext_lazy as _


class VideosConfig(AppConfig):
    name = 'wiki.plugins.videos'
    verbose_name = _("Wiki videos")
    label = 'wiki_videos'
