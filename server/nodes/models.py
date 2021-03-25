from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
from urllib.parse import urlparse
import re

# Server that we share information with
class Node(models.Model):
    type = "node"

    remote_server_url = models.URLField(max_length=200, primary_key=True, unique=True)
    remote_server_username = models.CharField(max_length=200, default='', blank=True)
    remote_server_password = models.CharField(max_length=200, default='', blank=True, validators=[MinLengthValidator(3)])
    adminApproval = models.BooleanField(default=False)

    konnection_username = models.CharField(max_length=200, default='', blank=True)
    konnection_password = models.CharField(max_length=200, default='', blank=True)

    # create author of type 'node' if node is admin approved and remote_server_* are provided
    def save(self, *args, **kwargs):
        # set username to hostname if blank
        if not self.remote_server_username:
            self.remote_server_username = self.hostname()
        self.remote_server_username = re.sub(r'\W+', '', self.remote_server_username)
        super(Node, self).save(*args, **kwargs)

        user_model = get_user_model()
        if self.adminApproval and self.remote_server_url and self.remote_server_username and self.remote_server_password:
            try:
                server_user = user_model.objects.get(username=self.remote_server_username)
                # update server_user
                server_user.username = self.remote_server_username
                server_user.set_password(self.remote_server_password)
                server_user.url = self.remote_server_url
                server_user.adminApproval = self.adminApproval
                server_user.save()
            except user_model.DoesNotExist:
                # create server_user
                user_model.objects.create_author(
                    self.remote_server_username,
                    self.remote_server_password,
                    url=self.remote_server_url,
                    adminApproval=self.adminApproval,
                    type=self.type
                )
        else:
            # change adminApproval in server_user to False if it exists already
            try:
                server_user = user_model.objects.get(username=self.remote_server_username)
                if server_user:
                    server_user.adminApproval = False
                    server_user.save()
            except user_model.DoesNotExist:
                pass
    
    # delete corresponding author if exists
    def delete(self):
        try:
            server_user = get_user_model().objects.get(username=self.remote_server_username)
            if server_user:
                server_user.delete()
        except get_user_model().DoesNotExist:
            pass
        super(Node, self).delete()

    def hostname(self):
        parsed_url = urlparse(self.remote_server_url)
        return parsed_url.hostname
