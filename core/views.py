from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import permissions

from .serializers import PostSerializer
from .models import Post
from taggit.models import Tag


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"
    # permission_classes = [permissions.IsAuthenticated]


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs["tag_slug"].lower())
        return Post.objects.filter(tag=tag)
