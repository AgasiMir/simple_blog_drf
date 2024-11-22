import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model


from .models import Post, Comment


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_staff = False


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    h1 = factory.Faker("word")
    title = factory.Faker("word")
    description = factory.Faker("text")
    content = factory.Faker("text")


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    username = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    text = factory.Faker("text")
