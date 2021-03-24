from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from main.models import Followers

from main import models
import uuid

def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)

def author_b_follow_author_a_url(aId, bId):
    """Helper function to create author B to follow author A URL"""
    return reverse(
            'followers:followers modify',
            kwargs={'id': aId, 'foreignId': bId}
    )
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

    def test_author_followers(self):
        "Test return a follower list that include remote followers if the author exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        remote_author_payload = {
            "type":"author",
            "id":"11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"http://team6/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }
        self.client.force_authenticate(user=user)
        models.Followers.objects.create(author=user)
        author = models.Followers.objects.get(author=user)
        # Create Remote user 
        author.remoteFollowers['teamabc'] = {}
        author.remoteFollowers['teamabc']['actorId'] = remote_author_payload
        author.save()

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['items']), 1)

    def test_author_followers(self):
        "Test return a follower list that include remote and local followers if the author exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        userB = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3a').int,
        )
        remote_author_payload = {
            "type":"author",
            "id":"11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"http://team6/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }
       
        self.client.force_authenticate(user=user)
        models.Followers.objects.create(author=user)
        author = models.Followers.objects.get(author=user)
        # Create Remote user 
        author.remoteFollowers['teamabc'] = {}
        author.remoteFollowers['teamabc']['actorId'] = remote_author_payload
        author.save()
        # Local user
        author.followers.add(userB)
        author.save()

        res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/')
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['items']), 2)
    
    
    
    def test_invalid_author_followers(self):
        "Test return error if author does not exists"
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/service/author/abc123/followers/')

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


# class TestFollowerCheckEndpoint(TestCase):
#     """Test API(GET)://service/author/{id}/followers/{foreign_id}"""
#     def setUp(self):
#         self.client = APIClient()
#         self.authorA = create_author(
#             username='abc001',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
#         )
        
        
#     def test_follower_check(self):
#         "Test if A follow B"
#         create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
#         )

#         self.client.force_authenticate(user=self.authorA)

#         res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertFalse(res.data['items'][0]['status'])

#     def test_follower_with_unauthorized_user(self):
#         "Test if endpoint is safeguard by user credential"
#         create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
#         )

#         res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
#     def test_follower_admin_approval(self):
#         "Test if follower check endpoint is safeguard by adminApproval"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=False,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
#         )
#         self.client.force_authenticate(user=authorB)

#         res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_follower_invalid_author_uuid(self):
#         "Test follower check with invlid author uuid"
       
#         self.client.force_authenticate(user=self.authorA)

#         res = self.client.get('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')
       
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'User not found')

#     def test_follower_invalid_foreign_author_uuid(self):
#         "Test follower check invlid author B uuid"
#         create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=False,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb').int,
#         )
#         self.client.force_authenticate(user=self.authorA)

#         res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/')
       
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'User not found')

#     def test_create_follower_object(self):
#         "Test create follower object is does not exists"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         self.client.force_authenticate(user=authorB)

#         res = self.client.get('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/')

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['items'][0]['status'], False)
    
# class TestAddFollowerEndpoint(TestCase):
#     """Test API(PUT)://service/author/{id}/followers/{foreign_id}"""
#     def setUp(self):
#         self.client = APIClient()
        
#         self.authorA = create_author(
#             username='abc001',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
#         )

#         self.team6Credential = create_author(
#             username='team6',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3f'),
#         )

#     def test_adding_follower(self):
#         "Test adding author B to follow author A"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }
#         self.client.force_authenticate(user=authorB)
        
#         res = self.client.put(author_b_follow_author_a_url(self.authorA.id, authorB.id), payload, format='json')
        
#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_adding_invalid_follower(self):
#         "Test adding follower with invalid author B uuid"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         self.client.force_authenticate(user=authorB)
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }

#         res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/hello/', payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'User not found')

#     def test_adding_follower_to_invalid_author(self):
#         "Test adding follower with invalid author B uuid"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }
#         self.client.force_authenticate(user=authorB)

#         res = self.client.put('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/', payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'User not found')

#     def test_adding_follower_with_unauthorized_user(self):
#         "Test adding follower endpoint is safeguard by user credential"
#         create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }
        
#         res = self.client.put('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/', payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_adding_follower_user_admin_approval(self):
#         "Test adding follower endpoint is safeguard by adminApproval"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=False,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }
#         self.client.force_authenticate(user=authorB)

#         res = self.client.put('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/', payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_adding_follower_endpoint_check_foreign_id_with_loggedin_user(self):
#         "Test to ensure user login as the foreign id before adding following other author"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         create_author(
#             username='abc003',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fcc'),
#         )
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }
#         self.client.force_authenticate(user=authorB)

#         res = self.client.put('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/', payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_follower_object(self):
#         "Test create follower object if it does not exists locally"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         self.client.force_authenticate(user=authorB)
#         payload = {
#             'actor': {
#                 'host': 'https://konnection-client.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com'
#             }
#         }

#         res = self.client.put(author_b_follow_author_a_url(self.authorA.id, authorB.id), payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data['items'][0]['status'], True)

#     def test_cross_sever_adding_follower(self):
#         "Test adding foreign author B to follow local author A"
#         payload = {
#             'actor': {
#                 'host': 'https://team6.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com'
#             }
#         }
#         self.client.force_authenticate(user=self.team6Credential)

#         res = self.client.put(author_b_follow_author_a_url(self.authorA.id, self.team6Credential.id), payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_cross_server_adding_follower_without_actor_id(self):
#         "Test adding foreign author B to follow local author A without actor id"
#         payload = {
#             'actor': {
#                 'host': 'https://team6.herokuapp.com',
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com'
#             }
#         }
#         self.client.force_authenticate(user=self.team6Credential)

