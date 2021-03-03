from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


from main import models
import uuid

def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)

class TestFollowersListEndpoint(TestCase):
    """Test API(GET)://service/author/{id}/followers"""
    def setUp(self):
        self.client = APIClient()
        
    def test_author_followers(self):
        "Test return a follower list if the author exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_invalid_author_followers(self):
        "Test return error if author does not exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/abc123/')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_endpoint_with_unauthorized_user(self):
        "Test endpoint is safeguard by user credential"
        create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_endpoint_with_admin_approval(self):
        "Test endpoint is safeguard by adminApproval"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_follower_object(self):
        "Test create follower object is does not exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['items']), 0)


class TestFollowerCheckEndpoint(TestCase):
    """Test API(GET)://service/author/{id}/followers/{foreign_id}"""
    def setUp(self):
        self.client = APIClient()
        self.authorA = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        
        
    def test_follower_check(self):
        "Test if A follow B"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )

        self.client.force_authenticate(user=self.authorA)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.data['items'][0]['status'])

    def test_follower_with_unauthorized_user(self):
        "Test if endpoint is safeguard by user credential"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_follower_admin_approval(self):
        "Test if follower check endpoint is safeguard by adminApproval"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_follower_invalid_author_uuid(self):
        "Test follower check with invlid author uuid"
       
        self.client.force_authenticate(user=self.authorA)

        res = self.client.get('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    def test_follower_invalid_foreign_author_uuid(self):
        "Test follower check invlid foreign author uuid"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
        )
        self.client.force_authenticate(user=self.authorA)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/')
       
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    def test_create_follower_object(self):
        "Test create follower object is does not exists"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['items'][0]['status'], False)
    
class TestAddFollowerEndpoint(TestCase):
    """Test API(PUT)://service/author/{id}/followers/{foreign_id}"""
    def setUp(self):
        self.client = APIClient()
        
        self.authorA = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
        )

    def test_adding_follower(self):
        "Test adding foreign author to follow author"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)
        
        res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_adding_invalid_follower(self):
        "Test adding follower with invalid foreign author uuid"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/hello/')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    def test_adding_follower_to_invalid_author(self):
        "Test adding follower with invalid foreign author uuid"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.put('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    def test_adding_follower_with_unauthorized_user(self):
        "Test adding follower endpoint is safeguard by user credential"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        res = self.client.put('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_adding_follower_user_admin_approval(self):
        "Test adding follower endpoint is safeguard by adminApproval"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.put('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_adding_follower_endpoint_check_foreign_id_with_loggedin_user(self):
        "Test to ensure user login as the foreign id before adding following other author"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        create_author(
            username='abc003',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fcc'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/' )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_follower_object(self):
        "Test create follower object is does not exists"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['items'][0]['status'], True)

class TestDeleteFollowerEndpoint(TestCase):
    """Test API(Delete)://service/author/{id}/followers/{foreign_id}"""
    def setUp(self):
        self.client = APIClient()
        
        self.authorA = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
        )

    def test_unfollowing_an_author(self):
        "Test foreign author unfollowing an author"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        authorAObj = models.Author.objects.get(id=self.authorA.id)
        authorA = models.Followers.objects.create(author=authorAObj)
        authorA.followers.add(authorB)

        self.client.force_authenticate(user=authorB)
        res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unfollowing_an_not_following_author(self):
        "Test foreign author unfollowing an author that is not in their following"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )

        self.client.force_authenticate(user=authorB)
        res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'You are not following this author, hence, you can unfollow')

    def test_unfollow_with_invalid_foreign_id(self):
        "Test unfollowing with invalid foreign id"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        authorAObj = models.Author.objects.get(id=self.authorA.id)
        authorA = models.Followers.objects.create(author=authorAObj)
        authorA.followers.add(authorB)
        self.client.force_authenticate(user=authorB)

        res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/hello/')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    def test_unfollowing_with_invalid_author_id(self):
        "Test unfollowing with invalid author id"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        authorAObj = models.Author.objects.get(id=self.authorA.id)
        authorA = models.Followers.objects.create(author=authorAObj)
        authorA.followers.add(authorB)
        self.client.force_authenticate(user=authorB)

        res = self.client.delete('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['error'][0], 'User not found')

    def test_unfollowing_with_unauthorized_user(self):
        "Test deleting follower endpoint is safeguard by user credential"
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )

        res = self.client.delete('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfollowing_user_admin_approval(self):
        "Test deleting follower endpoint is safeguard by adminApproval"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=False,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        self.client.force_authenticate(user=authorB)

        res = self.client.delete('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_adding_follower_endpoint_check_foreign_id_with_loggedin_user(self):
        "Test to ensure user login as the foreign id before deleting follower from other author"
        authorB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        create_author(
            username='abc003',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fcc'),
        )
        authorAObj = models.Author.objects.get(id=self.authorA.id)
        authorA = models.Followers.objects.create(author=authorAObj)
        authorA.followers.add(authorB)
        self.client.force_authenticate(user=authorB)
        self.client.force_authenticate(user=authorB)

        res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/' )

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

