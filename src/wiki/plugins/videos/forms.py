from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from wiki.core.plugins.base import PluginSidebarFormMixin
from wiki.plugins.videos import models


class SidebarForm(PluginSidebarFormMixin):

    def __init__(self, article, request, *args, **kwargs):
        self.article = article
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['video'].required = True

    def get_usermessage(self):
        return gettext(
            "New video %s was successfully uploaded. You can use it by selecting it from the list of available videos.") % self.instance.get_filename()

    def save(self, *args, **kwargs):
        if not self.instance.id:
            video = models.Video()
            video.article = self.article
            kwargs['commit'] = False
            revision = super().save(*args, **kwargs)
            revision.set_from_request(self.request)
            video.add_revision(self.instance, save=True)
            return revision
        return super().save(*args, **kwargs)

    class Meta:
        model = models.VideoRevision
        fields = ('video',)


class RevisionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.video = kwargs.pop('video')
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['video'].required = True

    def save(self, *args, **kwargs):
        if not self.instance.id:
            kwargs['commit'] = False
            revision = super().save(*args, **kwargs)
            revision.inherit_predecessor(self.video, skip_video_file=True)
            revision.deleted = False  # Restore automatically if deleted
            revision.set_from_request(self.request)
            self.video.add_revision(self.instance, save=True)
            return revision
        return super().save(*args, **kwargs)

    class Meta:
        model = models.VideoRevision
        fields = ('video',)


class PurgeForm(forms.Form):

    confirm = forms.BooleanField(label=_('Are you sure?'), required=False)

    def clean_confirm(self):
        confirm = self.cleaned_data['confirm']
        if not confirm:
            raise forms.ValidationError(gettext('You are not sure enough!'))
        return confirm