#         res = self.client.put(author_b_follow_author_a_url(self.authorA.id, self.team6Credential.id), payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_cross_server_adding_follower_without_actor_host(self):
#         "Test adding foreign author B to follow local author A without actor host"
#         payload = {
#             'actor': {
#             },
#             'object': {
#                 'host': 'https://konnection-client.herokuapp.com',
#             }
#         }
#         self.client.force_authenticate(user=self.team6Credential)

#         res = self.client.put(author_b_follow_author_a_url(self.authorA.id, self.team6Credential.id), payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

#     def test_cross_server_adding_follower_without_object_host(self):
#         "Test adding foreign author B to follow local author A without object host"
#         payload = {
#             'actor': {
#                 'host': 'https://team6.herokuapp.com',
#                 'id': 'aaaaa',
#             },
#             'object': {
#             }
#         }
#         self.client.force_authenticate(user=self.team6Credential)

#         res = self.client.put(author_b_follow_author_a_url(self.authorA.id, self.team6Credential.id), payload, format='json')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# class TestDeleteFollowerEndpoint(TestCase):
#     """Test API(Delete)://service/author/{id}/followers/{foreign_id}"""
#     def setUp(self):
#         self.client = APIClient()
        
#         self.authorA = create_author(
#             username='abc001',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
#         )

#     def test_unfollowing_an_author(self):
#         "Test author B unfollowing an author"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         authorAObj = models.Author.objects.get(id=self.authorA.id)
#         authorA = models.Followers.objects.create(author=authorAObj)
#         authorA.followers.add(authorB)

#         self.client.force_authenticate(user=authorB)
#         res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

#         self.assertEqual(res.status_code, status.HTTP_200_OK)

#     def test_unfollowing_an_not_following_author(self):
#         "Test author B unfollowing an author that is not in their following"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )

#         self.client.force_authenticate(user=authorB)
#         res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'You are not following this author, hence, you can unfollow')

#     def test_unfollow_with_invalid_foreign_id(self):
#         "Test unfollowing with invalid foreign id"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         authorAObj = models.Author.objects.get(id=self.authorA.id)
#         authorA = models.Followers.objects.create(author=authorAObj)
#         authorA.followers.add(authorB)
#         self.client.force_authenticate(user=authorB)

#         res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/hello/')

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'User not found')

#     def test_unfollowing_with_invalid_author_id(self):
#         "Test unfollowing with invalid author id"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         authorAObj = models.Author.objects.get(id=self.authorA.id)
#         authorA = models.Followers.objects.create(author=authorAObj)
#         authorA.followers.add(authorB)
#         self.client.force_authenticate(user=authorB)

#         res = self.client.delete('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(res.data['error'][0], 'User not found')

#     def test_unfollowing_with_unauthorized_user(self):
#         "Test deleting follower endpoint is safeguard by user credential"
#         create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )

#         res = self.client.delete('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_unfollowing_user_admin_approval(self):
#         "Test deleting follower endpoint is safeguard by adminApproval"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=False,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         self.client.force_authenticate(user=authorB)

#         res = self.client.delete('/service/author/hello/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fbb/' )

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_adding_follower_endpoint_check_foreign_id_with_loggedin_user(self):
#         "Test to ensure user login as the foreign id before deleting follower from other author"
#         authorB = create_author(
#             username='abc002',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
#         )
#         create_author(
#             username='abc003',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fcc'),
#         )
#         authorAObj = models.Author.objects.get(id=self.authorA.id)
#         authorA = models.Followers.objects.create(author=authorAObj)
#         authorA.followers.add(authorB)
#         self.client.force_authenticate(user=authorB)
#         self.client.force_authenticate(user=authorB)

#         res = self.client.delete('/service/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/followers/88f1df52-4b43-11e9-910f-b8ca3a9b9fcc/' )

#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

# class TestFriendsListEndpoint(TestCase):
#     """Test API(GET):://service/author/{id}/friends/"""

#     def setUp(self):
#         self.client = APIClient()
#         self.client2 = APIClient()
#         self.id = '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'
#         self.id2 = '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'
        
#     def test_author_followers(self):
#         "Test returns an empty list if no friends"
#         user = create_author(
#             username='abc001',
#             password='abcpwd',
#             adminApproval=True,
#             id=uuid.UUID(self.id),
#         )
#         self.client.force_authenticate(user=user)

#         res = self.client.get(f'/service/author/{self.id}/friends/')

#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, {})

    # def test_friends(self):
    #     """Test returns a list of friends"""

    #     authorA = create_author(
    #         username='user1',
    #         password='abcpwd',
    #         adminApproval=True,
    #         id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
    #     )

    #     authorB = create_author(
    #         username='user2',
    #         password='abcpwd',
    #         adminApproval=True,
    #         id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
    #     )
        
    #     self.client.force_authenticate(user=authorB)
    #     res = self.client.put(f'/service/author/{self.id}/followers/{self.id2}/')
        
    #     self.client2.force_authenticate(user=authorA)
    #     res = self.client2.put(f'/service/author/{self.id2}/followers/{self.id}/')

    #     res = self.client.get(f'/service/author/{self.id}/friends/')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data['friends']), 1)
    #     self.assertEqual(res.data['friends'][0]['username'], 'user2')

    #     res = self.client2.get(f'/service/author/{self.id2}/friends/')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data['friends']), 1)
    #     self.assertEqual(res.data['friends'][0]['username'], 'user1')
