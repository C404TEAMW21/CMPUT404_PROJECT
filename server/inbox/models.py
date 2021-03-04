from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Author
from posts.models import Post
from posts.serializers import PostSerializer

class Inbox(models.Model):
    # TODO add like and follow
    type = "inbox"
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    items = ArrayField(models.JSONField(), blank=True, default=list, null=True)

    def send_to_inbox(self, inbox_id, post_id):
        try:
            a_post = Post.objects.get(pk=post_id, unlisted=False)
            inbox = Inbox.objects.get(author=inbox_id)
        except Post.DoesNotExist:
            return
        except Inbox.DoesNotExist:
            return
        data = PostSerializer(a_post).data
        data['categories'] = list(data['categories'])
        inbox.items.append(data)
        inbox.save()


# create Inbox object after Author is created and called save()
@receiver(post_save, sender=Author)
def my_handler(sender, instance, **kwargs):
    if not Inbox.objects.filter(author=instance).exists():
        Inbox.objects.create(author=instance)