from django.utils.translation import gettext as _
from wiki.compat import url
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.videos import forms, models, settings, views
from wiki.plugins.images.markdown_extensions import ImageExtension
from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.plugins.notifications.util import truncate_title


class VideoPlugin(BasePlugin):

    slug = settings.SLUG
    sidebar = {
        'headline': _('Videos'),
        'icon_class': 'fa fa-play',
        'template': 'wiki/plugins/videos/sidebar.html',
        'form_class': forms.SidebarForm,
        'get_form_kwargs': (lambda a: {'instance': models.Video(article=a)})
    }

    # List of notifications to construct signal handlers for. This
    # is handled inside the notifications plugin.
    notifications = [
        {'model': models.VideoRevision,
         'message': lambda obj: _("An image was added: %s") % truncate_title(obj.get_filename()),
         'key': ARTICLE_EDIT,
         'created': False,
         # Ignore if there is a previous revision... the image isn't new
         'ignore': lambda revision: bool(revision.previous_revision),
         'get_article': lambda obj: obj.article}
    ]

    class RenderMedia:
        js = [
            'wiki/colorbox/jquery.colorbox-min.js',
            'wiki/js/images.js',
        ]

        css = {
            'screen': 'wiki/colorbox/example1/colorbox.css'
        }

    urlpatterns = {'article': [
        url('^$',
            views.VideoView.as_view(),
            name='videos_index'),
        url('^delete/(?P<video_id>[0-9]+)/$',
            views.DeleteView.as_view(),
            name='videos_delete'),
        url('^restore/(?P<video_id>[0-9]+)/$',
            views.DeleteView.as_view(),
            name='videos_restore',
            kwargs={'restore': True}),
        url('^purge/(?P<video_id>[0-9]+)/$',
            views.PurgeView.as_view(),
            name='videos_purge'),
        url('^(?P<video_id>[0-9]+)/revision/change/(?P<rev_id>[0-9]+)/$',
            views.RevisionChangeView.as_view(),
            name='videos_set_revision'),
        url('^(?P<video_id>[0-9]+)/revision/add/$',
            views.RevisionAddView.as_view(),
            name='videos_add_revision'),
    ]}

    markdown_extensions = [ImageExtension()]


registry.register(VideoPlugin)
