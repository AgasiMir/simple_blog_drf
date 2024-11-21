from django.contrib.auth import get_user_model
from django.db import models

from taggit.managers import TaggableManager

from core.services.utils import unique_slugify


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("username", "post")


class Post(models.Model):
    h1 = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.TextField()
    content = models.TextField()
    tag = TaggableManager()
    image = models.ImageField(upload_to="myblog_drf/%Y/%m/%d", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    # Такой подход полностью удовлетворяет админку,
    # но добавляет еще один в index.html и post_detail.html.
    #  Поэтому, в моделях использовал мэнеджер только к комментариям,
    #  а в админке уже чере qet_queryset, оптимизировал посты
    # objects = PostManager()

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    OPTIONS = (
        ("WISH", "Пожелания"),
        ("TECH", "Техническая неисправность"),
        ("OTHER", "Прочее"),
    )
    body = models.TextField()
    subject = models.CharField(max_length=5, choices=OPTIONS, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.name}: {self.subject}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    username = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user_name"
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.username}: {self.post}"
