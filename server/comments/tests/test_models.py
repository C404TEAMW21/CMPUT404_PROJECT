from django.test import TestCase
from django.contrib.auth import get_user_model

from comments.models import Comment
from posts.models import Post
from datetime import datetime

from main import models
import uuid


COMMENT_CONTENT = 'This is a comment'

class CommentTestCase(TestCase):
    def setUp(self):
        self.title = 'Title'
        self.source = 'https://example.com/source'
        self.origin ='https://example.com/origin'
        self.description = 'This is a brief description'
        self.content='The actual content'
        self.content_type='text/plain'

        self.author = get_user_model().objects.create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('33f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )

        self.post = Post.objects.create(
            title=self.title,
            source=self.source,
            origin=self.origin,
            description=self.description,
            content=self.content,
            author=self.author,
        )
    
    def isvaliduuid(self, id):
        try:
            uuid.UUID(id, version=4)
            return True
        except ValueError:
            return False

    def test_create_comment(self):
        """Test creation of Comment Object"""
        comment = Comment.objects.create(
            author=self.author,
            comment=COMMENT_CONTENT,
            post=self.post,
        )

        self.assertEqual(comment.type, 'comment')
        self.assertEqual(comment.author, self.author)
        self.assertTrue(isinstance(comment.id, uuid.UUID))
        self.assertEqual(comment.comment, COMMENT_CONTENT)
        self.assertTrue(isinstance(comment.published, datetime))
        self.assertTrue(comment.contentType, Comment.CT_MARKDOWN)
    
    def test_create_comment(self):
        """Test Comment Object can choose plain text for content"""
        comment = Comment.objects.create(
            author=self.author,
            comment=COMMENT_CONTENT,
            post=self.post,
            contentType=Comment.CT_PLAIN
        )

        self.assertTrue(comment.contentType, Comment.CT_PLAIN)
