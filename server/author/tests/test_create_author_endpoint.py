from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
import uuid

from main import utils

CREATE_USER_URL = reverse('author:create')
AUTH_USER_URL = reverse('author:auth')
ME_URL = reverse('author:me')
ALL_AUTHOR_URL = reverse('author:all_local')

def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)
     
class TestCreateAuthorEndpoint(TestCase):
    """Test API(POST)://api/author/create/"""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_endpoint(self):
        """Test signing up an author with valid payload return successful"""
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_user_endpoint_return_obj(self):
        """Test signing up an author return the correct object"""
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        
        self.assertNotIn('type', res.data)
        self.assertNotIn('id', res.data)
        self.assertNotIn('host', res.data)
        self.assertNotIn('displayName', res.data)
        self.assertNotIn('url', res.data)
        self.assertNotIn('github', res.data)

    def test_create_user_with_existed_username(self):
        """Test signing up an author with same username to return error"""
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        create_author(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_username_too_short(self):
        """Test signing up error with username less than 3 char long"""
        payload={
            'username':'ab',
            'password':'abcaa',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_with_password_too_short(self):
        """Test signing up error with password less than 5 char long"""
        payload={
            'username':'abc',
            'password':'abca',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class TestAuthAuthorEndpoint(TestCase):
    """Test API(POST)://api/author/auth/"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_author_endpoint_to_return_token(self):
        """Test token as return object after logging in"""
        payload={
            'username':'abc001',
            'password':'abcpwd',
            'adminApproval': True,
        }
        create_author(**payload)

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_auth_author_endpoint_with_invalid_credentials(self):
        """Test logging in with invalid credentials"""
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        create_author(**{
            'username':'abc001',
            'password':'abcwrong',
        })

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_auth_author_endpoint_with_missing_field(self):
        """Test logging in with incompleted data"""
        payload={
            'username':'abc001',
            'password':'',
        }

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
    
    def test_user_without_admin_approval(self):
        """Test returning error when logging into an
        account that is without admin approval"""
        payload={
            'username':'abc001',
            'password':'abcpwd',
        }
        create_author(**payload)

        res = self.client.post(AUTH_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', res.data)


class TestAuthGetAuthorEndpoint(TestCase):
    """Test API(GET)://api/author/{AUTHOR_ID}/"""
    def setUp(self):
        self.client = APIClient()
        
    def test_get_author_endpoint_with_auth(self):
        """Test retrieving author profile if user is logged in"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get('/api/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_get_author_endpoint_without_auth(self):
        """Test unsuccessful getting author profile if user is not logged in"""
        res = self.client.get('/api/author/77f1df52-4b43-11e9-910f-b8ca3a9b9f3e/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_author(self):
        """Test retrieving invalid author profile"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        self.client.force_authenticate(user)

        res = self.client.get('/api/author/hello-what-is-this/')
       
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
          
class TestUpdateAuthorProfileEndpoint(TestCase):
    """Test API(PUT)://api/author/{AUTHOR_ID}/"""
    def setUp(self):
        self.client = APIClient()
        self.author = create_author(
            username='abc001',
            password='abcpwd',
        )
        self.authorID = self.author.id

    def test_update_author_profile_endpoint(self):
        """Test updating author profile if user is logged in"""
        payload = {
            'displayName':'abc100',
            'github':'https://github.com/IanSeng'
        }
        self.client.force_authenticate(user=self.author)

        res = self.client.put(f'/api/author/{self.authorID}/', payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['displayName'], 'abc100')
        self.assertEqual(res.data['github'], 'https://github.com/IanSeng')

    def test_update_others_profile(self):
        """Test return invalid if user trys to update someone elses profile"""
        otherAuthor = create_author(
            username='abc002',
            password='abcpwd',
        )
        payload = {
            'displayName':'abc100',
            'github':'https://github.com/IanSeng'
        }
        self.client.force_authenticate(user=self.author)

        res = self.client.put(f'/api/author/{otherAuthor.id}/', payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_profile_without_credentials(self):
        """Test return invalid if user trys to update someone elses profile"""
        payload = {
            'displayName':'abc100',
            'github':'https://github.com/IanSeng'
        }

        res = self.client.put(f'/api/author/{self.authorID}/', payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class TestMeProfileEndpoint(TestCase):
    """Test API(GET)://api/author/me/"""
    def setUp(self):
        self.client = APIClient()
        
    def test_me_endpoint_with_auth(self):
        """Test retrieving my author profile if user is logged in"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=True,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('type', res.data)
        self.assertIn('id', res.data)
        self.assertIn('host', res.data)
        self.assertIn('displayName', res.data)
        self.assertIn('url', res.data)
        self.assertIn('github', res.data)

    def test_me_endpoint_without_auth(self):
        """Test return error if user is not logged in"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_endpoint_without_admin_approval(self):
        """Test return error is author is not admin approved"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=False,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class TestGetAllAuthorsEndpoint(TestCase):
    """Test API(GET)://api/authors/"""
    def setUp(self):
        self.client = APIClient()
    
    def test_get_all_authors_endpoint(self):
        """Test retrieving all authors profile list if user is logged in"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval= True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e').int,
        )
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval= True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3f').int,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get(ALL_AUTHOR_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
    
    def test_get_all_authors_endpoint_without_auth(self):
        """Test unsuccessful getting all authors profile if user is not logged in"""
        res = self.client.get(ALL_AUTHOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_authors_endpoint_not_return_superuser(self):
        """Test retrieving all authors profile list exclude superuser"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval= True,
            type=utils.UserType.superuser.value,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
        )
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval= True,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3f'),
        )
        self.client.force_authenticate(user)

        res = self.client.get(ALL_AUTHOR_URL)
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_get_all_authors_endpoint_not_return_unapproved(self):
        """Test retrieving all authors profile list exclude not admin approved user"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval= True,
            type=utils.UserType.superuser.value,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'),
        )
        create_author(
            username='abc002',
            password='abcpwd',
            adminApproval= False,
            id=uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3f'),
        )
        self.client.force_authenticate(user)

        res = self.client.get(ALL_AUTHOR_URL)
       
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_get_all_authors_endpoint_without_admin_approval(self):
        """Test get all authors endpoint is safeguard by admin approved"""
        user = create_author(
            username='abc001',
            password='abcpwd',
            adminApproval=False,
        )
        self.client.force_authenticate(user=user)

        res = self.client.get(ALL_AUTHOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
