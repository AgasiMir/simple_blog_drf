from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, TagDetailView, TagView

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("tags/", TagView.as_view()),
    path('tags/<str:tag_slug>/', TagDetailView.as_view())
] + router.urls
