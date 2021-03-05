from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from inbox.models import Inbox
from posts.models import Post
from main import utils

from rest_framework.test import APIClient
from rest_framework import status

def create_post(**params):
    """Helper function to create Post"""
    return Post.objects.create(**params)

def create_payload(item_type, item_id):
    """Helper function to create Post"""
    payload = {
        "type": item_type,
        "id": item_id,
    }
    return payload

# TODO: add test cases for Like and Follow
class TestInboxEndpoint(TestCase):
    """Test Inbox API ://service/author/{AUTHOR_ID}/inbox/

    GET - get the Inbox
    POST - send Follow, Like, Post to the Inbox
    DELETE - clear the Inbox

    """

    def setUp(self):
        self.author_1 = get_user_model().objects.create_author(
            username='testing1',
            password='testing1',
            adminApproval=True
        )
        self.author_2 = get_user_model().objects.create_author(
            username='testing2',
            password='testing2',
            adminApproval=True
        )
        self.inbox_1 = Inbox.objects.get(author=self.author_1)
        self.inbox_2 = Inbox.objects.get(author=self.author_2)
        # Inbox URL of author_1
        self.inbox_url = reverse(
            'inbox:inbox', kwargs={'author_id': self.author_1.id}
        )
        self.client = APIClient()

    def test_send_public_post(self):
        """Test sending public Post returns Response with Post id"""
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "PUBLIC",
        }

        self.client.force_authenticate(user=self.author_1)
        post = create_post(**post_params)
        payload = create_payload("post", post.id)

        self.inbox_1 = Inbox.objects.get(author=self.author_1)
        self.assertEqual(len(self.inbox_1.items), 0)
        res = self.client.post(self.inbox_url, payload)
        self.inbox_1 = Inbox.objects.get(author=self.author_1)
        self.assertEqual(len(self.inbox_1.items), 1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(f'{post.id}', res.data['data'])
        self.assertIn(f'{self.author_1.id}', res.data['data'])

    def test_send_post_with_invalid_post_id(self):
        """Test sending public Post with invalid Post id"""
        self.client.force_authenticate(user=self.author_1)
        payload = create_payload("post", "0000")

        res = self.client.post(self.inbox_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_invalid_payload(self):
        """Test sending item with invalid type to Inbox"""
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "FRIENDS",
        }
        self.client.force_authenticate(user=self.author_1)
        post = create_post(**post_params)
        payload = create_payload("invalid_type", post.id)

        res = self.client.post(self.inbox_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'],
                         "Invalid type, only \'post\', \'follow\', \'like\'")

    def test_get_self_inbox(self):
        """Test Author getting Author's own inbox"""
        self.client.force_authenticate(user=self.author_1)
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(('type', 'inbox'), res.data.items())
        self.assertEqual(f'{utils.HOST}/author/{self.author_1.id}', res.data['author'])
        self.assertIn('items', res.data)

    def test_get_others_inbox(self):
        """Test Author getting another Author's inbox"""
        self.client.force_authenticate(user=self.author_2)
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_not_approved_inbox(self):
        """Test Author getting Author's own inbox when account not approved"""
        self.client.force_authenticate(user=self.author_1)
        self.author_1.adminApproval = False
        self.author_1.save()
        res = self.client.get(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.author_1.adminApproval = True
        self.author_1.save()

    def test_delete_self_inbox(self):
        """Test Author delete Author's own inbox"""
        self.client.force_authenticate(user=self.author_1)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "PUBLIC",
        }
        post_1 = create_post(**post_params)
        post_2 = create_post(**post_params)
        post_3 = create_post(**post_params)

        payload = create_payload("post", post_1.id)
        res = self.client.post(self.inbox_url, payload)
        payload = create_payload("post", post_2.id)
        res = self.client.post(self.inbox_url, payload)
        payload = create_payload("post", post_3.id)
        res = self.client.post(self.inbox_url, payload)

        inbox_1 = Inbox.objects.get(author=self.author_1)
        self.assertEqual(len(inbox_1.items), 3)
        res = self.client.delete(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        inbox_1 = Inbox.objects.get(author=self.author_1)
        self.assertEqual(len(inbox_1.items), 0)

    def test_delete_others_inbox(self):
        """Test Author delete other Author's inbox"""
        self.client.force_authenticate(user=self.author_2)
        post_params = {
            "title": "Title",
            "author": self.author_1,
            "visibility": "PUBLIC",
        }
        post_1 = create_post(**post_params)
        post_2 = create_post(**post_params)
        post_3 = create_post(**post_params)

        payload = create_payload("post", post_1.id)
        res = self.client.post(self.inbox_url, payload)
        payload = create_payload("post", post_2.id)
        res = self.client.post(self.inbox_url, payload)
        payload = create_payload("post", post_3.id)
        res = self.client.post(self.inbox_url, payload)

        res = self.client.delete(self.inbox_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
