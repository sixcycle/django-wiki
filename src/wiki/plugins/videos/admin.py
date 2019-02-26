from django import forms
from django.contrib import admin

from . import models


class VideoForm(forms.ModelForm):

    class Meta:
        model = models.Video
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            revisions = models.VideoRevision.objects.filter(
                plugin=self.instance)
            self.fields['current_revision'].queryset = revisions
        else:
            self.fields[
                'current_revision'].queryset = models.VideoRevision.objects.none()
            self.fields['current_revision'].widget = forms.HiddenInput()


class VideoRevisionInline(admin.TabularInline):
    model = models.VideoRevision
    extra = 1
    fields = ('video', 'locked', 'deleted')


class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    inlines = (VideoRevisionInline,)


admin.site.register(models.Video, VideoAdmin)
