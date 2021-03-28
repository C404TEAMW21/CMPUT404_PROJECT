from django.test import TestCase
from django.contrib.auth import get_user_model

from main import models
import uuid
class ModelTests(TestCase):
    def test_create_user_with_username(self):
        username='test001'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.username, username)
        self.assertEquals(author.type, 'author')
        self.assertTrue(author.check_password(password))
        self.assertTrue(author.id)

    def test_username_stripping_to_alphanumeric(self):
        username='test 001---- 🎉'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.username, "test001")

    def test_author_displayName(self):
        username='test001'
        password='testpwd'
        displayName="🎉John 123"
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            displayName=displayName,
        )

        self.assertEqual(author.displayName, displayName)

    def test_author_github(self):
        username='test001'
        password='testpwd'
        github="http://github.com/IanSeng"
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            github=github,
        )

        self.assertEqual(author.github, github)

    def test_author_url(self):
        username='test001'
        password='testpwd'
        host='https://konnection-client.herokuapp.com'
        id='77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'
    
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
            id=uuid.UUID(id),
        )

        self.assertEqual(author.url, f'{host}/author/{id}')

    def test_author_host(self):
        username='test001'
        password='testpwd'
        host='https://konnection-server.herokuapp.com/'
        author = get_user_model().objects.create_author(
            username=username,
            password=password
        )

        self.assertEqual(author.host, host)

    def test_author_superuser(self):
        username='testsuper001'
        password='testpwd'
        user = get_user_model().objects.create_superuser(
            username=username,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_author_follower_empty(self):
        "author create empty follower list"
        username='test0010'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
        )

        author = models.Followers.objects.create(author=author)  

        self.assertEqual(len(author.followers.all()), 0)

    def test_author_with_follower(self):
        "author create follower list"
        username='test001'
        followerUserName="test002"
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
        )
        follower = get_user_model().objects.create_author(
            username=followerUserName,
            password=password,
        )

        author = models.Followers.objects.create(author=author)  
        author.followers.add(follower)

        self.assertEqual(len(author.followers.all()), 1)

    def test_author_following_empty(self):
        "author create empty following list"
        username='test0010'
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
        )

        author = models.Following.objects.create(author=author)  

        self.assertEqual(len(author.following.all()), 0)

    def test_author_with_following(self):
        "author create follower list"
        username='test001'
        followingUserName="test002"
        password='testpwd'
        author = get_user_model().objects.create_author(
            username=username,
            password=password,
        )
        follower = get_user_model().objects.create_author(
            username=followingUserName,
            password=password,
        )

        author = models.Following.objects.create(author=author)  
        author.following.add(follower)

        self.assertEqual(len(author.following.all()), 1)

    def test_create_follower_object_after_author(self):
        """Test creation of followers object on create of Author"""
        get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )

        self.assertEqual(models.Followers.objects.count(), 1)

    def test_create_following_object_after_author(self):
        """Test creation of following object on create of Author"""
        get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        get_user_model().objects.create_author(
            username='test 002---- 🎉',
            password='testpwd'
        )

        self.assertEqual(models.Following.objects.count(), 2)


    def test_get_all_local_followers(self):
        "test get_all_local_followers function to return all local followers"
        author_a = get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        author_b = get_user_model().objects.create_author(
            username='test 00b---- 🎉',
            password='testpwd'
        )
        
        author = models.Followers.objects.get(author=author_a) 
        author.followers.add(author_b)
        
        self.assertEqual(len(author.get_all_local_followers(author_a)), 1)

    def test_get_all_remote_followers(self):
        "test get_all_remote_followers function to return all remote followers"
        author_a = get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        remote_author_payload = {
            "type":"author",
            "id":"11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"http://team6/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }

        author = models.Followers.objects.get(author=author_a)  
        author.remoteFollowers['11111111-4b43-11e9-910f-b8ca3a9b9f3e'] = remote_author_payload
        author.save()
        
        self.assertEqual(len(author.get_all_remote_followers(author_a)), 1)

   

    def test_get_all_local_followering(self):
        "test get_all_local_following function to return all local following"
        author_a = get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        author_b = get_user_model().objects.create_author(
            username='test 00b---- 🎉',
            password='testpwd'
        )
        
        author = models.Following.objects.get(author=author_a) 
        author.following.add(author_b)
        
        self.assertEqual(len(author.get_all_local_following(author_a)), 1)

    def test_get_all_remote_followering(self):
        "test get_all_remote_following function to return all remote following"
        author_a = get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        remote_author_payload = {
            "type":"author",
            "id":"11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"http://team6/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }

        author = models.Following.objects.get(author=author_a)  
        author.remote_following['11111111-4b43-11e9-910f-b8ca3a9b9f3e'] = remote_author_payload
        author.save()
        
        self.assertEqual(len(author.get_all_remote_following(author_a)), 1)

    def test_get_all_local_friends(self):
        "test get_all_local_friends function to return all local friends"
        author_a = get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        author_b = get_user_model().objects.create_author(
            username='test 00b---- 🎉',
            password='testpwd'
        )

        # B follow A 
        author_a_follwers = models.Followers.objects.get(author=author_a) 
        author_a_follwers.followers.add(author_b)
        # A following B
        author_a_following = models.Following.objects.get(author=author_a) 
        author_a_following.following.add(author_b)

        self.assertEqual(len(author_a_following.get_all_local_friends(author_a)), 1)

    def test_get_all_remote_friends(self):
        "test get_all_local_friends function to return all remote friends"
        author_a = get_user_model().objects.create_author(
            username='test 001---- 🎉',
            password='testpwd'
        )
        remote_author_b_payload = {
            "type":"author",
            "id":"11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "url":"http://team6/api/11111111-4b43-11e9-910f-b8ca3a9b9f3e",
            "host":"http://team6/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        }

        # Remote B follow A 
        author_a_followers = models.Followers.objects.get(author=author_a) 
        author_a_followers.remoteFollowers['11111111-4b43-11e9-910f-b8ca3a9b9f3e'] = remote_author_b_payload
        author_a_followers.save()
        # A following remote B
        author_a_following = models.Following.objects.get(author=author_a) 
        author_a_following.remote_following['11111111-4b43-11e9-910f-b8ca3a9b9f3e'] = remote_author_b_payload
        author_a_following.save()

        self.assertEqual(len(author_a_following.get_all_remote_friends(author_a)), 1)
