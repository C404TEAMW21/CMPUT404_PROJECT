from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from likes.models import Like


class TestLikeEndpoint(TestCase):
    """ Test Get API : api/author/{author_id}/post/{post_id}/likes
            GET - get the likes for a post

        Test Get API : api/author/{author_id}/post/{post_id}/comments/{comment_id}/likes
            GET - get the likes for a comment

        Test Get API : api/author/{author_id}/liked
            GET - get the liked for an autor
    """

    def setUp(self):
        self.author_1 = get_user_model().objects.create_author(
            username='testing1',
            password='testing1',
            adminApproval=True
        )

        self.post_author = '1e5a01f5-b9a2-436b-b29d-900a28d46068'
        self.post_id = '2ed70465-0e94-4049-a472-167229a11c78'
        self.comment_id = '3ad70465-0e94-4049-a472-167229a11c78'
        self.post =  f"http://127.0.0.1:8000/api/author/{self.post_author}/posts/{self.post_id}"
        self.comment =  f"http://127.0.0.1:8000/api/author/{self.post_author}/posts/{self.post_id}/comments/{self.comment_id}"
       
        self.client = APIClient()
    
    def create_different_authors(self, author_id):
        author = {
            'id': author_id,
            'url': 'http://this.is.a.host/author/author_id',
            'host': 'http://this.is.a.host',
            'type': 'author',
            'github': '',
            'username': 'object',
            'displayName': ''
        }
        return author


    def test_get_post_likes(self):
        """Test get post likes endpoint"""

        author_id1 = '8e5a01f5-b9a2-436b-b29d-900a28d46068'
        like = Like.objects.create(
            author=self.create_different_authors(author_id1), 
            object=self.post,
            object_type=Like.LIKE_POST,
            object_id=self.post.split('/')[-1],
            author_id=author_id1)

        author_id2 = '9e5a01f5-b9a2-436b-b29d-900a28d46068'
        like = Like.objects.create(
            author=self.create_different_authors(author_id2), 
            object=self.post,
            object_type=Like.LIKE_POST,
            object_id=self.post.split('/')[-1],
            author_id=author_id2)
        
        url = reverse('likes:post_likes', kwargs={'author_id': self.post_author, 'post_id': self.post_id})
        self.client.force_authenticate(user=self.author_1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data.get('items')), 2)
        self.assertEqual(res.data.get('type'), 'likes')
        self.assertEqual(res.data['items'][0]['author'], self.create_different_authors(author_id1))
        self.assertEqual(res.data['items'][0]['object'], self.post)

    def test_get_comment_likes(self):
        """Test get comment likes endpoint"""

        author_id1 = '8e5a01f5-b9a2-436b-b29d-900a28d46068'
        like = Like.objects.create(
            author=self.create_different_authors(author_id1), 
            object=self.comment,
            object_type=Like.LIKE_COMMENT,
            object_id=self.comment.split('/')[-1],
            author_id=author_id1)
        
        author_id2 = '9e5a01f5-b9a2-436b-b29d-900a28d46068'
        like = Like.objects.create(
            author=self.create_different_authors(author_id2), 
            object=self.comment,
            object_type=Like.LIKE_COMMENT,
            object_id=self.comment.split('/')[-1],
            author_id=author_id2)
        
        url = reverse(
            'likes:comment_likes',
            kwargs={
                'author_id': self.post_author,
                'post_id': self.post_id,
                'comment_id': self.comment_id
            }
        )
        self.client.force_authenticate(user=self.author_1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data.get('items')), 2)
        self.assertEqual(res.data.get('type'), 'likes')
        self.assertEqual(res.data['items'][0]['author'], self.create_different_authors(author_id1))
        self.assertEqual(res.data['items'][0]['object'], self.comment)
    
    def test_get_author_liked(self):
        """Test can get all things an author liked"""

        # author1 liked comment
        author_id1 = '8e5a01f5-b9a2-436b-b29d-900a28d46068'
        like = Like.objects.create(
            author=self.create_different_authors(author_id1), 
            object=self.comment,
            object_type=Like.LIKE_COMMENT,
            object_id=self.comment.split('/')[-1],
            author_id=author_id1)
        
        # author1 liked post
        like = Like.objects.create(
            author=self.create_different_authors(author_id1), 
            object=self.post,
            object_type=Like.LIKE_POST,
            object_id=self.post.split('/')[-1],
            author_id=author_id1)
        
        # author2 liked comment
        author_id2 = '9e5a01f5-b9a2-436b-b29d-900a28d46068'
        like = Like.objects.create(
            author=self.create_different_authors(author_id2), 
            object=self.comment,
            object_type=Like.LIKE_COMMENT,
            object_id=self.comment.split('/')[-1],
            author_id=author_id2)

        # only returns author1 liked objects

        url = reverse(
            'likes:liked',
            kwargs={'author_id': author_id1}
        )
        self.client.force_authenticate(user=self.author_1)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('type'), 'liked')
        self.assertEqual(len(res.data.get('items')), 2)

        first_item = res.data.get('items')[0]
        self.assertEqual(first_item['type'], 'like')
        self.assertEqual(first_item['author'], self.create_different_authors(author_id1))
        self.assertEqual(first_item['object'], self.comment)
