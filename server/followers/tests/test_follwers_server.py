from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


from nodes.models import Node
from main import models
import uuid
import httpretty


def create_author(**params):
    """Helper function to create author"""
    return get_user_model().objects.create_author(**params)


def author_b_follow_author_a_url(aId, bId):
    """Helper function to create author B to follow author A URL"""
    return reverse(
        'followers:followers modify',
        kwargs={'id': aId, 'foreignId': bId}
    )


def mock_team6_node():
    node = Node.objects.create(
        remote_server_url='https://team6-project-socialdistrib.herokuapp.com/',
        remote_server_username='username',
        remote_server_password='abc',
        adminApproval=True,
        konnection_username='ourusername',
        konnection_password='password'
    )
    return node


def mock_put_successful_local_follow_team_6(local_uuid, remote_uuid):
    httpretty.register_uri(
        httpretty.PUT,
        f"https://team6-project-socialdistrib.herokuapp.com/author/{remote_uuid}/followers/{local_uuid}",
        status=201,
    )

def mock_put_unsuccessful_local_follow_team_6(local_uuid, remote_uuid):
    httpretty.register_uri(
        httpretty.PUT,
        f"https://team6-project-socialdistrib.herokuapp.com/author/{remote_uuid}/followers/{local_uuid}",
        status=400,
    )

def mock_delete_successful_local_unfollow_team_6(local_uuid, remote_uuid):
    httpretty.register_uri(
        httpretty.DELETE,
        f"https://team6-project-socialdistrib.herokuapp.com/author/{remote_uuid}/followers/{local_uuid}",
        status=200,
    )

def mock_delete_unsuccessful_local_unfollow_team_6(local_uuid, remote_uuid):
    httpretty.register_uri(
        httpretty.DELETE,
        f"https://team6-project-socialdistrib.herokuapp.com/author/{remote_uuid}/followers/{local_uuid}",
        status=400,
    )


class TestAddFollowersEndpointWithRemoteServer(TestCase):
    """Test API(PUT)://api/author/{remote_id}/followers/{local_id}"""

    def setUp(self):
        self.client = APIClient()

    @httpretty.activate
    def test_local_author_to_follow_remote_author(self):
        "Test adding local author to follow remote auhtor and the object is append to following"
        local_author = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        payload = {
            'actor': {
                'host': 'https://konnection-server.herokuapp.com/',
                'id': '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb',
            },
            'object': {
                'host': 'https://team6-project-socialdistrib.herokuapp.com/',
                'id': '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e',
            }
        }
        mock_team6_node()
        mock_put_successful_local_follow_team_6(
            '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb', '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')
        self.client.force_authenticate(user=local_author)

        res = self.client.put(author_b_follow_author_a_url(
            '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e', '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'), payload, format='json')
        author_following_obj = models.Following.objects.get(author=local_author)
        author_following = author_following_obj.get_all_remote_following(author=local_author)

        self.assertEqual(res.status_code,  status.HTTP_201_CREATED)
        self.assertEqual(len(author_following), 1)

    @httpretty.activate
    def test_local_author_to_follow_remote_author_unccessful(self):
        "Test adding local author to follow remote auhtor unsuccessfully"
        local_author = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        payload = {
            'actor': {
                'host': 'https://konnection-server.herokuapp.com/',
                'id': '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb',
            },
            'object': {
                'host': 'https://team6-project-socialdistrib.herokuapp.com/',
                'id': '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e',
            }
        }
        mock_team6_node()
        mock_put_unsuccessful_local_follow_team_6(
            '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb', '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')
        self.client.force_authenticate(user=local_author)

        res = self.client.put(author_b_follow_author_a_url(
            '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e', '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'), payload, format='json')
        author_following_obj = models.Following.objects.get(author=local_author)
        author_following = author_following_obj.get_all_remote_following(author=local_author)

        self.assertEqual(res.status_code,  status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(author_following), 0)

    @httpretty.activate
    def test_invalid_local_author_to_follow_remote_author(self):
        "Test adding invalid local author to follow remote auhtor"
        local_author = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        payload = {
            'actor': {
                'host': 'https://konnection-server.herokuapp.com/',
                'id': 'abc',
            },
            'object': {
                'host': 'https://team6-project-socialdistrib.herokuapp.com/',
                'id': '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e',
            }
        }
        mock_team6_node()
        mock_put_successful_local_follow_team_6(
            'abc', '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')
        self.client.force_authenticate(user=local_author)

        res = self.client.put(author_b_follow_author_a_url(
            '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e', 'abc'), payload, format='json')

        self.assertEqual(res.status_code,  status.HTTP_400_BAD_REQUEST)

