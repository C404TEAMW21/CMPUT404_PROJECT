from django.db import models
from posts.models import Post
import uuid
from main import models as mainModels

class Comment(models.Model):
    type = "comment"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(mainModels.Author, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    CT_MARKDOWN = 'text/markdown'
    CT_PLAIN = 'text/plain'

    CONTENT_TYPE_CHOICES = [
        ('Text', (
            (CT_MARKDOWN, 'markdown'),
            (CT_PLAIN, 'plain'),
        ))
    ]

    contentType = models.CharField(
        max_length=18,
        choices=CONTENT_TYPE_CHOICES,
        default=CT_MARKDOWN
    )
