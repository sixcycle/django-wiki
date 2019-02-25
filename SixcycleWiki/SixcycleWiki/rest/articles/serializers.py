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
    owner = serializers.SerializerMethodField()
    created = serializers.DateTimeField()
    modified = serializers.DateTimeField()

    def get_owner(self, obj):
        if obj.owner:
            return {
                'email': obj.owner.email,
                'profile_picture_url': obj.owner.profile_picture_url
            }
        return {}
