from django.contrib import admin
from django.utils.safestring import mark_safe

from core.models import Comment, Feedback, Post


class CommentsInLine(admin.StackedInline):
    model = Comment
    readonly_fields = ["username", "post", "text", "created_date"]
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "author__username", "tag_list"]
    list_display = [
        "get_image",
        "title",
        "tag_list",
        "author",
        "get_comments_count",
        "created_at",
    ]
    list_display_links = ["get_image", "title"]
    ordering = ["-id", "title", "author"]
    date_hierarchy = "created_at"
    list_filter = ["created_at", "tag"]
    list_per_page = 10

    fields = [
        "get_fields_image",
        "h1",
        "title",
        "description",
        "content",
        "tag",
        "image",
        "author",
    ]
    save_on_top = True
    readonly_fields = ["get_fields_image"]
    raw_id_fields = ["author"]

    inlines = [CommentsInLine]

    @admin.display(description="image")
    def get_image(self, obj: Post):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=160>")
        return "No image"

    @admin.display(description="image")
    def get_fields_image(self, obj: Post):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width=80%>")
        return "No image"

    @admin.display(description="comments")
    def get_comments_count(self, obj: Post):
        return obj.comments.count()

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("tag", "comments")
            .select_related("author")
        )

    def tag_list(self, obj: Post):
        return ", ".join(o.name for o in obj.tag.all())


@admin.register(Feedback)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "email", "created_at"]
    list_display_links = ["name", "subject"]
    date_hierarchy = "created_at"
    list_filter = ["subject", "created_at"]
    list_per_page = 20

    readonly_fields = ["name", "email", "subject", "body", "created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["username", "get_text", "created_date"]
    list_display_links = ["username", "get_text"]
    date_hierarchy = "created_date"
    list_filter = ["created_date"]
    list_per_page = 20

    readonly_fields = ["post", "username", "text", "created_date"]

    @admin.display(description="text")
    def get_text(self, obj: Comment):
        return obj.text[:75] if len(obj.text) <= 125 else obj.text[:72] + "..."


admin.site.site_title = "myblog_drf"
admin.site.site_header = "myblog_drf"
admin.site.index_title = "Администрирование myblog_drf"
