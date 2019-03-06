import markdown
from django.template.loader import render_to_string
from wiki.plugins.videos import models, settings

VIDEO_RE = (
    r"(?:(?im)" +
    # Match '[image:N'
    r"\[video\:(?P<id>[0-9]+)" +
    # Match optional 'align'
    r"(?:\s+align\:(?P<align>right|left))?" +
    # Match optional 'size'
    r"(?:\s+size\:(?P<size>default|small|medium|large|orig))?" +
    # Match ']' and rest of line.
    # Normally [^\n] could be replaced with a dot '.', since '.'
    # does not match newlines, but inline processors run with re.DOTALL.
    r"\s*\](?P<trailer>[^\n]*)$" +
    # Match zero or more caption lines, each indented by four spaces.
    r"(?P<caption>(?:\n    [^\n]*)*))"
)


class VideoExtension(markdown.Extension):

    """ Images plugin markdown extension for django-wiki. """

    def extendMarkdown(self, md):
        md.inlinePatterns.add('dw-videos', VideoPattern(VIDEO_RE, md), '>link')
        md.postprocessors.add('dw-videos-cleanup', VideoPostprocessor(md), '>raw_html')


class VideoPattern(markdown.inlinepatterns.Pattern):
    """
    django-wiki video preprocessor
    Parse text for [video:N] references.

    For instance:

    [video:id]
        This is the caption text maybe with [a link](...)

    So: Remember that the caption text is fully valid markdown!
    """

    def handleMatch(self, m):
        video = None
        video_id = None
        video_id = m.group("id").strip()
        try:
            video = models.Video.objects.get(
                article=self.markdown.article,
                id=video_id,
                current_revision__deleted=False,
            )
        except models.Video.DoesNotExist:
            pass
        video_url = settings.MEDIA_URL + video.current_revision.videorevision.video.name
        caption = m.group("caption")
        trailer = m.group('trailer')
        if not caption:
            caption_placeholder = None
        else:
            caption_placeholder = caption
        html = render_to_string(
            "wiki/plugins/videos/render.html",
            context={
                "video": video,
                "caption": caption_placeholder,
                "video_url": video_url
            },
        )
        return self.markdown.htmlStash.store(html)
        # html_before, html_after = html.split(caption_placeholder)
        # placeholder_before = self.markdown.htmlStash.store(html_before)
        # placeholder_after = self.markdown.htmlStash.store(html_after)
        # return placeholder_before + caption + placeholder_after + trailer


class VideoPostprocessor(markdown.postprocessors.Postprocessor):

    def run(self, text):
        """
        This cleans up after Markdown's well-intended placing of image tags
        inside <p> elements. The problem is that Markdown should put
        <p> tags around images as they are inline elements. However, because
        we wrap them in <figure>, we don't actually want it and have to
        remove it again after.
        """
        text = text.replace("<p>\n<video", "<video")
        text = text.replace("</video>\n</p>", "</video>")
        return text
