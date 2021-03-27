from django.test import TestCase
from django.contrib.auth import get_user_model

from likes.models import Like

class LikeTestCase(TestCase):
    def setUp(self):
        self.author_id = "8e5a01f5-b9a2-436b-b29d-900a28d46068"
        self.author = {
            "id": self.author_id,
            "url": "",
            "host": "http://127.0.0.1:8000",
            "type": "author",
            "github": "",
            "username": "object",
            "displayName": ""
        }

        self.comment =  "http://127.0.0.1:8000/api/author/8e5a01f5-b9a2-436b-b29d-900a28d46068/posts/2ed70465-0e94-4049-a472-167229a11c78/comments/3ad70465-0e94-4049-a472-167229a11c78"
        self.post =  "http://127.0.0.1:8000/api/author/8e5a01f5-b9a2-436b-b29d-900a28d46068/posts/2ed70465-0e94-4049-a472-167229a11c78"

    def test_create_like_for_comment(self):
        """Test creation of Like object for comment"""
        Like()
        like = Like(
            author=self.author, 
            object=self.comment,
            object_type=Like.LIKE_COMMENT,
            object_id=self.comment.split('/')[-1],
            author_id=self.author_id)
        self.assertEqual(like.type, 'like')

    def test_create_like_for_post(self):
        """Test creation of Like object for post"""
        Like()
        like = Like(
            author=self.author, 
            object=self.post,
            object_type=Like.LIKE_POST,
            object_id=self.post.split('/')[-1],
            author_id=self.author_id)
        self.assertEqual(like.type, 'like')
