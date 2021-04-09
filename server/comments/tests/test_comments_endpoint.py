from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Post
from comments.models import Comment
from rest_framework.test import APIClient
from rest_framework import status
from main import models
from author.serializers import AuthorProfileSerializer
import json


CONTENT = 'This is a short comment'

class TestCreateCommentEndpoint(TestCase):
    """Tests the endpoint api/author/{AUTHOR_ID}/posts/{POST_ID}/comments

    GET - returns a list of comments
    POST - creates a comment
    """

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
        )

        self.author2 = get_user_model().objects.create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
        )

        self.author3 = get_user_model().objects.create_author(
            username='abc003',
            password='abcpwd',
            adminApproval=True,
        )

        self.post = Post.objects.create(
            title=self.title,
            source=self.source,
            origin=self.origin,
            description=self.description,
            content=self.content,
            author=self.author,
        )

        self.comment_url = reverse(
            'comments:comments',
            kwargs={'author_id': self.post.author.id, 'post_id': self.post.id}
        )
        self.client = APIClient()

    def author_json(self, id):
        author = {
            "id": str(id),
            "url": f"https://url.com/author/{id}",
            "host": "https://url.com/",
            "type": "author",
            "github": "www.google.ca",
            "displayName": "a display name"
        }
        return author

    def payload(self, author):
        payload = {
            'comment': CONTENT,
            'contentType': Comment.CT_MARKDOWN,
            'author': AuthorProfileSerializer(author).data,
        }
        return payload
    
    def receive_comments_payload(self, author):
        payload = {
            'author': AuthorProfileSerializer(author).data,
        }
        return payload

    def test_get_comments_endpoint(self):
        """Test get an empty list of comments"""
        self.client.force_authenticate(user=self.author)
        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])
    
    def test_get_comments_endpoint_as_remote_user(self):
        """Test get a list of comments as remote_user"""
        # make friend post
        Post.objects.filter(visibility=Post.PUBLIC).update(visibility=Post.FRIENDS)
        self.post.visibility = Post.FRIENDS

        # author and author2 are friends
        follower = models.Followers.objects.get(author=self.author)
        follower.remoteFollowers[str(self.author2.id)] = self.author_json(self.author2.id)
        follower.save()

        following = models.Following.objects.get(author=self.author)
        following.remote_following[str(self.author2.id)] = self.author_json(self.author2.id)
        following.save()

        Comment.objects.create(
            author=self.author_json(self.author.id),
            comment='comment by original post author',
            post=self.post
        )
        Comment.objects.create(
            author=self.author_json('h57796cb5a0441fca3f1093620d327b2'),
            comment='comment by a friend',
            post=self.post
        )

        # post author can see both comments
        self.client.force_authenticate(user=self.author)
        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # remote node user passes user id
        remote_server = get_user_model().objects.create_author(
            username='remote',
            password='abc123',
            adminApproval=True,
            type='node'
        )
        remote_server.url = 'https://url.com/' # set explicitly to override default
        remote_server.save()

        # remote author can see both comments
        self.client.force_authenticate(user=remote_server)
        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_comments_endpoint_as_local_user(self):
        """Test get a list of comments as local_user"""
        # make friend post
        Post.objects.filter(visibility=Post.PUBLIC).update(visibility=Post.FRIENDS)
        self.post.visibility = Post.FRIENDS

        # author and author2 are friends
        models.Followers.objects.get(author=self.author).followers.add(self.author2)
        models.Followers.objects.get(author=self.author2).followers.add(self.author)
        models.Following.objects.get(author=self.author).following.add(self.author2)
        models.Following.objects.get(author=self.author2).following.add(self.author)

        # author and author3 are friends
        models.Followers.objects.get(author=self.author).followers.add(self.author3)
        models.Followers.objects.get(author=self.author3).followers.add(self.author)
        models.Following.objects.get(author=self.author3).following.add(self.author)
        models.Following.objects.get(author=self.author).following.add(self.author3)

        Comment.objects.create(
            author=self.author_json(self.author.id),
            comment='comment by original post author',
            post=self.post
        )
        Comment.objects.create(
            author=self.author_json(self.author2.id),
            comment='comment by a friend',
            post=self.post
        )

        # post author can see both comments
        self.client.force_authenticate(user=self.author)
        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # logged-in friend (of post author) can see both comments
        self.client.force_authenticate(user=self.author2)
        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # another author can only see post author's comments
        self.client.force_authenticate(user=self.author3)
        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_comment_endpoint(self):
        """Test create a comment"""
        self.client.force_authenticate(user=self.author)

        res = self.client.post(self.comment_url, self.payload(self.author), format='json')
        comment = res.data
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment['type'], 'comment')
        self.assertEqual(comment['author']['id'], str(self.author.id))
        self.assertEqual(comment['comment'], CONTENT)
        self.assertEqual(comment['contentType'], Comment.CT_MARKDOWN)

        res = self.client.get(self.comment_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment_obj = Comment.objects.get(id=comment['id'].split('/')[-1])
        self.assertEqual(comment_obj.post, self.post)
 
    def test_create_comment_endpoint_for_friends(self):
        """Test create and getting comments as a friend or the post author"""
        # This is a FRIENDS post
        post = Post.objects.filter(visibility=Post.PUBLIC).update(visibility=Post.FRIENDS)

        # author is friend with author2
        models.Followers.objects.get(author=self.author).followers.add(self.author2)
        models.Followers.objects.get(author=self.author2).followers.add(self.author)
        models.Following.objects.get(author=self.author).following.add(self.author2)
        models.Following.objects.get(author=self.author2).following.add(self.author)

        # author is friend with author3
        models.Followers.objects.get(author=self.author).followers.add(self.author3)
        models.Followers.objects.get(author=self.author3).followers.add(self.author)
        models.Following.objects.get(author=self.author).following.add(self.author3)
        models.Following.objects.get(author=self.author3).following.add(self.author)

        # friend makes a comment
        self.client.force_authenticate(user=self.author2)
        res = self.client.post(self.comment_url, self.payload(self.author2), format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # original post author makes a comment
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.author)
        res = self.client2.post(self.comment_url, self.payload(self.author), format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # second friend makes a comment
        self.client3 = APIClient()
        self.client3.force_authenticate(user=self.author3)
        res = self.client3.post(self.comment_url, self.payload(self.author3), format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # original author can see all three comments
        res = self.client2.generic(method='GET', path=self.comment_url, data=self.receive_comments_payload(self.author), content_type='application/json')
        res = self.client2.get(self.comment_url, self.receive_comments_payload(self.author), format='json')
        self.assertEqual(len(res.data), 3)

        # friend can see two comments
        res = self.client.get(self.comment_url, self.receive_comments_payload(self.author2), format='json')
        self.assertEqual(len(res.data), 2)

        # second friend can see two comments
        res = self.client3.get(self.comment_url)
        self.assertEqual(len(res.data), 2)
