import os.path

from django.conf import settings as django_settings
from django.db import models
from django.db.models import signals
from django.utils.translation import gettext, gettext_lazy as _
from wiki.models.pluginbase import RevisionPlugin, RevisionPluginRevision
from . import settings


def upload_path(instance, filename):
    # Has to match original extension filename

    upload_path = settings.IMAGE_PATH
    upload_path = upload_path.replace(
        '%aid', str(instance.plugin.image.article.id))
    if settings.IMAGE_PATH_OBSCURIFY:
        import uuid
        upload_path = os.path.join(upload_path, uuid.uuid4().hex)
    return os.path.join(upload_path, filename)


class Video(RevisionPlugin):

    # The plugin system is so awesome that the inheritor doesn't need to do
    # anything! :D

    def can_write(self, user):
        if not settings.ANONYMOUS and (not user or user.is_anonymous):
            return False
        return RevisionPlugin.can_write(self, user)

    def can_delete(self, user):
        return self.can_write(user)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        db_table = 'wiki_videos_video'  # Matches label of upcoming 0.1 release

    def __str__(self):
        if self.current_revision:
            return gettext('Video: %s') % self.current_revision.videorevision.get_filename()
        else:
            return gettext('Current revision not set!!')


class VideoRevision(RevisionPluginRevision):

    video = models.FileField(
        upload_to=upload_path,
        max_length=2000,
        blank=True,
        null=True,
        storage=settings.STORAGE_BACKEND
    )

    def get_filename(self):
        if self.video:
            try:
                return self.video.name.split('/')[-1]
            except OSError:
                pass
        return None

    def get_size(self):
        """Used to retrieve the file size and not cause exceptions."""
        try:
            return self.video.size
        except (ValueError, OSError):
            return None

    def inherit_predecessor(self, video, skip_video_file=False):
        """
        Inherit certain properties from predecessor because it's very
        convenient. Remember to always call this method before
        setting properties :)

        A revision may not have a predecessor if the property is unset, it may
        be unset if it's the initial history entry.
        """
        predecessor = video.current_revision.videorevision
        super().inherit_predecessor(video)
        self.plugin = predecessor.plugin
        self.deleted = predecessor.deleted
        self.locked = predecessor.locked
        if not skip_video_file:
            try:
                self.video = predecessor.video
            except IOError:
                self.video = None

    class Meta:
        verbose_name = _('video revision')
        verbose_name_plural = _('video revisions')
        # Matches label of upcoming 0.1 release
        db_table = 'wiki_videos_videorevision'
        ordering = ('-created',)

    def __str__(self):
        return gettext('Video Revision: %d') % self.revision_number


def on_video_revision_delete(instance, *args, **kwargs):
    if not instance.video:
        return

    # Remove video file
    instance.video.delete(save=False)

    try:
        path = instance.video.path.split("/")[:-1]
    except NotImplementedError:
            # This backend storage doesn't implement 'path' so there is no
            # path to delete
        return

    # Clean up empty directories

    # Check for empty folders in the path. Delete the first two.
    if len(path[-1]) == 32:
        # Path was (most likely) obscurified so we should look 2 levels down
        max_depth = 2
    else:
        max_depth = 1
    for depth in range(0, max_depth):
        delete_path = "/".join(path[:-depth] if depth > 0 else path)
        try:
            dir_list = os.listdir(
                os.path.join(django_settings.MEDIA_ROOT, delete_path))
        except OSError:
            # Path does not exist, so let's not try to remove it...
            dir_list = None
        if not (dir_list is None) and len(dir_list) == 0:
            os.rmdir(delete_path)


signals.pre_delete.connect(on_video_revision_delete, VideoRevision)
