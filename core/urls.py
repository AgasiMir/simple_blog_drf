from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import FeedbackView, PostViewSet, TagDetailView, TagView, AsideView, UserViewSet


"""
Для того, чтобы AsideView можно было зарегистрировть в роутере,
необходимо, чтобы данный класс наследовался не от generics.ListAPIView,
а от mixins.ListModelMixin, viewsets.GenericViewSet. В противном случае,
AsideView нужно прописать в urlpatterns.
"""
router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("aside", AsideView, basename="aside")
router.register("feedback", FeedbackView, basename="feedback")
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("tags/", TagView.as_view()),
    path('tags/<str:tag_slug>/', TagDetailView.as_view()),
    # path('aside/', AsideView.as_view()),
] + router.urls
