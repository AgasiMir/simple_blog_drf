from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, TagDetailView

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path('tags/<str:tag_slug>/', TagDetailView.as_view())
] + router.urls
