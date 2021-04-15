from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Author
from posts.models import Post
from posts.serializers import PostSerializer

class Inbox(models.Model):
    type = "inbox"
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = ArrayField(models.JSONField(), blank=True, default=list, null=True)

    def send_to_inbox(self, data):
        self.items.append(data)
        self.save()


# create Inbox object after Author is created and called save()
@receiver(post_save, sender=Author)
def my_handler(sender, instance, **kwargs):
    if not Inbox.objects.filter(author=instance).exists():
        Inbox.objects.create(author=instance)