from rest_framework import serializers
from django.contrib.auth import get_user_model
from taggit.serializers import TagListSerializerField, TaggitSerializer

from taggit.models import Tag
from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tag = TagListSerializerField()
    author = serializers.SlugRelatedField(
        slug_field="username", queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Post
        fields = "__all__"
        lookup_field = "slug"
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]
        lookup_field = "name"
        extra_kwargs = {"url": {"lookup_field": "name"}}
