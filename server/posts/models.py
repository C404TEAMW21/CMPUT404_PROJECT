from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField

from main import models as mainModels
from main import utils
import uuid

class Post(models.Model):
    type = "post"
    title = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    source = models.URLField(blank=True, help_text="last location/url where we got this post")
    origin = models.URLField(blank=True,  help_text="original location/url")
    description = models.CharField(blank=True, max_length=250)

    # TODO: might have a user make 2 posts if a post includes an image
    CT_MARKDOWN = 'text/markdown' # CommonMark
    CT_PLAIN = 'text/plain'       # utf-8
    CT_HTML = 'text/html' # TODO: strip tags
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

    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(mainModels.Author, on_delete=models.PROTECT)

    # TODO: create categories
    categories = ArrayField(models.TextField(), blank=True, default=list, null=True) # e.g. ["web","tutorial"]
    count =  models.PositiveIntegerField(default=0)       # for comments
    size =  models.PositiveIntegerField(default=0)        # page size for comments

    # For comments, see the function get_comments_page_url() below
    # TODO: turn comment-related attributes into functions instead
    # TODO: get 5 comments per post

    # Default time is in UTC (see settings.py)
    published = models.DateTimeField(default=now)

    # Default visibility is Public
    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'
    VISIBILITY_CHOICES = [ (PUBLIC, 'Public'), (FRIENDS, 'Friends')]
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default=PUBLIC)

    # unlisted is used for images so they won't show up in timelines
    unlisted = models.BooleanField(default=False)

    # TODO; page pagination
    def get_comments_page_url(self):
        return f'{utils.HOST}/author/{str(self.author.id)}/posts/{str(self.id)}/comments'

    def get_id_url(self):
        return f'{utils.HOST}/author/{str(self.author.id)}/posts/{str(self.id)}/'