class TestDeleteFollowersEndpointWithRemoteServer(TestCase):
    """Test API(DELETE)://api/author/{remote_id}/followers/{local_id}"""

    def setUp(self):
        self.client = APIClient()

    @httpretty.activate
    def test_local_author_to_unfollow_remote_author(self):
        "Test local author to unfollow remote auhtor and the remote auhtor object is remove from following"
        local_author = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        remote_author_payload = {
            "type":"author",
            "id":"77f1df52-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"https://team6-project-socialdistrib.herokuapp.com/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }
        request_payload = {
            'host': "https://team6-project-socialdistrib.herokuapp.com/"
        }
        self.client.force_authenticate(user=local_author)
        local_author_following_obj = models.Following.objects.get(author=local_author)
        # Create Remote user in following
        local_author_following_obj.remote_following["77f1df52-4b43-11e9-910f-b8ca3a9b9f3e"] = remote_author_payload
        local_author_following_obj.save()
        mock_team6_node()
        mock_delete_successful_local_unfollow_team_6('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb', '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')
        author_following = local_author_following_obj.get_all_remote_following(author=local_author)

        res = self.client.delete(author_b_follow_author_a_url(
            '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e', '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'), request_payload, format='json')
        author_following = local_author_following_obj.get_all_remote_following(author=local_author)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(author_following), 0)

    @httpretty.activate
    def test_local_author_to_unfollow_remote_author_unccessful(self):
        "Test local author to unfollow remote auhtor unsuccessfully"
        local_author = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        remote_author_payload = {
            "type":"author",
            "id":"77f1df52-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"https://team6-project-socialdistrib.herokuapp.com/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }
        request_payload = {
            'host': "https://team6-project-socialdistrib.herokuapp.com/"
        }
        self.client.force_authenticate(user=local_author)
        local_author_following_obj = models.Following.objects.get(author=local_author)
        # Create Remote user in following
        local_author_following_obj.remote_following["77f1df52-4b43-11e9-910f-b8ca3a9b9f3e"] = remote_author_payload
        local_author_following_obj.save()
        mock_team6_node()
        mock_delete_unsuccessful_local_unfollow_team_6('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb', '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')
        author_following = local_author_following_obj.get_all_remote_following(author=local_author)

        res = self.client.delete(author_b_follow_author_a_url(
            '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e', '88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'), request_payload, format='json')
        author_following = local_author_following_obj.get_all_remote_following(author=local_author)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(author_following), 1)


    @httpretty.activate
    def test_invalid_local_author_to_unfollow_remote_author(self):
        "Test invalid local author to unfollow remote auhtor"
        local_author = create_author(
            username='abc002',
            password='abcpwd',
            adminApproval=True,
            id=uuid.UUID('88f1df52-4b43-11e9-910f-b8ca3a9b9fbb'),
        )
        request_payload = {
            'host': "https://team6-project-socialdistrib.herokuapp.com/"
        }
        self.client.force_authenticate(user=local_author)
        mock_team6_node()
        mock_delete_successful_local_unfollow_team_6('abc', '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e')

        res = self.client.delete(author_b_follow_author_a_url(
            '77f1df52-4b43-11e9-910f-b8ca3a9b9f3e', 'abc'), request_payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
       