from django.db import models
from posts.models import Post
import uuid
from main import utils

class Comment(models.Model):
    type = "comment"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.JSONField()
    comment = models.TextField(blank=True, null=True)
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    CT_MARKDOWN = 'text/markdown' # CommonMark
    CT_PLAIN = 'text/plain'       # utf-8
    CT_HTML = 'text/html'
    CT_BASE64 = 'application/base64'
    CT_PNG = 'image/png;base64'   # embedded png
    CT_JPG = 'image/jpeg;base64'  # embedded jpeg

    CONTENT_TYPE_CHOICES = [
        ('Text', (
            (CT_MARKDOWN, 'markdown'),
            (CT_PLAIN, 'plain'),
            (CT_HTML, 'html'),
        )),
        ('Encoded Text', (
            (CT_BASE64, 'base64'),
        )),
        ('Image', (
            (CT_PNG, '.png'),
            (CT_JPG, '.jpg'),
        )),
    ]

    contentType = models.CharField(
        max_length=18,
        choices=CONTENT_TYPE_CHOICES,
        default=CT_MARKDOWN
    )

    def get_id_url(self):
        return f'{utils.HOST}api/author/{str(self.post.author.id)}/posts/{str(self.post.id)}/comments/{self.id}'
