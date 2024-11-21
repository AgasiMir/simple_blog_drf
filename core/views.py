from django.core.exceptions import PermissionDenied
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import permissions, mixins, filters
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from taggit.models import Tag
from .serializers import (
    FeedbackSerializer,
    PostSerializer,
    RegisterSerializer,
    TagSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from .models import Feedback, Post


class PostViewSet(viewsets.ModelViewSet):
    search_fields = ["title"]
    filter_backends = [filters.SearchFilter]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "slug"
    # permission_classes = [permissions.IsAuthenticated]


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs["tag_slug"].lower())
        return Post.objects.filter(tag=tag)


class TagView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AsideView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()[:5]
    serializer_class = PostSerializer


class FeedbackView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterSerializer
        if self.action == "my_profile":
            return UserSerializer
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance != self.request.user:
            raise PermissionDenied("Отказано в доступе.")

        serializer.save()

    @action(detail=False, methods=["get"])
    def my_profile(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
