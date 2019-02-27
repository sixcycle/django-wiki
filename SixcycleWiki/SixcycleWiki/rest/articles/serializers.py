from rest_framework import serializers
from wiki.models.article import Article


class ArticleSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        source='current_revision.title'
    )
    content = serializers.CharField(
        source='current_revision.content'
    )
    summary = serializers.CharField(
        source='current_revision.user_message'
    )
    owner = serializers.SerializerMethodField()
    created = serializers.DateTimeField()
    modified = serializers.DateTimeField()
    slug = serializers.SerializerMethodField()

    def get_owner(self, obj):
        if obj.owner:
            return {
                'email': obj.owner.email,
                'profile_picture_url': obj.owner.profile_picture_url,
                'name': obj.owner.name
            }
        return {}

    def get_slug(self, obj):
        return obj.get_absolute_url()
