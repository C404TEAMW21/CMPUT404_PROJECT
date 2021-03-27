from django.db import models


class Like(models.Model):
    type = "like"
    
    author = models.JSONField()
    object = models.TextField()
    object_id = models.TextField()
    author_id = models.CharField(max_length=40)

    # For easier time querying
    LIKE_COMMENT = 'comment'
    LIKE_POST = 'post'

    LIKE_CHOICES = [
        (LIKE_COMMENT, LIKE_COMMENT),
        (LIKE_POST, LIKE_POST)
    ]

    object_type = models.CharField(
        max_length=8,
        choices=LIKE_CHOICES
    )

    class Meta:
        unique_together = ('author_id', 'object')
